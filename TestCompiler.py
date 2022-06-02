
"""Run test programs (TODO better docstring)"""

import argparse

from enum import Flag, auto, unique
from functools import reduce
from operator import ior
import re
from typing import Dict, Callable, List, Set
from pathlib import Path
import subprocess
import unittest


def replace_stem(path: Path, new_stem: str) -> Path:
    try:
        return path.with_stem(new_stem)
    except AttributeError:
        # python versions before 3.9
        # stick old suffix on new stem
        return path.with_name(new_stem).with_suffix(path.suffix)


class TestDirs:
    # invalid programs
    INVALID_LEX = "invalid_lex"
    INVALID_PARSE = "invalid_parse"
    INVALID_SEMANTICS = "invalid_semantics"
    INVALID_DECLARATIONS = "invalid_declarations"
    INVALID_TYPES = "invalid_types"
    INVALID_STRUCT_TAGS = "invalid_struct_tags"
    # valid test programs for parts I & II
    VALID = "valid"
    # valid test programs for part III
    ALL_OPTS = "all_optimizations"
    CONST = "constant_folding"
    COPY_PROP = "copy_propagation"
    DSE = "dead_store_elimination"
    UCE = "unreachable_code_eimination"
    REG_ALLOC = "int_only"
    REG_ALLOC_PARTII = "all_types"


dirs = {"invalid": [TestDirs.INVALID_LEX,
                    TestDirs.INVALID_PARSE,
                    TestDirs.INVALID_SEMANTICS,
                    TestDirs.INVALID_DECLARATIONS,
                    TestDirs.INVALID_TYPES,
                    TestDirs.INVALID_STRUCT_TAGS],
        "valid": [TestDirs.VALID, TestDirs.ALL_OPTS, TestDirs.CONST,
                  TestDirs.COPY_PROP, TestDirs.DSE, TestDirs.UCE, TestDirs.REG_ALLOC,
                  TestDirs.REG_ALLOC_PARTII]
        }

DIRECTORIES_BY_STAGE = {
    "lex": {"invalid": [TestDirs.INVALID_LEX],
            "valid": [TestDirs.INVALID_PARSE,
                      TestDirs.INVALID_SEMANTICS,
                      TestDirs.INVALID_DECLARATIONS,
                      TestDirs.INVALID_TYPES,
                      TestDirs.INVALID_STRUCT_TAGS] + dirs["valid"]},
    "parse": {"invalid": [TestDirs.INVALID_LEX, TestDirs.INVALID_PARSE],
              "valid": [TestDirs.INVALID_SEMANTICS,
                        TestDirs.INVALID_DECLARATIONS,
                        TestDirs.INVALID_TYPES,
                        TestDirs.INVALID_STRUCT_TAGS] + dirs["valid"]},
    "validate": dirs,
    "tacky": dirs,
    "codegen": dirs,
    "run": dirs
}

# maybe use a bitwise enum here to combine them?


@unique
class ExtraCredit(Flag):
    """All extra-credit features"""
    BITWISE = auto()
    COMPOUND = auto()
    GOTO = auto()
    SWITCH = auto()
    NAN = auto()
    NONE = 0
    ALL = BITWISE | COMPOUND | GOTO | SWITCH | NAN

    def to_regex(self):
        pattern = '|'.join(name.lower()
                           for name, v in ExtraCredit.__members__.items() if v in self)
        return re.compile(pattern)

# adapted from https://eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases


def gcc_build_obj(prog: Path) -> None:
    """Compile source file to an object file"""
    objfile = prog.with_suffix('.o')

    # IMPORTANT: if we're building a library, and 'gcc' command actually
    # points to clang, which it does on macOS, we must _not_ enable optimizations
    # Clang optimizes out sign-/zero-extension for narrow args
    # which violates the System V ABI and breaks ABI compatibility
    # with our implementation
    # see https://stackoverflow.com/a/36760539
    subprocess.run(["gcc", prog, "-c", "-o", objfile], check=True)


