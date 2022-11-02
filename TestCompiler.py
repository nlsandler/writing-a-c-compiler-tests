
"""Run test programs (TODO better docstring)"""
from test_base import TestBase
import argparse

from functools import reduce
from operator import ior
from typing import Callable, List, Tuple, Iterable, Type
from pathlib import Path
import unittest

from test_base import AssemblyTest


def make_invalid_test(program_path: Path) -> Callable:
    """Return a function to test that compiling program at program_path fails"""

    def test_invalid(self: TestBase.TestChapter):
        self.compile_failure(program_path)

    return test_invalid


def make_valid_test(program_path: Path) -> Callable:
    """Return a function to test that compiling program at program_path succeeds"""

    def test_valid(self: TestBase.TestChapter):
        self.compile_success(program_path)

    return test_valid


def make_running_test(program_path: Path) -> Callable:
    """Compile and run program, check results"""

    def test_valid(self: TestBase.TestChapter):
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


def make_constant_folding_test(program_path: Path) -> Callable:

    def test_fold_const(self: AssemblyTest.ConstantFoldingTest):
        self.optimization_test(program_path)

    return test_fold_const


def extra_credit_programs(source_dir: Path, extra_credit_flags: TestBase.ExtraCredit) -> Iterable[Path]:
    extra_cred_regex = extra_credit_flags.to_regex()
    for source_prog in source_dir.rglob("*.c"):
        if extra_cred_regex.search(source_prog.stem):
            yield source_prog


def find_valid_subdirectories(chapter: int, stage: str, optimization: AssemblyTest.Optimizations, int_only: bool) -> Iterable[Path]:
    if chapter < 20:
        return map(Path, TestBase.DIRECTORIES_BY_STAGE[stage]["valid"])
    if chapter == 20:

        if optimization == AssemblyTest.Optimizations.CONSTANT_FOLD:
            base_path = Path("constant_folding")
            test_dirs = [base_path / "int_only"]
            if not int_only:
                test_dirs.append(base_path / "all_types")
        elif optimization == AssemblyTest.Optimizations.COPY_PROP:
            base_path = Path("copy_propagation")
            test_dirs = [base_path/"int_only"]
            if not int_only:
                test_dirs.append(base_path / "all_types")
        else:
            raise NotImplementedError("we handle these differently")

        return test_dirs
    raise NotImplementedError("reg allocation tests")


def build_test_class(chapter: int, compiler: Path, options: List[str], stage: str, extra_credit: TestBase.ExtraCredit, skip_invalid: bool, optimization: AssemblyTest.Optimizations, int_only: bool) -> Tuple[str, Callable]:

    test_dir = Path(__file__).parent.joinpath(
        f"chapter{chapter}").resolve()

    testclass_name = f"TestChapter{chapter}"

    testclass_attrs = {"test_dir": test_dir,
                       "cc": compiler,
                       "options": options,
                       "exit_stage": None if stage == "run" else stage,
                       "extra_credit": extra_credit}

    base_class: Type[TestBase.TestChapter] = TestBase.TestChapter
    if chapter == 20:

        if optimization == AssemblyTest.Optimizations.UNREACHABLE_CODE_ELIM:
            # don't go through usual test-finding process for unreachable code elimination tests
            testclass_attrs["test_dir"] = test_dir / \
                "unreachable_code_elimination"
            testclass_type = type(
                testclass_name, (AssemblyTest.UnreachableCodeTest,), testclass_attrs)
            return testclass_name, testclass_type
        elif optimization == AssemblyTest.Optimizations.COPY_PROP:
            # don't go through usual test-finding process for copy prop tests
            # TODO deal with not-int-only tests
            base_class = AssemblyTest.CopyPropTest
        elif optimization == AssemblyTest.Optimizations.CONSTANT_FOLD:
            base_class = AssemblyTest.ConstantFoldingTest
        else:
            raise NotImplementedError("other optimizations")

    # generate invalid test cases up to the appropriate stage
    # Note: there are no valid optimizaton tests
    if not skip_invalid:
        for invalid_subdir in TestBase.DIRECTORIES_BY_STAGE[stage]["invalid"]:
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

    for valid_subdir in find_valid_subdirectories(chapter, stage, optimization, int_only):

        valid_directory = test_dir / valid_subdir

        lib_subdir = valid_directory / "libraries"
        for program in valid_directory.rglob("*.c"):
            test_name = f"test_{valid_subdir}_{program.stem}"
            if stage == "run":
                # optimization tests are special
                if any(p for p in program.parents if p.stem == "constant_folding"):
                    testclass_attrs[test_name] = make_constant_folding_test(
                        program)
                # programs in valid/libraries are special
                elif lib_subdir not in program.parents:
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
                    # optimization tests are special
                    if any(p for p in program.parents if p.stem == "constant_folding"):
                        testclass_attrs[test_name] = make_constant_folding_test(
                            program)
                    if any(p for p in program.parents if p.stem == "copy_propagation"):
                        testclass_attrs[test_name] = AssemblyTest.CopyPropTest.get_test_for_path(
                            program)
                    # programs in valid/libraries are special
                    elif valid_extra_credit_lib_subdir not in program.parents:
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

    testclass_type = type(
        testclass_name, (base_class,), testclass_attrs)
    return testclass_name, testclass_type


