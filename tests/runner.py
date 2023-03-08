"""Argument parsing and main entry point for test script"""

from __future__ import annotations

import argparse
import unittest
import warnings
from functools import reduce
from operator import ior
from pathlib import Path
from typing import Iterable, Optional, Type

import tests
import tests.regalloc
import tests.tacky.suite
from tests.basic import ExtraCredit
from tests.regalloc import CHAPTER as REGALLOC_CHAPTER
from tests.tacky.common import CHAPTER as TACKY_OPT_CHAPTER
from tests.tacky.suite import Optimizations


def get_optimization_flags(
    latest_chapter: int, optimization_opt: Optional[tests.tacky.suite.Optimizations]
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
    # required arguments
    parser.add_argument("cc", type=str, help="Path to your compiler")
    parser.add_argument(
        "--chapter",
        type=int,
        choices=range(0, REGALLOC_CHAPTER + 1),
        required=True,
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
        "--stage", type=str, choices=["lex", "parse", "validate", "tacky", "codegen"]
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
        action="store_const",
        const=ExtraCredit.NAN,
        dest="append_const",
        help="Include tests for floating-point NaN",
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
    if args.stage and args.chapter >= TACKY_OPT_CHAPTER:
        # TODO better error message here
        parser.error(
            message=f"Option --stage not allowed with Part III tests (chapter {args.chapter})",
        )

    if (
        args.extra_credit
        and ExtraCredit.ALL in args.extra_credit
        and len(args.extra_credit) > 1
    ):
        warnings.warn(
            "--extra-credit enables all extra-credit tests; ignoring other extra-credit options."
        )

    if args.int_only and (Optimizations.UNREACHABLE_CODE_ELIM == args.optimization):
        warnings.warn("--int-only has no effect on unreachable code elimination tests")

    if args.int_only and args.chapter < TACKY_OPT_CHAPTER:
        warnings.warn("Option --int-only has no impact on Part I & Part II tests")

    if args.no_coalescing and args.chapter < TACKY_OPT_CHAPTER:
        warnings.warn("Option --no-coalescing has no impact on Part I & Part II tests")

    return args


def main() -> int:
    """Main entry point for test runner"""
    args = parse_arguments()
    compiler = Path(args.cc).resolve()

    # merge list of extra-credit features into bitvector

    if args.extra_credit is not None:
        extra_credit: ExtraCredit = reduce(ior, args.extra_credit)
    else:
        extra_credit = ExtraCredit.NONE

    if args.latest_only:
        chapters: Iterable[int] = [args.chapter]
    else:
        chapters = range(1, args.chapter + 1)

    # construct options to pass to compiler under test
    # including optimizations and options to stop after a particular stage
    stage: str = args.stage or "run"  # by default, compile and run the program
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
            test_class = tests.basic.build_test_class(
                compiler,
                chapter,
                options=cc_options,
                stage=stage,
                extra_credit_flags=extra_credit,
                skip_invalid=args.skip_invalid,
            )
            test_instance = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
            test_suite.addTest(test_instance)
        elif chapter == TACKY_OPT_CHAPTER:
            # for TACKY optimizations we build one test class per optimization
            test_classes = tests.tacky.suite.build_tacky_test_suite(
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
            tests.regalloc.configure_tests(
                compiler, cc_options, extra_credit, args.int_only, args.no_coalescing
            )
            test_instance = unittest.defaultTestLoader.loadTestsFromTestCase(
                tests.regalloc.TestRegAlloc
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
    return 1