class TestChapter(unittest.TestCase):
    """Base per-chapter test case"""
    longMessage = False

    # properties overridden by subclass
    test_dir: Path = None
    cc: Path = None
    options: List[str]
    exit_stage: str = None
    extra_credit: Set[ExtraCredit] = set()

    def tearDown(self) -> None:

        # delete any non-C files aproduced during this testrun
        garbage_files = (f for f in self.test_dir.rglob(
            "*") if not f.is_dir() and f.suffix not in ['.c', '.h'])

        for f in garbage_files:
            f.unlink()

    def gcc_compile_and_run(self, *args: Path, prefix_output=False) -> subprocess.CompletedProcess:
        exe = args[0].with_suffix('')
        if prefix_output:
            exe = replace_stem(exe, f"expected_{exe.stem}")

        # capture output so we don't see warnings, and so we can report failures
        subprocess.run(["gcc"] + list(args) + ["-o", exe],
                       check=True, capture_output=True)
        return subprocess.run([exe], check=False, text=True, capture_output=True)

    def invoke_compiler(self, program_path, cc_opt=None) -> subprocess.CompletedProcess:
        """Invoke compiler and return CompletedProcess object"""
        # when testing early stages, pass current stage as compiler option (e.g. --lex)
        # for testing library functions, we'll use -c to assemble without linking
        # and to test optimizations we'll use -s to keep assembly code
        if cc_opt is None and self.exit_stage is not None:
            cc_opt = f"--{self.exit_stage}"

        args = [self.cc] + self.options
        if cc_opt is not None:
            args.append(cc_opt)

        args.append(program_path)

        proc = subprocess.run(args, capture_output=True,
                              check=False, text=True)
        return proc

    def validate_no_output(self, program_path: str):
        """make sure we didn't emit executable or assembly code"""

        # if we compiled /path/to/foo.c, look for /path/to/foo.s
        stem = program_path.stem
        assembly_path = program_path.parent / f'{stem}.s'
        self.assertFalse(assembly_path.exists(
        ), msg=f"Found assembly file {assembly_path} for invalid program!")

        # now look for /path/to/foo
        executable_path = program_path.parent / stem
        self.assertFalse(executable_path.exists())

    def validate_runs(self, expected: subprocess.CompletedProcess, actual: subprocess.CompletedProcess):
        self.assertEqual(expected.returncode, actual.returncode,
                         msg=f"Expected return code {expected.returncode}, found {actual.returncode}")
        self.assertEqual(expected.stdout, actual.stdout,
                         msg=f"Expected output {expected.stdout}, found {actual.stdout}")
        self.assertEqual(expected.stderr, actual.stderr,
                         msg=f"Expected error output {expected.stderr}, found {actual.stderr}")

    def compile_failure(self, program_path):

        # make sure compiler returned non-zero exit code -
        # if it does, subprocess.run will raise CalledProcessError
        with self.assertRaises(subprocess.CalledProcessError, msg=f"Didn't catch error in {program_path}"):
            result = self.invoke_compiler(program_path)
            result.check_returncode()

        self.validate_no_output(program_path)

    def compile_success(self, program_path):
        # run compiler up to stage, make sure it doesn't throw an exception
        result = self.invoke_compiler(program_path)
        self.assertEqual(result.returncode, 0,
                         msg=f"compilation failed with error: {result.stderr}")

        # make sure we didn't emit executable or assembly code
        self.validate_no_output(program_path)

    def compile_and_run(self, program_path):

        # first compile and run the program with GCC
        expected_result = self.gcc_compile_and_run(
            program_path, prefix_output=True)

        # run compiler, make sure it doesn't throw an exception

        compile_result = self.invoke_compiler(program_path)
        self.assertEqual(compile_result.returncode, 0,
                         msg=f"compilation failed with error: {compile_result.stderr}")

        # run the executable
        exe = program_path.with_suffix('')

        result = subprocess.run(
            [exe], check=False, capture_output=True, text=True)

        self.validate_runs(expected_result, result)

    def compile_client_and_run(self, program_path: Path):
        """Compile client with self.cc and library with GCC, make sure they work together"""
        lib_source = replace_stem(program_path,
                                  program_path.stem[:-len('_client')])  # strip _client from filename

        gcc_build_obj(lib_source)
        self.invoke_compiler(program_path, cc_opt="-c")

        # link both object files and run resulting executable
        result = self.gcc_compile_and_run(lib_source.with_suffix(
            '.o'), program_path.with_suffix('.o'))

        # now compile both with gcc and run resulting executable
        expected_result = self.gcc_compile_and_run(
            lib_source, program_path, prefix_output=True)

        # make sure results are the same
        self.validate_runs(expected_result, result)

    def compile_lib_and_run(self, program_path: Path):
        """Compile lib with self.cc and client with GCC, make sure they work together"""
        client_source = replace_stem(program_path, program_path.stem+"_client")

        gcc_build_obj(client_source)
        self.invoke_compiler(program_path, cc_opt="-c")

        # link both object files and run resulting executable
        result = self.gcc_compile_and_run(program_path.with_suffix(
            '.o'), client_source.with_suffix('.o'))

        # now compile both with gcc and run resulting executable
        expected_result = self.gcc_compile_and_run(
            program_path, client_source, prefix_output=True)

        # make sure results are the same
        self.validate_runs(expected_result, result)


