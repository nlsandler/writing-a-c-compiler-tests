"""Make sure all valid test programs are well-defined and expected_results.json is up to date"""

import itertools
import subprocess
import unittest
from pathlib import Path
from typing import Callable, List, Iterable, Union

from .. import basic, regalloc


def build_compiler_args(source_file: Path) -> List[str]:
    """Given a source file, build the list of files/extra options we need for standalone compilation"""
    args = [str(source_file)]
    needs_mathlib = basic.needs_mathlib(source_file)

    # if this is a library, also compile client
    if "libraries" in source_file.parts and not source_file.name.endswith("_client.c"):
        client_name = source_file.name.replace(".c", "_client.c")
        client_path = source_file.with_name(client_name)
        args.append(str(client_path))
        needs_mathlib |= basic.needs_mathlib(client_path)

    # if it's in chapter 20, get extra libs as needed
    if (
        "chapter_20" in source_file.parts
        and source_file.name in regalloc.REGALLOC_TESTS
    ):
        # we may need to include wrapper script
        args.append(str(regalloc.WRAPPER_SCRIPT))

    # some test programs have extra libraries too
    args.extend(str(lib) for lib in basic.get_libs(source_file))

    # add mathlib option if needed
    if needs_mathlib:
        args.append("-lm")

    args.extend(["-o", str(source_file.with_suffix(""))])

    return args


class SanitizerTest(unittest.TestCase):
    def compile_and_run_sanitized(self, source_file: Path) -> None:
        """Make sure aggressive compiler warnings and UBSan don't complain about this program"""

        key = basic.get_props_key(source_file)

        # TODO run other sanitizers too?
        subproc_args = [
            "clang",
            # turn on all the warnings
            "-Wall",
            "-Wextra",
            "-Werror",
            "-pedantic",
            # now turn off some of them
            "-Wno-newline-eof",  # TODO just fix this?
            # macro to include warning suppression pragmas in individual source files
            "-D",
            "SUPPRESS_WARNINGS",
            # don't complain if there's an unknown warning option - it might have been added in a later version of clang
            "-Wno-unknown-warning-option",
            # enable ubsan, and enable optimizations so UBSan can catch more errors
            "-O3",
            "-fsanitize=undefined",
        ]
        subproc_args.extend(build_compiler_args(source_file))

        # compile it
        try:
            subprocess.run(subproc_args, check=True, text=True, capture_output=True)
        except subprocess.CalledProcessError as err:
            # This is an internal error in the test suite
            # TODO better handling of internal problems with test suite
            self.fail(f"Compilation fail with error output: {err.stderr}")

        # run it
        proc = subprocess.run(
            [source_file.with_suffix("")], capture_output=True, text=True, check=False
        )

        # make sure there's nothing on standard error - this may be a ubsan problem
        # tests never write to stderr deliberately
        self.assertFalse(
            proc.stderr, msg=f"Test program wrote to stderr: {proc.stderr}"
        )

        # make sure return code and stdout in expected_results.json are accurate
        self.assertEqual(proc.returncode, basic.EXPECTED_RESULTS[key]["return_code"])
        self.assertEqual(proc.stdout, basic.EXPECTED_RESULTS[key].get("stdout", ""))

    def tearDown(self) -> None:
        """Delete executable files produced during this test run"""
        garbage_files = (
            f
            for f in basic.TEST_DIR.rglob("*")
            if not f.is_dir() and f.suffix not in [".c", ".h", ".s", ".md"]
        )

        for junk in garbage_files:
            junk.unlink()


def make_sanitize_test(program: Path) -> Callable[[SanitizerTest], None]:
    """Generate sanitizer test method for one test program"""

    def test(self: SanitizerTest) -> None:
        self.compile_and_run_sanitized(program)

    return test


def configure_tests() -> None:
    valid_progs = itertools.chain(
        basic.TEST_DIR.glob("chapter_*/valid/**/*.c"),
        basic.TEST_DIR.glob("chapter_19/**/*.c"),
        basic.TEST_DIR.glob("chapter_20/all_types/**/*.c"),
        basic.TEST_DIR.glob("chapter_20/int_only/**/*.c"),
    )
    for prog in valid_progs:
        if prog.name.endswith("_client.c") or "helper_libs" in prog.parts:
            continue
        # TODO refactor getting the key/test name
        test_key = prog.relative_to(basic.TEST_DIR).with_suffix("")
        test_name = f"test_{test_key}"
        assert not getattr(
            SanitizerTest, test_name, None
        )  # sanity check - no duplicate tests
        setattr(SanitizerTest, test_name, make_sanitize_test(prog))


def load_tests(
    loader: unittest.TestLoader,
    tests: Iterable[Union[unittest.TestCase, unittest.TestSuite]],
    pattern: str,
) -> unittest.TestSuite:
    suite = unittest.TestSuite()
    configure_tests()
    tests = loader.loadTestsFromTestCase(SanitizerTest)
    suite.addTests(tests)
    return suite
