
"""Run test programs (TODO better docstring)"""

import argparse

from enum import Enum
from sys import executable
from typing import Callable, List, Set
from pathlib import Path
import subprocess
import unittest


class TestDirs:
    INVALID_LEX = "invalid_lex"
    INVALID_PARSE = "invalid_parse"
    INVALID_SEMANTICS = "invalid_semantics"
    INVALID_DECLARATIONS = "invalid_declarations"
    INVALID_TYPES = "invalid_types"
    INVALID_STRUCT_TAGS = "invalid_struct_tags"
    VALID = "valid"


dirs = {"invalid": [TestDirs.INVALID_LEX,
                    TestDirs.INVALID_PARSE,
                    TestDirs.INVALID_SEMANTICS,
                    TestDirs.INVALID_DECLARATIONS,
                    TestDirs.INVALID_TYPES,
                    TestDirs.INVALID_STRUCT_TAGS],
        "valid": [TestDirs.VALID]}

DIRECTORIES_BY_STAGE = {
    "lex": {"invalid": [TestDirs.INVALID_LEX],
            "valid": [TestDirs.INVALID_PARSE,
                      TestDirs.INVALID_SEMANTICS,
                      TestDirs.INVALID_DECLARATIONS,
                      TestDirs.INVALID_TYPES,
                      TestDirs.INVALID_STRUCT_TAGS,
                      TestDirs.VALID]},
    "parse": {"invalid": [TestDirs.INVALID_LEX, TestDirs.INVALID_PARSE],
              "valid": [TestDirs.INVALID_SEMANTICS,
                        TestDirs.INVALID_DECLARATIONS,
                        TestDirs.INVALID_TYPES,
                        TestDirs.INVALID_STRUCT_TAGS,
                        TestDirs.VALID]},
    "validate": dirs,
    "tacky": dirs,
    "codegen": dirs,
    "run": dirs
}

# maybe use a bitwise enum here to combine them?


class ExtraCredit(Enum):
    """All extra-credit features"""
    BITWISE = 1
    COMPOUND = 2
    GOTO = 3
    SWITCH = 4
    NAN = 5

# adapted from https://eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases


class TestChapter(unittest.TestCase):
    """Base per-chapter test case"""
    longMessage = False
    test_dir: Path = None  # overridden per subclass

    def tearDown(self) -> None:

        # delete any non-C files aproduced during this testrun
        garbage_files = (f for f in self.test_dir.rglob(
            "*") if not f.is_dir() and f.suffix not in ['.c', '.h'])

        for f in garbage_files:
            f.unlink()


def invoke_compiler(compiler_path: Path, program_path: Path, stage=None) -> int:
    """Invoke compiler and return CompletedProcess object"""
    # TODO make this a method of TestChapter/include compiler_path etc in test_chapter?
    args = [compiler_path]
    if stage is not None and stage != "run":
        args.append(f"--{stage}")

    args.append(program_path)

    proc = subprocess.run(args, capture_output=True, check=True, text=True)
    return proc


def gcc_compile_and_run(prog: Path) -> subprocess.CompletedProcess:
    exe = prog.with_stem(f"expected_{prog.stem}").with_suffix('')
    subprocess.run(["gcc", prog, "-o", exe], check=True)
    return subprocess.run(exe, check=False, text=True, capture_output=True)


def make_invalid_test(compiler_path: Path, stage: str, program_path: Path) -> Callable:

    def test_invalid(self):

        # make sure compiler returned non-zero exit code -
        # if it does, subprocess.run will raise CalledProcessError
        with self.assertRaises(subprocess.CalledProcessError, msg=f"Didn't catch error in {program_path}"):
            invoke_compiler(compiler_path, program_path, stage)

        # make sure we didn't emit executable or assembly code

        # if we compiled /path/to/foo.c, look for /path/to/foo.s
        stem = program_path.stem
        assembly_path = program_path.parent / f'{stem}.s'
        self.assertFalse(assembly_path.exists(
        ), msg=f"Found assembly file {assembly_path} for invalid program!")

        # now look for /path/to/foo
        executable_path = program_path.parent / stem
        self.assertFalse(executable_path.exists())

    return test_invalid


def make_valid_test(compiler_path: Path, stage: str, program_path: Path) -> Callable:
    """Test that compilation up to given stage succeeds, but don't run program"""

    def test_valid(self):
        # run compiler, make sure it doesn't throw an exception
        try:
            invoke_compiler(compiler_path, program_path, stage)
        except subprocess.CalledProcessError as err:
            self.fail(f"compilation failed with error: {err.stderr}")

        # make sure we didn't emit executable or assembly code

        # if we compiled /path/to/foo.c, look for /path/to/foo.s
        stem = program_path.stem
        assembly_path = program_path.parent / f'{stem}.s'
        self.assertFalse(assembly_path.exists(
        ), msg=f"Stage {stage} produced unexpected assembly file {assembly_path}!")

        # now look for /path/to/foo
        executable_path = program_path.parent / stem
        self.assertFalse(executable_path.exists(
        ), msg=f"Stage {stage} produced unexpected executable {executable_path}")

    return test_valid


def make_running_test(compiler_path: Path, program_path: Path) -> Callable:
    """Compile and run program, check results"""

    def test_valid(self):

        # first compile and run the program with GCC
        expected_result = gcc_compile_and_run(program_path)

        # run compiler, make sure it doesn't throw an exception
        try:
            invoke_compiler(compiler_path, program_path)
        except subprocess.CalledProcessError as err:
            self.fail(f"compilation failed with error: {err.stderr}")

        # run the executable
        exe = program_path.with_suffix('')

        result = subprocess.run(
            exe, check=False, capture_output=True, text=True)

        self.assertEqual(expected_result.returncode, result.returncode)
        self.assertEqual(expected_result.stdout, result.stdout)
        self.assertEqual(expected_result.stderr, result.stderr)

    return test_valid