def make_invalid_test(program_path: Path) -> Callable:
    """Return a function to test that compiling program at program_path fails"""

    def test_invalid(self: TestChapter):
        self.compile_failure(program_path)

    return test_invalid


def make_valid_test(program_path: Path) -> Callable:
    """Return a function to test that compiling program at program_path succeeds"""

    def test_valid(self: TestChapter):
        self.compile_success(program_path)

    return test_valid


def make_running_test(program_path: Path) -> Callable:
    """Compile and run program, check results"""

    def test_valid(self: TestChapter):
        self.compile_and_run(program_path)

    return test_valid


def make_client_test(program_path: Path) -> Callable:

    def test_client(self):
        self.compile_client_and_run(program_path)

    return test_client


def make_lib_test(program_path: Path) -> Callable:

    def test_lib(self):
        self.compile_lib_and_run(program_path)

    return test_lib


def extra_credit_programs(source_dir: Path, extra_credit_flags: ExtraCredit) -> List[Path]:
    extra_cred_regex = extra_credit_flags.to_regex()
    for source_prog in source_dir.rglob("*.c"):
        if extra_cred_regex.search(source_prog.stem):
            yield source_prog


def build_test_class(chapter: int, compiler: Path, options: List[str], stage: str, extra_credit: ExtraCredit, skip_invalid: bool) -> Dict[str, Callable]:

    test_dir = Path(__file__).parent.joinpath(
        f"chapter{chapter}").resolve()

    testclass_attrs = {"test_dir": test_dir,
                       "cc": compiler,
                       "options": options,
                       "exit_stage": None if stage == "run" else stage,
                       "extra_credit": extra_credit}

    # generate invalid test cases up to the appropriate stage
    if not skip_invalid:
        for invalid_subdir in DIRECTORIES_BY_STAGE[stage]["invalid"]:
            invalid_directory = test_dir / invalid_subdir
            for program in invalid_directory.rglob("*.c"):
                testclass_attrs[f'test_{invalid_subdir}_{program.stem}'] = make_invalid_test(
                    program)

            # if we've enabled any extra-credit features, look for programs that test those too
            if extra_credit:
                invalid_extra_credit_directory = test_dir / \
                    f"{invalid_subdir}_extra_credit"
                for program in extra_credit_programs(invalid_extra_credit_directory, extra_credit):
                    testclass_attrs[f'test_{invalid_subdir}_extra_credit_{program.stem}'] = make_invalid_test(
                        program)

    for valid_subdir in DIRECTORIES_BY_STAGE[stage]["valid"]:

        valid_directory = test_dir / valid_subdir
        lib_subdir = valid_directory / "libraries"
        for program in valid_directory.rglob("*.c"):
            test_name = f"test_{valid_subdir}_{program.stem}"
            if stage == "run":
                # programs in valid/libraries are special
                if lib_subdir not in program.parents:
                    testclass_attrs[test_name] = make_running_test(
                        program)
                elif program.stem.endswith("client"):
                    testclass_attrs[test_name] = make_client_test(
                        program)
                else:
                    testclass_attrs[test_name] = make_lib_test(
                        program)
            else:
                testclass_attrs[test_name] = make_valid_test(
                    program)

        # add extra-credit tests
        # TODO refactor w/ non-extra-credit code above
        if extra_credit:
            valid_extra_credit_directory = test_dir / \
                f"{valid_subdir}_extra_credit"
            valid_extra_credit_lib_subdir = valid_extra_credit_directory / "libraries"
            for program in extra_credit_programs(valid_extra_credit_directory, extra_credit):
                test_name = f"test_{valid_subdir}_extra_credit_{program.stem}"
                if stage == "run":
                    # programs in valid/libraries are special
                    if valid_extra_credit_lib_subdir not in program.parents:
                        testclass_attrs[test_name] = make_running_test(
                            program)
                    elif program.stem.endswith("client"):
                        testclass_attrs[test_name] = make_client_test(
                            program)
                    else:
                        testclass_attrs[test_name] = make_lib_test(
                            program)
                else:
                    testclass_attrs[test_name] = make_valid_test(
                        program)

    testclass_name = f"TestChapter{chapter}"
    testclass_type = type(testclass_name, (TestChapter,), testclass_attrs)
    return testclass_name, testclass_type


