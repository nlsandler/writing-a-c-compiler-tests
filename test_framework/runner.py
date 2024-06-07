"""Argument parsing and main entry point for test script"""

from __future__ import annotations

import argparse
import itertools
import platform
import subprocess
import unittest
import warnings
from functools import reduce
from operator import ior
from pathlib import Path
from typing import Iterable, Optional, List, Type

import test_framework
import test_framework.basic
import test_framework.regalloc
import test_framework.tacky.suite
from test_framework.basic import ExtraCredit
from test_framework.regalloc import CHAPTER as REGALLOC_CHAPTER
from test_framework.tacky.common import CHAPTER as TACKY_OPT_CHAPTER
from test_framework.tacky.suite import Optimizations


def get_optimization_flags(
    latest_chapter: int,
    optimization_opt: Optional[test_framework.tacky.suite.Optimizations],
) -> list[str]:
    """Return list of command-line optimization options to pass to the compiler under test"""

    if optimization_opt is None:
        if latest_chapter < TACKY_OPT_CHAPTER:
            # don't enable optimizations
            return []
        # otherwise, default to enabling all optimizations
        return [
            "--fold-constants",
            "--eliminate-unreachable-code",
            "--propagate-copies",
            "--eliminate-dead-stores",
        ]

    # we enable optimizations cumulatively
    # you can test each one in isolation by passing them as extra compiler
    # arguments
    if latest_chapter == REGALLOC_CHAPTER:
        raise ValueError(
            (
                f"Option {optimization_opt} is incompatible with register allocation tests. "
                "All TACKY optimizations must be enabled."
            )
        )

    if optimization_opt == Optimizations.CONSTANT_FOLD:
        return ["--fold-constants"]
    if optimization_opt == Optimizations.UNREACHABLE_CODE_ELIM:
        return ["--fold-constants", "--eliminate-unreachable-code"]
    if optimization_opt == Optimizations.COPY_PROP:
        return [
            "--fold-constants",
            "--eliminate-unreachable-code",
            "--propagate-copies",
        ]
    if optimization_opt == Optimizations.DEAD_STORE_ELIM:
        return [
            "--fold-constants",
            "--eliminate-unreachable-code",
            "--propagate-copies",
            "--eliminate-dead-stores",
        ]

    # we got an unrecognizeable option (or ALL, which should never be passed
    # to this function)
    raise NotImplementedError(f"Don't know how to handle option {optimization_opt}")


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser()
    # --check-setup checks your system setup rather than testing the compiler itself
    parser.add_argument(
        "--check-setup", action="store_true", help="Test your system configuration"
    )

    # required arguments (if not use --check-setup)
    parser.add_argument(
        "cc", type=str, nargs="?", default=None, help="Path to your compiler"
    )
    parser.add_argument(
        "--chapter",
        type=int,
        choices=range(1, REGALLOC_CHAPTER + 1),
        help=(
            "Specify which chapter to test. "
            "(By default, this will run the tests from earlier chapters as well.)"
        ),
    )
    # more generally-useful options
    parser.add_argument(
        "--latest-only",
        action="store_true",
        help="Only run tests for the current chapter, not earlier chapters",
    )
    parser.add_argument(
        "--skip-invalid",
        action="store_true",
        help="Only run valid test programs (useful when testing backend changes)",
    )
    parser.add_argument(
        "--failfast", "-f", action="store_true", help="Stop on first test failure"
    )
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parser.add_argument(
        # by default, compile and run the program
        "--stage",
        type=str,
        default="run",
        choices=["lex", "parse", "validate", "tacky", "codegen", "run"],
    )
    parser.add_argument(
        "--expected-error-codes",
        type=int,
        nargs="+",
        metavar="n",
        help="Specify one or more exit codes (in range 1-255) that your compiler may return when rejecting a program. "
        "If specified, invalid test cases will pass only if the compiler exits with one of these error codes. "
        "If not specified, invalid test cases pass if the compiler exits with any non-zero code. "
        "Used to distinguish between expected failures (i.e. rejecting an invalid source program) and unexpected failures (segfaults/internal errors).",
    )
    parser.add_argument(
        "--keep-asm-on-failure",
        action="store_true",
        help="Recompile any valid test programs that fail with the -S option to preserve assembly output.",
    )
    # options to enable extra-credit tests
    parser.add_argument(
        "--bitwise",
        action="append_const",
        dest="extra_credit",
        const=ExtraCredit.BITWISE,
        help="Include tests for bitwise operations",
    )
    parser.add_argument(
        "--compound",
        action="append_const",
        dest="extra_credit",
        const=ExtraCredit.COMPOUND,
        help="Include tests for compound assignment",
    )
    parser.add_argument(
        "--increment",
        action="append_const",
        dest="extra_credit",
        const=ExtraCredit.INCREMENT,
        help="Include tests for increment and decrement operators",
    )
    parser.add_argument(
        "--goto",
        action="append_const",
        const=ExtraCredit.GOTO,
        dest="extra_credit",
        help="Include tests for goto and labeled statements",
    )
    parser.add_argument(
        "--switch",
        action="append_const",
        dest="extra_credit",
        const=ExtraCredit.SWITCH,
        help="Include tests for switch statements",
    )
    parser.add_argument(
        "--nan",
        action="append_const",
        const=ExtraCredit.NAN,
        dest="extra_credit",
        help="Include tests for floating-point NaN",
    )
    parser.add_argument(
        "--union",
        action="append_const",
        const=ExtraCredit.UNION,
        dest="extra_credit",
        help="Include tests for union types",
    )
    parser.add_argument(
        "--extra-credit",
        action="append_const",
        const=ExtraCredit.ALL,
        help="Include tests for all extra credit features",
    )
    # optimization tests
    optimize_opts = parser.add_mutually_exclusive_group()
    optimize_opts.add_argument(
        "--fold-constants",
        action="store_const",
        dest="optimization",
        const=Optimizations.CONSTANT_FOLD,
        help="Run constant folding tests and enable constant folding on tests from earlier chapters",
    )
    optimize_opts.add_argument(
        "--eliminate-unreachable-code",
        action="store_const",
        dest="optimization",
        const=Optimizations.UNREACHABLE_CODE_ELIM,
        help=(
            "Run unreachable code elimination tests, "
            "And enable constant folding and unreachable code elimination on tests from earlier chapters."
        ),
    )
    optimize_opts.add_argument(
        "--propagate-copies",
        action="store_const",
        dest="optimization",
        const=Optimizations.COPY_PROP,
        help="Enable constant folding, unreachable code elimination, and copy propagation",
    )
    optimize_opts.add_argument(
        "--eliminate-dead-stores",
        action="store_const",
        dest="optimization",
        const=Optimizations.DEAD_STORE_ELIM,
        help="Enable all four optimizations",
    )
    parser.add_argument(
        "--int-only",
        action="store_true",
        help="Only run optimization tests that use Part I language features",
    )
    parser.add_argument(
        "--no-coalescing",
        action="store_true",
        help="Run register allocation tests that don't rely on coalescing",
    )
    # extra args to pass through to compiler, should be followed by --
    parser.add_argument("extra_cc_options", type=str, nargs="*")
    args = parser.parse_intermixed_args()

    # extra validation of parsed args

    # if --check-setup is present, shouldn't have any other options
    if args.check_setup:
        ignored_args = [
            k for k, v in vars(args).items() if bool(v) and (k != "check_setup")
        ]
        if ignored_args:
            warnings.warn(
                f"These options have no effect when combined with --check-setup: {', '.join(ignored_args)}."
            )
    # if it's absent, need to specify compiler and chapter
    elif not (args.cc and args.chapter):
        parser.error("cc and --chapter are required")

    if args.stage and args.stage != "run" and args.chapter >= TACKY_OPT_CHAPTER:
        # TODO better error message here
        parser.error(
            message=f"Testing intermediate stage not allowed with Part III tests (chapter {args.chapter})",
        )

    if (
        args.extra_credit
        and ExtraCredit.ALL in args.extra_credit
        and len(args.extra_credit) > 1
    ):
        warnings.warn(
            "--extra-credit enables all extra-credit tests; ignoring other extra-credit options."
        )

    if args.int_only and args.chapter < TACKY_OPT_CHAPTER:
        warnings.warn("Option --int-only has no impact on Part I & Part II tests")

    if args.no_coalescing and args.chapter < TACKY_OPT_CHAPTER:
        warnings.warn("Option --no-coalescing has no impact on Part I & Part II tests")

    if args.expected_error_codes:

        out_of_range = [str(i) for i in args.expected_error_codes if i < 1 or i > 255]
        if out_of_range:
            bad_codes = ", ".join(out_of_range)
            s = "s" if len(out_of_range) > 1 else ""
            msg = f"Invalid argument{s} to --expected-error-codes: {bad_codes}. Invalid exit codes must be between 1 and 255."
            parser.error(msg)

    return args


