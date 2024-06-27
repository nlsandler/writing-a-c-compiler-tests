"""Tests for TACKY optimizations."""

from __future__ import annotations

import itertools
from enum import Enum, auto, unique
from pathlib import Path
from typing import Callable, Iterable, List, Type, TypeVar

from .. import basic
from . import common, const_fold, copy_prop, dead_store_elim, pipeline, unreachable

TEST_DIR = Path(__file__).parent.parent.joinpath("chapter_19").resolve()


@unique
class Optimizations(Enum):
    """Which TACKY optimizations to test"""

    CONSTANT_FOLD = auto()
    UNREACHABLE_CODE_ELIM = auto()
    COPY_PROP = auto()
    DEAD_STORE_ELIM = auto()
    ALL = auto()


T = TypeVar("T", bound=common.TackyOptimizationTest)


def configure_tests(
    cls: Type[T],
    test_maker: Callable[[Path], Callable[[T], None]],
    compiler: Path,
    options: list[str],
    int_only: bool,
    extra_credit_flags: basic.ExtraCredit,
) -> None:
    """Dynamically add test methods and attributes to one of the optimization test classes.

    Args:
        cls: the test class to configure
        test_maker: a function that takes the path to a source program and returns a test method
                    validating that we process that program correctly
        compiler: absolute path to the compiler under test
        options: extra command-line options to pass through to compiler
                 (including optimization flags)
        int_only: True if we're skipping tests that use Part II features, False if we're
                  including them
        extra_credit_flags:  extra credit features to test, represented as a bit vector
    """

    setattr(cls, "cc", compiler)
    setattr(cls, "options", options)
    setattr(cls, "exit_stage", None)

    tests: Iterable[Path]
    if cls == unreachable.TestUnreachableCodeElim:
        # no distinction b/t int_only and all_types
        tests = cls.test_dir.rglob("*.c")
    else:
        tests = (cls.test_dir / "int_only").rglob("*.c")
        if not int_only:
            partii_tests = (cls.test_dir / "all_types").rglob("*.c")
            tests = itertools.chain(tests, partii_tests)

    for program in tests:
        if basic.excluded_extra_credit(program, extra_credit_flags):
            continue
        key = program.relative_to(cls.test_dir).with_suffix("")
        name = f"test_{key}"
        assert not getattr(cls, name, None)  # sanity check - no duplicate tests
        setattr(cls, name, test_maker(program))


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

    if optimization_under_test is None or optimization_under_test == Optimizations.ALL:
        # testing the whole pipeline; return all four classes
        configure_tests(
            const_fold.TestConstantFolding,
            const_fold.make_constant_fold_test,
            compiler,
            options,
            int_only,
            extra_credit_flags,
        )
        configure_tests(
            unreachable.TestUnreachableCodeElim,
            unreachable.make_unreachable_code_test,
            compiler,
            options,
            int_only,
            extra_credit_flags,
        )
        configure_tests(
            copy_prop.TestCopyProp,
            copy_prop.make_copy_prop_test,
            compiler,
            options,
            int_only,
            extra_credit_flags,
        )
        configure_tests(
            dead_store_elim.TestDeadStoreElimination,
            dead_store_elim.make_dse_test,
            compiler,
            options,
            int_only,
            extra_credit_flags,
        )

        configure_tests(
            pipeline.TestWholePipeline,
            pipeline.make_whole_pipeline_test,
            compiler,
            options,
            int_only,
            extra_credit_flags,
        )
        return [
            const_fold.TestConstantFolding,
            unreachable.TestUnreachableCodeElim,
            copy_prop.TestCopyProp,
            dead_store_elim.TestDeadStoreElimination,
            pipeline.TestWholePipeline,
        ]

    # otherwise we're only testing one optimiztion; generate tests for the appropriate class
    if optimization_under_test == Optimizations.CONSTANT_FOLD:
        # add tests to TestConstantFolding class
        configure_tests(
            const_fold.TestConstantFolding,
            const_fold.make_constant_fold_test,
            compiler,
            options,
            int_only,
            extra_credit_flags,
        )
        return [const_fold.TestConstantFolding]

    if optimization_under_test == Optimizations.UNREACHABLE_CODE_ELIM:
        # this test suite doesn't include Part II-specific tests, so don't need int_only arg
        configure_tests(
            unreachable.TestUnreachableCodeElim,
            unreachable.make_unreachable_code_test,
            compiler,
            options,
            int_only,
            extra_credit_flags,
        )
        return [unreachable.TestUnreachableCodeElim]
    if optimization_under_test == Optimizations.COPY_PROP:
        configure_tests(
            copy_prop.TestCopyProp,
            copy_prop.make_copy_prop_test,
            compiler,
            options,
            int_only,
            extra_credit_flags,
        )
        return [copy_prop.TestCopyProp]
    if optimization_under_test == Optimizations.DEAD_STORE_ELIM:
        configure_tests(
            dead_store_elim.TestDeadStoreElimination,
            dead_store_elim.make_dse_test,
            compiler,
            options,
            int_only,
            extra_credit_flags,
        )
        return [dead_store_elim.TestDeadStoreElimination]
    raise ValueError(f"Unknown optimization {optimization_under_test}")