class TestBuilder:
    def __init__(self, compiler: Path, stage: str,
                 chapters: List[int],
                 extra_credit_features: Set[ExtraCredit]) -> None:
        self.compiler = compiler
        self.stage = stage
        self.extra_credit = extra_credit_features
        self.chapters = chapters

    def build_tests(self) -> dict[str, type]:
        testclass_dict = {}
        for chapter in self.chapters:
            testclass_name = f"TestChapter{chapter}"
            testclass_attrs = self.build_tests_for_chapter(chapter)
            testclass_dict[testclass_name] = type(
                testclass_name, (TestChapter,), testclass_attrs)

        return testclass_dict

    def build_tests_for_chapter(self, chapter: int) -> dict[str, Callable]:

        test_dir = Path(__file__).parent.joinpath(
            f"chapter{chapter}").resolve()

        testclass_attrs = {'test_dir': test_dir}
        # run invalid test cases up to the appropriate stage
        for invalid_subdir in DIRECTORIES_BY_STAGE[self.stage]["invalid"]:
            invalid_directory = test_dir / invalid_subdir
            for program in invalid_directory.rglob("*.c"):
                testclass_attrs[f'test_{invalid_subdir}_{program.stem}'] = make_invalid_test(
                    self.compiler, self.stage, program)

        for valid_subdir in DIRECTORIES_BY_STAGE[self.stage]["valid"]:
            valid_directory = test_dir / valid_subdir
            for program in valid_directory.rglob("*.c"):
                if self.stage == "run":
                    testclass_attrs[f'test_valid_{program.stem}'] = make_running_test(
                        self.compiler, program)
                else:
                    testclass_attrs[f'test_valid_{program.stem}'] = make_valid_test(
                        self.compiler, self.stage, program)

        return testclass_attrs


"""
which folders are we looking in?
- invalid_lex/
- invalid_parse/
- invalid_semantics/
- invalid_declarations/
- invalid_types/
    inconsistent --> shift from invalid_semantics/ to invalid_declarations/ and invalid_types/ in chapter 10! do we care?
    this continues into chapter 12 and on
    in chapter 18, we have invalid_types/pointer_conversions/, other subdirectories
- invalid_struct_tags/
    chapter 19
- valid/
    valid/libraries/
        <x>.c and <x>_client.c
    valid/arguments_in_registers/ chapter 10
    valid/explicit_casts, etc in chapter 13, 14,

"""


def parse_arguments() -> argparse.ArgumentParser:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cc", type=str, help="Path to your compiler")
    # QUESTION: should this include tests from previous chapters too? yes, per chapters 3, 4
    # but maybe add an option to just run most recent tests?
    parser.add_argument("--chapter", type=int, choices=range(0, 19),  required=True,  # let people specify optimization chapters?
                        help="Specify which chapter to test. (By default, this will run the tests from earlier chapters as well.)")
    parser.add_argument("--latest-only", action="store_true",
                        help="Only run tests for the current chapter, not earlier chapters")
    parser.add_argument(
        "--stage", type=str, choices=["lex", "parse", "validate", "tacky", "codegen"])
    parser.add_argument("--bitwise", action="store_const",
                        const=ExtraCredit.BITWISE, help="Include tests for bitwise operations")
    parser.add_argument("--compound", action="store_const",
                        const=ExtraCredit.COMPOUND, help="Include tests for compound assignment")
    parser.add_argument("--goto", action="store_const", const=ExtraCredit.GOTO,
                        help="Include tests for goto and labeled statements")
    parser.add_argument("--switch", action="store_const",
                        const=ExtraCredit.SWITCH, help="Include tests for switch statements")
    parser.add_argument("--nan", action="store_const", const=ExtraCredit.NAN,
                        help="Include tests for floating-point NaN")
    # TODO should this be mutually exclusive with other extra-credit flags?
    parser.add_argument("--extra-credit", action="store_true",
                        help="Include tests for all extra credit features")
    return parser.parse_args()


def main():
    """Main entry point for test runner"""
    args = parse_arguments()
    compiler = Path(args.cc).resolve()

    # Get set of extra-credit features
    if args.extra_credit:
        extra_credit_features = set(list(ExtraCredit))
    else:
        # Get all extra-credit values specified on the command line,
        # remove None, which indicates a command-line option wasn't set
        extra_credit_features = set(
            [args.bitwise, args.compound, args.goto, args.switch, args.nan]).remove(None)

    if args.latest_only:
        chapters = args.chapter
    else:
        chapters = range(2, args.chapter + 1)

    stage = args.stage or "run"  # by default, compile and run the program
    test_builder = TestBuilder(compiler=compiler, stage=stage,
                               chapters=chapters, extra_credit_features=set())  # TODO extra credit

    names = []
    for testcase_name, testcase_type in test_builder.build_tests().items():
        globals()[testcase_name] = testcase_type
        names.append(testcase_name)
    tests = unittest.defaultTestLoader.loadTestsFromName('TestCompiler')

    # TODO command-line arg to control verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(tests)

    # runner = unittest.TextTestRunner()
    # runner.run(suite)
    # runner.run(TestChapter())

    # stage = args.stage or "run"  # by default, compile and run the program

    # test_runner = TestRunner(compiler, stage, extra_credit_features, chapters)
    # test_runner.run()


if __name__ == "__main__":
    main()