def check_setup() -> bool:
    """Make sure system requirements are met

    Print a message and return True on success, False on failure
    """

    # Don't need to check Python version, we do this at very start of script

    # use this to track issues that we should report on but continue with validation
    issues: List[str] = []

    # Check OS and architecture
    machine = platform.machine().lower()
    system = platform.system()

    VALID_ARCHS: List[str] = ["x86_64", "amd64"]  # two names for the same arch

    # macOS: make sure they're running on x86-64; if they're on ARM, prompt to use Rosetta
    if system == "Darwin":
        if machine in VALID_ARCHS:
            # we're on an x86-64 machine (or running an x86-64 Python binary), so far so good
            pass

        elif machine == "arm64":
            # we're on an ARM64 machine
            # if Python reports that machine is arm64 but processor is i386,
            # that means we're running under Rosetta2
            # (see https://github.com/python/cpython/issues/96993)
            if platform.processor().lower() != "i386":
                issues.append(
                    """You're running macOS on ARM. You need to use Rosetta to emulate x86-64.
Use this command to open an x86-64 shell:
 arch -x86_64 zsh
Then try running this script again from that shell.
"""
                )

        else:
            # We're running some other (very old) architecture, we can't run x86-64 binar
            print(
                f"This architecture isn't supported. (Machine name is {machine}, we need x86_64/AMD64.)"
            )
            return False

    # on non-macOS systems, arch MUST be x86-64, otherwise this will not work
    elif machine not in VALID_ARCHS:
        print(
            f"This architecture isn't supported. (Machine name is {machine}, we need x86_64/AMD64.)"
        )
        return False

    elif system == "Windows":
        # the architecture is right but they need to use WSL
        print(
            """You're running Windows. You need to use WSL to emulate Linux.
Follow these instructions to install WSL and set up a Linux distribution on your machine: https://learn.microsoft.com/en-us/windows/wsl/install.
Then clone the test suite in your Linux distribution and try this command again from there.
            """
        )
        return False

    elif system not in ["Linux", "FreeBSD"]:
        # This is probably some other Unix-like system; it'll probably work but I haven't tested it
        issues.append(
            "This OS isn't officially supported. You might be able to complete the project on this system, but no guarantees."
        )

    # Check that GCC command is present
    try:
        subprocess.run(["gcc", "-v"], check=True, capture_output=True)
    except FileNotFoundError:
        msg = "Can't find the 'gcc' command. "
        if system == "Darwin":
            msg = (
                msg
                + """This command is included in the Xcode command-line developer tools. To install them, run:
 clang -v
Then try this command again.
"""
            )
        else:
            msg = (
                msg
                + "Use your system's package manager to install GCC, then try this command again."
            )
        issues.append(msg)

    # Check that GDB or LLDB is present
    try:
        subprocess.run(["gdb", "-v"], check=True, capture_output=True)
    except FileNotFoundError:
        try:
            # gdb isn't installed, try lldb
            subprocess.run(["lldb", "-v"], check=True, capture_output=True)
        except FileNotFoundError:
            # neither is installed
            msg = "No debugger found. The test script doesn't require a debugger but you probably want one for, ya know, debugging. "
            # TODO refactor
            if system == "Darwin":
                msg = (
                    msg
                    + """LLDB is included in the Xcode command-line developer tools. To install them, run:
                    clang -v
                Then try this command again."""
                )
            else:
                msg = (
                    msg
                    + "\nUse your system's package manager to install GDB, then try this command again."
                )
            issues.append(msg)

    if issues:
        print("\n\n".join(issues))
        return False

    print("All system requirements met!")
    return True