def parse_arguments() -> argparse.Namespace:
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
                        const=TestBase.ExtraCredit.BITWISE, help="Include tests for bitwise operations")
    parser.add_argument("--compound", action="append_const", dest="extra_credit",
                        const=TestBase.ExtraCredit.COMPOUND, help="Include tests for compound assignment")
    parser.add_argument("--goto", action="append_const", const=TestBase.ExtraCredit.GOTO, dest="extra_credit",
                        help="Include tests for goto and labeled statements")
    parser.add_argument("--switch", action="append_const", dest="extra_credit",
                        const=TestBase.ExtraCredit.SWITCH, help="Include tests for switch statements")
    parser.add_argument("--nan", action="store_const", const=TestBase.ExtraCredit.NAN, dest="append_const",
                        help="Include tests for floating-point NaN")
    # TODO should this be mutually exclusive with other extra-credit flags?
    parser.add_argument("--extra-credit", action="append_const", const=TestBase.ExtraCredit.ALL,
                        help="Include tests for all extra credit features")
    # optimization tests
    optimize_opts = parser.add_mutually_exclusive_group()
    optimize_opts.add_argument('--fold-constants', action='store_const', dest="optimization",
                               const=AssemblyTest.Optimizations.CONSTANT_FOLD, help='Enable constant folding, and run constant folding tests in chapter 20')
    optimize_opts.add_argument('--eliminate-unreachable-code', action='store_const', dest="optimization",
                               const=AssemblyTest.Optimizations.UNREACHABLE_CODE_ELIM, help="Enable constant folding and unreachable code elimination; run unreachable code elimination tests in chapter 20"
                               )
    optimize_opts.add_argument('--propagate-copies', action='store_const', dest="optimization", const=AssemblyTest.Optimizations.COPY_PROP,
                               help="Enable constant folding, unreachable code elimination, and copy propagation")
    parser.add_argument("--int-only", action="store_true",
                        help="Only run optimization tests that use Part I language features")
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
        extra_credit = TestBase.ExtraCredit.NONE

    if args.latest_only:
        chapters = [args.chapter]
    else:
        chapters = range(2, args.chapter + 1)

    stage = args.stage or "run"  # by default, compile and run the program
    cc_options = args.extra_cc_options
    # add optimization options (they're cumulative)
    if args.optimization == AssemblyTest.Optimizations.CONSTANT_FOLD:
        cc_options.append("--fold-constants")
    elif args.optimization == AssemblyTest.Optimizations.UNREACHABLE_CODE_ELIM:
        cc_options.extend(["--fold-constants", "--eliminate-unreachable-code"])
    elif args.optimization == AssemblyTest.Optimizations.COPY_PROP:
        cc_options.extend(
            ["--fold-constants", "--eliminate-unreachable-code", "--propagate-copies"])
    # create a subclass of TestChapter for each chapter,
    # dynamically adding a test case for each source program
    for chapter in chapters:
        class_name, class_type = build_test_class(
            chapter, compiler, cc_options, stage, extra_credit, args.skip_invalid, args.optimization, args.int_only)
        globals()[class_name] = class_type

    tests = unittest.defaultTestLoader.loadTestsFromName('TestCompiler')

    # handle ctrl-C cleanly
    unittest.installHandler()
    runner = unittest.TextTestRunner(
        verbosity=args.verbose, failfast=args.failfast)
    runner.run(tests)


if __name__ == "__main__":
    main()
