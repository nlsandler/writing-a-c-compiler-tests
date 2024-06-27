"""Tests of top-level test run script
These assume we have access to two copies of the reference implementation:
- $$NQCC is the path to the fully implemented compiler
- $$NQCC_PARTIAL is a path to version of the compiler that is implemented
  through chapter 19 but doesn't include register allocation
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Union, Sequence


from ..regalloc import REGALLOC_TESTS
from ..basic import (
    ASSEMBLY_LIBS,
    EXPECTED_RESULTS,
    ROOT_DIR,
    TEST_DIR,
    excluded_extra_credit,
    ExtraCredit,
)
from ..tacky.dead_store_elim import STORE_ELIMINATED

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


def get_expected_test_count(
    chapters: Sequence[int], *, subdir: str = "", excluded_dirs: Sequence[str] = ()
) -> int:
    """Calculate the number of test programs in the specified chapters.
    Include invalid test programs, exclude extra credit tests.
    Args:
        * chapters: list of chapters to calculate test count for
        * subdir: subdirectory within chapter to get test count for (for chapter 19 tests)
        * excluded_dirs: list of directory names to exclude from count
            (used to exclude directories containing helper libraries, or all_types
            directories when running int-only tests)
    """

    def should_include(f: Path) -> bool:
        """Include a test file if it's not an extra-credit test or in any of excluded_dirs"""
        if any(excluded in f.parts for excluded in excluded_dirs):
            return False
        return not excluded_extra_credit(f, ExtraCredit.NONE)

    count = 0
    for i in chapters:
        chapter_dir = TEST_DIR / f"chapter_{i}"
        if subdir:
            chapter_dir = chapter_dir / subdir
        chapter_files = chapter_dir.rglob("*.c")
        count += sum(1 for f in chapter_files if should_include(f))

    return count


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
        expected_test_count = get_expected_test_count(chapters=[2])
        try:
            testrun = run_test_script("./test_compiler $NQCC --chapter 2 --latest-only")
        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")

        actual_test_count = get_test_count(testrun)
        self.assertEqual(expected_test_count, actual_test_count)

    def test_multiple_chapters_intermediate(self) -> None:
        """We can test through an intermediate stage through multiple chapters"""
        expected_test_count = len(list((TEST_DIR / "chapter_1").rglob("*.c"))) + len(
            list((TEST_DIR / "chapter_2").rglob("*.c"))
        )
        try:
            testrun = run_test_script("./test_compiler $NQCC --chapter 2 --stage parse")
        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")

        actual_test_count = get_test_count(testrun)
        self.assertEqual(expected_test_count, actual_test_count)

    def test_int_only_ch19(self) -> None:
        """The --int-only option excludes chapter 19 tests that rely on Part II features"""

        # expected tests include all tests in chapters 1 - 10, and all tests in int_only
        # subdirectories in chapter 19
        expected_test_count = get_expected_test_count(
            chapters=list(range(1, 11)) + [19],
            excluded_dirs=["all_types", "helper_libs"],
        )

        try:
            testrun = run_test_script("./test_compiler $NQCC --chapter 19 --int-only")
        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")

        actual_test_count = get_test_count(testrun)
        self.assertEqual(expected_test_count, actual_test_count)

    def test_int_only_ch20(self) -> None:
        """The --int-only option excludes chapter 20 tests that rely on Part II features"""
        # expected tests include all tests in chapters 1 - 10, and all tests in int_only
        # subdirectories in chapters 19 and 20
        expected_test_count = get_expected_test_count(
            chapters=list(range(1, 11))
        ) + get_expected_test_count(
            chapters=[19, 20],
            excluded_dirs=["all_types", "helper_libs", "libraries"],
        )

        try:
            testrun = run_test_script("./test_compiler $NQCC --chapter 20 --int-only")
        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")

        actual_test_count = get_test_count(testrun)
        self.assertEqual(expected_test_count, actual_test_count)

    def test_regalloc_failure(self) -> None:
        """Partially-completed NQCC fails register allocation tests"""
        expected_test_count = get_expected_test_count(
            chapters=[20], excluded_dirs=["libraries"]
        )

        expected_failure_count = len(REGALLOC_TESTS.keys())
        with self.assertRaises(subprocess.CalledProcessError) as err:
            run_test_script("./test_compiler $NQCC_PARTIAL --chapter 20 --latest-only")
        failure_count = get_failure_count(err.exception)
        test_count = get_test_count(err.exception)
        self.assertEqual(
            expected_failure_count,
            failure_count,
            msg=f"Expected {expected_failure_count} failures but got {failure_count}",
        )
        self.assertEqual(expected_test_count, test_count)

    def test_optimization_success(self) -> None:
        """With optimizations, NQCC passes the chapter 19 tests"""
        expected_test_count = get_expected_test_count(
            chapters=[19], excluded_dirs=["helper_libs"]
        )
        try:
            testrun = run_test_script(
                "./test_compiler $NQCC --chapter 19 --latest-only"
            )

        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")
        actual_test_count = get_test_count(testrun)
        self.assertEqual(expected_test_count, actual_test_count)

    def test_expected_error_code(self) -> None:
        """The --expected-error-codes option specifies expected error codes when compilation fails."""

        # NQCC throws error code 125 in all cases
        # This should succeed b/c it specifies the error code we'll actually throw
        try:
            testrun = run_test_script(
                "./test_compiler $NQCC --chapter 1 --expected-error-codes 125"
            )
        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")

        # Specify multiple error codes including the one we'll actually throw; this should also succeed
        try:
            testrun = run_test_script(
                "./test_compiler $NQCC --chapter 1 --expected-error-codes 125 127"
            )
        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")

        # Here all invalid tests should fail b/c we won't use the expected error code
        with self.assertRaises(subprocess.CalledProcessError) as expected_failure:
            run_test_script(
                "./test_compiler $NQCC --chapter 1 --expected-error-codes 127"
            )
        failure_count = get_failure_count(expected_failure.exception)
        expected_failure_count = len(
            list((TEST_DIR / "chapter_1").rglob("invalid_*/*.c"))
        )
        self.assertEqual(expected_failure_count, failure_count)


