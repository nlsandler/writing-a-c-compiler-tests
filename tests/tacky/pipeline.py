"""Tests for whole compiler pipeline"""

from pathlib import Path
from typing import Callable

from . import common


class TestWholePipeline(common.TackyOptimizationTest):
    """Test cases for whole pipeline
    Run tests in whole_pipeline subdirectory but use same logic as dead store elimination tests.
    """

    test_dir = common.TEST_DIR / "whole_pipeline"


RETVAL_TESTS = {"dead_condition.c": 10, "elim_and_copy_prop.c": 10, "remainder_test": 1}
STORE_ELIMINATED = {"alias_analysis_change.c": [5, 10]}


def make_whole_pipeline_test(program: Path) -> Callable[[TestWholePipeline], None]:
    if program.name in RETVAL_TESTS:
        expected_retval = RETVAL_TESTS[program.name]

        def test(self: TestWholePipeline) -> None:
            self.return_const_test(source_file=program, returned_const=expected_retval)

    elif program.name in STORE_ELIMINATED:
        consts = STORE_ELIMINATED[program.name]

        def test(self: TestWholePipeline) -> None:
            self.store_eliminated_test(source_file=program, redundant_consts=consts)

    else:
        raise RuntimeError(f"Don't know what to do with {program.name}")

    return test