def is_valid_test_case(failure_case: unittest.TestCase) -> bool:
    invalid_dirs = test_framework.basic.dirs["invalid"]
    # if the test name (which includes path to the file under test) contains the name
    # of any invalid subdirectory, the program under test is invalid.
    if any(dir + "/" in failure_case.id() for dir in invalid_dirs):
        return False
    return True


def gen_assembly(failure_case: test_framework.basic.TestChapter) -> None:
    """Recompile failed test with -S option to generate assembly"""
    # HACK: work backwards from test method name to determine name of file under test
    # given fully qualified test name (e.g.
    # test_framework.basic.TestChapter13.test_valid/special_values/infinity),
    # get name of test method (e.g. test_valid/special_values/infinity)
    test_method_name = failure_case.id().split(".")[-1]
    # now remove "test_" prefix and add ".c" suffix to get e.g. valid/special_values/infinity.c
    # (don't use removeprefix to support Python 3.8)
    relative_src_path = (test_method_name[len("test_") :]) + ".c"
    # finally, get absolute path to file under test
    absolute_src_path = (failure_case.test_dir / relative_src_path).with_suffix(".c")
    # compile it with -S option (note that we don't need -lm or -c b/c we stop before assembly/linking)
    # if compilation fails, don't raise an error or print out stdout/stderr; we've already
    # reported that issue during test run
    compiler_args = [failure_case.cc] + failure_case.options + ["-S", absolute_src_path]
    subprocess.run(compiler_args, check=False, text=True, capture_output=True)


