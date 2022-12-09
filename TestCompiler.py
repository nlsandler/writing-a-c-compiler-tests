
"""Entry point for test script"""
import argparse

from functools import reduce
from operator import ior
from typing import Type, Optional
from pathlib import Path
import unittest

import tests
from tests.Chapter20 import Optimizations
from tests.TestBase import ExtraCredit




def get_optimization_flags(latest_chapter: int, optimization_opt: Optional[Optimizations]) -> list[str]:

    if optimization_opt is None:
        if latest_chapter < 20:
            # don't enable optimizations
            return []
        # otherwise, default to enabling all optimizations
        return ["--fold-constants", "--eliminate-unreachable-code", "--propagate-copies", "--eliminate-dead-stores"]

    # we enable optimizations cumulatively
    # you can test each one in isolation by passing them as extra compiler arguments
    if latest_chapter > 20:
        raise ValueError(f"Option {optimization_opt} is incompatible with chapter 21 tests. All TACKY optimizations must be enabled.")

    if optimization_opt == Optimizations.CONSTANT_FOLD:
        return ["--fold-constants"]
    if optimization_opt == Optimizations.UNREACHABLE_CODE_ELIM:
        return ["--fold-constants", "--eliminate-unreachable-code"]
    if optimization_opt == Optimizations.COPY_PROP:
        return ["--fold-constants", "--eliminate-unreachable-code", "--propagate-copies"]
    if optimization_opt == Optimizations.DEAD_STORE_ELIM:
        return ["--fold-constants", "--eliminate-unreachable-code", "--propagate-copies", "--eliminate-dead-stores"]
    
    # we got an unrecognizeable option (or ALL, which should never be passed to this function)
    raise NotImplementedError(f"Don't know how to handle option {optimization_opt}")


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
    # optimization tests
    optimize_opts = parser.add_mutually_exclusive_group()
    optimize_opts.add_argument('--fold-constants', action='store_const', dest="optimization",
                               const=Optimizations.CONSTANT_FOLD, help='Enable constant folding, and run constant folding tests in chapter 20')
    optimize_opts.add_argument('--eliminate-unreachable-code', action='store_const', dest="optimization",
                               const=Optimizations.UNREACHABLE_CODE_ELIM, help="Enable constant folding and unreachable code elimination; run unreachable code elimination tests in chapter 20"
                               )
    optimize_opts.add_argument('--propagate-copies', action='store_const', dest="optimization", const=Optimizations.COPY_PROP,
                               help="Enable constant folding, unreachable code elimination, and copy propagation")
    optimize_opts.add_argument('--eliminate-dead-stores', action='store_const', dest="optimization",
                               const=Optimizations.DEAD_STORE_ELIM, help="Enable all four optimizations")
    parser.add_argument("--int-only", action="store_true",
                        help="Only run optimization tests that use Part I language features")
    parser.add_argument("--no-coalescing", action="store_true", help="Run register allocation tests that don't rely on coalescing")
    # extra args to pass through to compiler, should be followed by --
    parser.add_argument("extra_cc_options", type=str, nargs="*")
    return parser.parse_intermixed_args()


def main() -> None:
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
    cc_options = args.extra_cc_options
    optimization_flags = get_optimization_flags(args.chapter, args.optimization)
    cc_options.extend(optimization_flags)

    # create a subclass of TestChapter for each chapter,
    # dynamically adding a test case for each source program

    test_suite = unittest.TestSuite()

    for chapter in chapters:
        test_class: Type[unittest.TestCase]
        if chapter < 20:
            test_class = tests.build_test_class(chapter, compiler, cc_options, stage, extra_credit, args.skip_invalid)
            test_instance = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
            test_suite.addTest(test_instance)
        elif chapter == 20:
            test_classes = tests.Chapter20.build_test_suite(compiler, cc_options, extra_credit, args.optimization, args.int_only)
            for tc in test_classes:
                test_instance = unittest.defaultTestLoader.loadTestsFromTestCase(tc)
                test_suite.addTest(test_instance)
        elif chapter == 21:
            test_class = tests.build_chapter_21_test_class(compiler, cc_options, extra_credit, args.int_only, args.no_coalescing)
            test_instance = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
            test_suite.addTest(test_instance)
        else:
            raise ValueError(f"There is no chapter {chapter}!")

    # handle ctrl-C cleanly
    unittest.installHandler()
    runner = unittest.TextTestRunner(
        verbosity=args.verbose, failfast=args.failfast)
    runner.run(test_suite)
