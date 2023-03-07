"""Tests for TACKY optimizations."""
from __future__ import annotations

from enum import Enum, auto, unique
from pathlib import Path
from typing import List

from .. import basic
from . import common, const_fold, copy_prop, dead_store_elim, unreachable

TEST_DIR = Path(__file__).parent.parent.joinpath("chapter19").resolve()


@unique
class Optimizations(Enum):
    """Which TACKY optimizations to test"""

    CONSTANT_FOLD = auto()
    UNREACHABLE_CODE_ELIM = auto()
    COPY_PROP = auto()
    DEAD_STORE_ELIM = auto()
    ALL = auto()


def build_tacky_test_suite(
    compiler: Path,
    optimization_under_test: Optimizations,
    *,
    options: list[str],
    int_only: bool,
    extra_credit_flags: basic.ExtraCredit,
) -> List[type[common.TackyOptimizationTest]]:
    """Collect test classes for TACKY optimizations.

    We use a different subclass of OptimizationTest for each of our four TACKY optimizations.
    If we're only testing one optimization, we'll use one subclass; if we're testing the whole
    optimization pipeline we'll use all four. We'll configure each subclass by defining
    a few attributes (e.g. the path to the compiler under test) and generating a test
    method for each C program in the target optimization's test suite.

    Args:
        compiler: absolute path to compiler under test
        optimization_under_test: which optimization(s) to test
        options: extra command-line options to pass through to compiler
                 (including optimization flags)
        int_only: True if we're skipping tests that use Part II features, False if we're
                  including them
        extra_credit_flags:  extra credit features to test, represented as a bit vector
    Returns:
        a list of subclasses of OptimizationTest
    """

    common_testclass_attrs = {
        "cc": compiler,
        "options": options,
        "exit_stage": None,
    }

    # TODO whole pipline tests!
    # TODO refactor configure_tests from different moduels, they're basically identical

    if optimization_under_test is None or optimization_under_test == Optimizations.ALL:
        # testing the whole pipeline; return all four classes
        const_fold.configure_tests(common_testclass_attrs, extra_credit_flags, int_only)
        unreachable.configure_tests(common_testclass_attrs, extra_credit_flags)
        copy_prop.configure_tests(common_testclass_attrs, extra_credit_flags, int_only)
        dead_store_elim.configure_tests(
            common_testclass_attrs, extra_credit_flags, int_only
        )
        return [
            const_fold.TestConstantFolding,
            unreachable.TestUnreachableCodeElim,
            copy_prop.TestCopyProp,
            dead_store_elim.TestDeadStoreElimination,
        ]

    # otherwise we're only testing one optimiztion; generate tests for the appropriate class
    if optimization_under_test == Optimizations.CONSTANT_FOLD:

        # add tests to TestConstantFolding class
        const_fold.configure_tests(common_testclass_attrs, extra_credit_flags, int_only)
        return [const_fold.TestConstantFolding]

    if optimization_under_test == Optimizations.UNREACHABLE_CODE_ELIM:
        # this test suite doesn't include Part II-specific tests, so don't need int_only arg
        unreachable.configure_tests(common_testclass_attrs, extra_credit_flags)
        return [unreachable.TestUnreachableCodeElim]
    if optimization_under_test == Optimizations.COPY_PROP:
        copy_prop.configure_tests(common_testclass_attrs, extra_credit_flags, int_only)
        return [copy_prop.TestCopyProp]
    if optimization_under_test == Optimizations.DEAD_STORE_ELIM:
        dead_store_elim.configure_tests(
            common_testclass_attrs, extra_credit_flags, int_only
        )
        return [dead_store_elim.TestDeadStoreElimination]
    raise ValueError(f"Unknown optimization {optimization_under_test}")