def parse_arguments() -> argparse.ArgumentParser:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cc", type=str, help="Path to your compiler")
    # QUESTION: should this include tests from previous chapters too? yes, per chapters 3, 4
    # but maybe add an option to just run most recent tests?
    parser.add_argument("--chapter", type=int, choices=range(0, 22),  required=True,
                        help="Specify which chapter to test. (By default, this will run the tests from earlier chapters as well.)")
    parser.add_argument("--latest-only", action="store_true",
                        help="Only run tests for the current chapter, not earlier chapters")
    parser.add_argument("--skip-invalid", action="store_true",
                        help="Only run valid test programs (useful when testing backend changes)")
    parser.add_argument("--failfast", "-f", action="store_true",
                        help="Stop on first test failure")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parser.add_argument(
        "--stage", type=str, choices=["lex", "parse", "validate", "tacky", "codegen"])
    parser.add_argument("--bitwise", action="append_const", dest="extra_credit",
                        const=ExtraCredit.BITWISE, help="Include tests for bitwise operations")
    parser.add_argument("--compound", action="append_const", dest="extra_credit",
                        const=ExtraCredit.COMPOUND, help="Include tests for compound assignment")
    parser.add_argument("--goto", action="append_const", const=ExtraCredit.GOTO, dest="extra_credit",
                        help="Include tests for goto and labeled statements")
    parser.add_argument("--switch", action="append_const", dest="extra_credit",
                        const=ExtraCredit.SWITCH, help="Include tests for switch statements")
    parser.add_argument("--nan", action="store_const", const=ExtraCredit.NAN, dest="append_const",
                        help="Include tests for floating-point NaN")
    # TODO should this be mutually exclusive with other extra-credit flags?
    parser.add_argument("--extra-credit", action="append_const", const=ExtraCredit.ALL,
                        help="Include tests for all extra credit features")
    # extra args to pass through to compiler, should be followed by --
    parser.add_argument("extra_cc_options", type=str, nargs="*")
    return parser.parse_intermixed_args()


def main():
    """Main entry point for test runner"""
    args = parse_arguments()
    compiler = Path(args.cc).resolve()

    # merge list of extra-credit features into bitvector
    if args.extra_credit is not None:
        extra_credit = reduce(ior, args.extra_credit)
    else:
        extra_credit = ExtraCredit.NONE

    if args.latest_only:
        chapters = [args.chapter]
    else:
        chapters = range(2, args.chapter + 1)

    stage = args.stage or "run"  # by default, compile and run the program

    # create a subclass of TestChapter for each chapter,
    # dynamically adding a test case for each source program
    for chapter in chapters:
        class_name, class_type = build_test_class(
            chapter, compiler, args.extra_cc_options, stage, extra_credit, args.skip_invalid)
        globals()[class_name] = class_type

    tests = unittest.defaultTestLoader.loadTestsFromName('TestCompiler')

    runner = unittest.TextTestRunner(
        verbosity=args.verbose, failfast=args.failfast)
    runner.run(tests)


if __name__ == "__main__":
    main()