def main() -> int:
    """Main entry point for test runner"""
    args = parse_arguments()
    if args.check_setup:
        return check_setup()

    compiler = Path(args.cc).resolve()

    # merge list of extra-credit features into bitvector

    if args.extra_credit is not None:
        extra_credit: ExtraCredit = reduce(ior, args.extra_credit)
    else:
        extra_credit = ExtraCredit.NONE

    if args.latest_only:
        chapters: Iterable[int] = [args.chapter]
    elif args.int_only:
        # skip Part II chapters (11 - 18)
        chapters = itertools.chain(
            range(1, 11), range(TACKY_OPT_CHAPTER, args.chapter + 1)
        )
    else:
        chapters = range(1, args.chapter + 1)

    # construct options to pass to compiler under test
    # including optimizations and options to stop after a particular stage
    cc_options: list[str] = args.extra_cc_options
    optimization_flags = get_optimization_flags(args.chapter, args.optimization)
    cc_options.extend(optimization_flags)

    # create a subclass of TestChapter for each chapter,
    # dynamically adding a test case for each source program
    # technique adapted from
    # https://eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases
    test_suite = unittest.TestSuite()

    for chapter in chapters:
        test_class: Type[unittest.TestCase]
        if chapter < TACKY_OPT_CHAPTER:
            # Part I & II tests of new language features
            test_class = test_framework.basic.build_test_class(
                compiler,
                chapter,
                options=cc_options,
                stage=args.stage,
                extra_credit_flags=extra_credit,
                skip_invalid=args.skip_invalid,
                error_codes=args.expected_error_codes,
            )
            test_instance = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
            test_suite.addTest(test_instance)
        elif chapter == TACKY_OPT_CHAPTER:
            # for TACKY optimizations we build one test class per optimization
            test_classes = test_framework.tacky.suite.build_tacky_test_suite(
                compiler,
                args.optimization,
                options=cc_options,
                int_only=args.int_only,
                extra_credit_flags=extra_credit,
            )
            for tc in test_classes:
                test_instance = unittest.defaultTestLoader.loadTestsFromTestCase(tc)
                test_suite.addTest(test_instance)
        elif chapter == REGALLOC_CHAPTER:
            # register allocation tests
            test_framework.regalloc.configure_tests(
                compiler, cc_options, extra_credit, args.int_only, args.no_coalescing
            )
            test_instance = unittest.defaultTestLoader.loadTestsFromTestCase(
                test_framework.regalloc.TestRegAlloc
            )
            test_suite.addTest(test_instance)
        else:
            raise ValueError(f"There is no chapter {chapter}!")

    # handle ctrl-C cleanly
    unittest.installHandler()

    # run it
    runner = unittest.TextTestRunner(verbosity=args.verbose, failfast=args.failfast)
    result = runner.run(test_suite)
    if result.wasSuccessful():
        return 0

    if args.keep_asm_on_failure and args.stage == "run":
        for failure_case, _ in result.failures:
            assert isinstance(
                failure_case, test_framework.basic.TestChapter
            )  # placate mypy
            # no point in trying to emit assembly for invalid test programs,
            # since the compiler is supposed to fail before assembly generation
            if is_valid_test_case(failure_case):
                gen_assembly(failure_case)

    return 1