class BadSourceTest(unittest.TestCase):
    # paths that we'll refer to in setup/teardown
    ret2 = TEST_DIR / "chapter_1/valid/return_2.c"
    ret0 = TEST_DIR / "chapter_1/valid/return_0.c"
    hello_world = TEST_DIR / "chapter_9/valid/arguments_in_registers/hello_world.c"
    dse_relative = Path("chapter_19/dead_store_elimination/int_only/fig_19_11.c")
    dse = TEST_DIR / dse_relative

    # temporary directory - created in setup and removed in teardown
    tmpdir: tempfile.TemporaryDirectory[str]

    @classmethod
    def setUpClass(cls) -> None:
        # save these to a temporary directory before overwriting them
        cls.tmpdir = tempfile.TemporaryDirectory()
        shutil.copy(cls.hello_world, cls.tmpdir.name)
        shutil.copy(cls.ret0, cls.tmpdir.name)
        shutil.copy(cls.dse, cls.tmpdir.name)

        # overwrite hello_world with another file that has same retcode but different stdout
        shutil.copy(cls.ret0, cls.hello_world)

        # overwrite ret0 with another file with different retcode
        shutil.copy(cls.ret2, cls.ret0)

        # replace a dead store elimination test w/ a different program that has the same
        # result, but where the dead store can't be eliminated
        expected_retval = EXPECTED_RESULTS[str(cls.dse_relative)]["return_code"]
        store_to_elim = STORE_ELIMINATED[cls.dse.name]
        with open(
            TEST_DIR / "chapter_19/dead_store_elimination/int_only/fig_19_11.c",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(
                f"""
            int f(int arg) {{
                return arg;
            }}
            int target(void) {{
                int x = {store_to_elim};
                f(x);
                return {expected_retval};
            }}
            int main(void) {{ return target(); }}
            """
            )

    @classmethod
    def tearDownClass(cls) -> None:
        """Restore files we overwrote from temporary directory"""
        tmp_path = Path(cls.tmpdir.name)
        tmp_ret0 = tmp_path / cls.ret0.name
        tmp_helloworld = tmp_path / cls.hello_world.name
        tmp_dse = tmp_path / cls.dse.name

        shutil.copy(tmp_ret0, cls.ret0)
        shutil.copy(tmp_helloworld, cls.hello_world)
        shutil.copy(tmp_dse, cls.dse)
        cls.tmpdir.cleanup()

        # remove intermediate files produced by --keep-asm-on-failure
        for f in (TEST_DIR / f"chapter_1").rglob("*.s"):
            if f.name not in ASSEMBLY_LIBS:
                f.unlink(missing_ok=True)

    def assert_no_intermediate_files(self, chapter: int) -> None:
        # Executables, *.i files, etc should have been cleaned up
        intermediate_files = [
            str(f)
            for f in (TEST_DIR / f"chapter_{chapter}").rglob("*")
            if not f.is_dir()
            and f.suffix not in [".c", ".h", ".md"]
            and f.name not in ASSEMBLY_LIBS
        ]
        files_str = ", ".join(intermediate_files)
        self.assertFalse(
            intermediate_files,
            msg=f"Found intermediate files that should have been cleaned up: {files_str}",
        )

    def test_bad_retval(self) -> None:
        """Make sure the test fails if retval is different than expected"""

        expected_test_count = get_expected_test_count(chapters=[1])
        with self.assertRaises(subprocess.CalledProcessError) as cpe:
            run_test_script("./test_compiler $NQCC --chapter 1")
        actual_test_count = get_test_count(cpe.exception)
        failure_count = get_failure_count(cpe.exception)
        self.assertEqual(actual_test_count, expected_test_count)
        self.assertEqual(1, failure_count)
        self.assert_no_intermediate_files(1)

    def test_bad_stdout(self) -> None:
        """Make sure test fails if stdout is different than expected"""

        expected_test_count = get_expected_test_count(chapters=[9])
        with self.assertRaises(subprocess.CalledProcessError) as cpe:
            run_test_script("./test_compiler $NQCC --chapter 9 --latest-only")
        actual_test_count = get_test_count(cpe.exception)
        failure_count = get_failure_count(cpe.exception)
        self.assertEqual(actual_test_count, expected_test_count)
        self.assertEqual(1, failure_count)
        self.assert_no_intermediate_files(9)

    def test_optimization_failure(self) -> None:
        """Test fails if code hasn't been optimized as expected"""
        expected_test_count = get_expected_test_count(
            [19], subdir="dead_store_elimination"
        )

        with self.assertRaises(subprocess.CalledProcessError) as err:
            run_test_script(
                "./test_compiler $NQCC --chapter 19 --eliminate-dead-stores --latest-only"
            )
        failure_count = get_failure_count(err.exception)
        test_count = get_test_count(err.exception)
        self.assertEqual(
            1,
            failure_count,
            msg=f"Expected 1 failure but got {failure_count}",
        )
        self.assertEqual(expected_test_count, test_count)
        self.assert_no_intermediate_files(19)

    def test_intermediate(self) -> None:
        """Changed code shouldn't impact intermediate stages"""
        expected_test_count = get_expected_test_count(chapters=[1])

        try:
            testrun = run_test_script("./test_compiler $NQCC --chapter 1 --stage parse")
        except subprocess.CalledProcessError as err:
            self.fail(f"Test command failed with message {err.stderr}")

        actual_test_count = get_test_count(testrun)
        self.assertEqual(expected_test_count, actual_test_count)
        self.assert_no_intermediate_files(19)

    def test_keep_asm(self) -> None:
        """Use --keep-asm-on-failure option to generate assembly for failures"""
        with self.assertRaises(subprocess.CalledProcessError) as cpe:
            run_test_script("./test_compiler $NQCC --chapter 1")
        # make sure we preserved .s file for ret0, which should fail
        expected_asm = self.__class__.ret0.with_suffix(".s")
        self.assertTrue(
            expected_asm.exists,
            msg=f"{expected_asm} should be preserved on failure but wasn't found",
        )

    def test_keep_asm_optimize(self) -> None:
        """Make sure --keep-asm-on-failure works for chapter 19 tests"""
        with self.assertRaises(subprocess.CalledProcessError) as cpe:
            run_test_script("./test_compiler $NQCC --chapter 19")
        # make sure we preserved .s file for ret0, which should fail
        expected_asm = self.__class__.dse.with_suffix(".s")
        self.assertTrue(
            expected_asm.exists,
            msg=f"{expected_asm} should be preserved on failure but wasn't found",
        )
