"""Tests of top-level test run script"""
from __future__ import annotations
import re
import shutil
import subprocess
import unittest
from pathlib import Path
from typing import Union

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
        expected_test_count = len(list((ROOT_DIR / "chapter2").rglob("*.c")))
        try:
            testrun = run_test_script(
                "./test_compiler scripts/gcc_wrapper.py --chapter 2 --latest-only"
            )
        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")

        actual_test_count = get_test_count(testrun)
        self.assertEqual(expected_test_count, actual_test_count)

    def test_multiple_chapters_intermediate(self) -> None:
        expected_test_count = len(list((ROOT_DIR / "chapter1").rglob("*.c"))) + len(
            list((ROOT_DIR / "chapter2").rglob("*.c"))
        )
        try:
            testrun = run_test_script(
                "./test_compiler scripts/gcc_wrapper.py --chapter 2 --stage parse"
            )
        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")

        actual_test_count = get_test_count(testrun)
        self.assertEqual(expected_test_count, actual_test_count)

    def test_optimization_failure(self) -> None:
        """Without optimizations, GCC fails some chapter 19 tests"""
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
                "./test_compiler scripts/gcc_wrapper.py --chapter 19 --eliminate-dead-stores --latest-only"
            )
        failure_count = get_failure_count(err.exception)
        test_count = get_test_count(err.exception)
        self.assertEqual(expected_failure_count, failure_count)
        self.assertEqual(expected_test_count, test_count)

    def test_optimization_success(self) -> None:
        """With optimizations, GCC passes the chapter 19 tests"""
        expected_test_count = len(list((ROOT_DIR / "chapter19").rglob("*.c")))
        # the -O option will be passed through to GCC
        try:
            testrun = run_test_script(
                "./test_compiler scripts/gcc_wrapper.py --chapter 19 --latest-only -f -- -O"
            )

        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")
        actual_test_count = get_test_count(testrun)
        self.assertEqual(expected_test_count, actual_test_count)


class BadSourceTest(unittest.TestCase):
    def setUp(self) -> None:
        ret2 = ROOT_DIR / "chapter1/valid/return_2.c"
        ret0 = ROOT_DIR / "chapter1/valid/return_0.c"
        shutil.copy(ret2, ret0)

    def tearDown(self) -> None:
        subprocess.run(
            "git checkout chapter1", shell=True, check=True, capture_output=True
        )

    def test_bad_retval(self) -> None:
        """Make sure the test fails if retval is different than expected"""

        expected_test_count = len(list((ROOT_DIR / "chapter1").rglob("*.c")))
        with self.assertRaises(subprocess.CalledProcessError) as cpe:
            run_test_script("./test_compiler scripts/gcc_wrapper.py --chapter 1")
        actual_test_count = get_test_count(cpe.exception)
        failure_count = get_failure_count(cpe.exception)
        self.assertEqual(actual_test_count, expected_test_count)
        self.assertEqual(1, failure_count)

    def test_intermediate(self) -> None:
        """Changed code shouldn't impact intermediate stages"""
        expected_test_count = len(list((ROOT_DIR / "chapter1").rglob("*.c")))
        try:
            testrun = run_test_script(
                "./test_compiler scripts/gcc_wrapper.py --chapter 1 --stage parse"
            )
        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")

        actual_test_count = get_test_count(testrun)
        self.assertEqual(expected_test_count, actual_test_count)
