"""Tests of top-level test run script
These assume we have access to two copies of the reference implementation:
- $$NQCC is the path to the fully implemented compiler
- $$NQCC_PARTIAL is a path to version of the compiler that is implemented
  through the unreachable code elimination stage in chapter 19,
  but doesn't include dead code elimination or register allocation
"""
from __future__ import annotations

import re
import shutil
import subprocess
import unittest
from pathlib import Path
from typing import Union

from ..regalloc import REGALLOC_TESTS

ROOT_DIR = Path(__file__).parent.parent.parent
TEST_PATTERN = re.compile("^Ran ([0-9]+) tests", flags=re.MULTILINE)
FAILURE_PATTERN = re.compile("failures=([0-9]+)")


def run_test_script(cmd: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        shell=True,
        check=True,
        capture_output=True,
        text=True,
        cwd=str(ROOT_DIR),
    )


def get_test_count(
    testrun: Union[subprocess.CalledProcessError, subprocess.CompletedProcess[str]]
) -> int:
    run_output = re.search(TEST_PATTERN, testrun.stderr)
    if not run_output:
        raise RuntimeError(f"Unexpected test output: {testrun.stderr}")

    return int(run_output.group(1))


def get_failure_count(failure: subprocess.CalledProcessError) -> int:
    fail_output = re.search(FAILURE_PATTERN, failure.stderr)
    if not fail_output:
        raise RuntimeError(f"Unexpected test output: {failure.stderr}")

    return int(fail_output.group(1))


class TopLevelTest(unittest.TestCase):
    def test_one_chapter(self) -> None:
        """We can run tests for a single chapter with --latest-only"""
        expected_test_count = len(list((ROOT_DIR / "chapter2").rglob("*.c")))
        try:
            testrun = run_test_script("./test_compiler $NQCC --chapter 2 --latest-only")
        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")

        actual_test_count = get_test_count(testrun)
        self.assertEqual(expected_test_count, actual_test_count)

    def test_multiple_chapters_intermediate(self) -> None:
        """We can test through an intermediate stage through multiple chapters"""
        expected_test_count = len(list((ROOT_DIR / "chapter1").rglob("*.c"))) + len(
            list((ROOT_DIR / "chapter2").rglob("*.c"))
        )
        try:
            testrun = run_test_script("./test_compiler $NQCC --chapter 2 --stage parse")
        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")

        actual_test_count = get_test_count(testrun)
        self.assertEqual(expected_test_count, actual_test_count)

    def test_optimization_failure(self) -> None:
        """Partially-completed NQCC fails some optimization tests"""
        expected_test_count = len(
            list((ROOT_DIR / "chapter19/dead_store_elimination").rglob("*.c"))
        )

        # the tests in dont_elim just validate behavior without inspecting assembly
        expected_success_count = len(
            list(
                (ROOT_DIR / "chapter19/dead_store_elimination").rglob(
                    "dont_elim/**/*.c"
                )
            )
        )
        expected_failure_count = expected_test_count - expected_success_count
        with self.assertRaises(subprocess.CalledProcessError) as err:
            run_test_script(
                "./test_compiler $NQCC_PARTIAL --chapter 19 --eliminate-dead-stores --latest-only"
            )
        failure_count = get_failure_count(err.exception)
        test_count = get_test_count(err.exception)
        self.assertEqual(expected_failure_count, failure_count)
        self.assertEqual(expected_test_count, test_count)

    def test_regalloc_failure(self) -> None:
        """Partially-completed NQCC fails register allocation tests"""
        expected_test_count = len(
            list((ROOT_DIR / "chapter20/int_only").rglob("*.c"))
        ) + len(list((ROOT_DIR / "chapter20/all_types").rglob("*.c")))
        expected_failure_count = len(REGALLOC_TESTS.keys())
        with self.assertRaises(subprocess.CalledProcessError) as err:
            run_test_script("./test_compiler $NQCC_PARTIAL --chapter 20 --latest-only")
        failure_count = get_failure_count(err.exception)
        test_count = get_test_count(err.exception)
        self.assertEqual(expected_failure_count, failure_count)
        self.assertEqual(expected_test_count, test_count)

    def test_optimization_success(self) -> None:
        """With optimizations, NQCC passes the chapter 19 tests"""
        expected_test_count = len(list((ROOT_DIR / "chapter19").rglob("*.c")))
        try:
            testrun = run_test_script(
                "./test_compiler $NQCC --chapter 19 --latest-only"
            )

        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")
        actual_test_count = get_test_count(testrun)
        self.assertEqual(expected_test_count, actual_test_count)


class BadSourceTest(unittest.TestCase):
    def setUp(self) -> None:
        ret2 = ROOT_DIR / "chapter1/valid/return_2.c"
        ret0 = ROOT_DIR / "chapter1/valid/return_0.c"
        hello_world = ROOT_DIR / "chapter9/valid/arguments_in_registers/hello_world.c"
        shutil.copy(ret2, ret0)
        shutil.copy(ret0, hello_world)

    def tearDown(self) -> None:
        # TODO: save ret0 and hello-world to tmp files and restore them instead of using checkout here
        subprocess.run(
            "git checkout chapter1 chapter9",
            shell=True,
            check=True,
            capture_output=True,
        )

    def test_bad_retval(self) -> None:
        """Make sure the test fails if retval is different than expected"""

        expected_test_count = len(list((ROOT_DIR / "chapter1").rglob("*.c")))
        with self.assertRaises(subprocess.CalledProcessError) as cpe:
            run_test_script("./test_compiler $NQCC --chapter 1")
        actual_test_count = get_test_count(cpe.exception)
        failure_count = get_failure_count(cpe.exception)
        self.assertEqual(actual_test_count, expected_test_count)
        self.assertEqual(1, failure_count)

    def test_bad_stdout(self) -> None:
        """Make sure test fails if stdout is different than expected"""

        expected_test_count = len(list((ROOT_DIR / "chapter9").rglob("*.c"))) - len(
            list((ROOT_DIR / "chapter9").rglob("**/extra_credit/*.c"))
        )
        with self.assertRaises(subprocess.CalledProcessError) as cpe:
            run_test_script("./test_compiler $NQCC --chapter 9 --latest-only")
        actual_test_count = get_test_count(cpe.exception)
        failure_count = get_failure_count(cpe.exception)
        self.assertEqual(actual_test_count, expected_test_count)
        self.assertEqual(1, failure_count)

    def test_intermediate(self) -> None:
        """Changed code shouldn't impact intermediate stages"""
        expected_test_count = len(list((ROOT_DIR / "chapter1").rglob("*.c")))
        try:
            testrun = run_test_script("./test_compiler $NQCC --chapter 1 --stage parse")
        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")

        actual_test_count = get_test_count(testrun)
        self.assertEqual(expected_test_count, actual_test_count)
