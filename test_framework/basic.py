"""Basic tests for Parts I & II"""
from __future__ import annotations

import json
import platform
import subprocess
import sys
import unittest
from enum import Flag, auto, unique
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Type

# Constants + per-test info from configuration files
# TODO should this be in a separate module maybe?

ROOT_DIR = Path(__file__).parent.parent  # ROOT of test repo
TEST_DIR = ROOT_DIR / "tests"  # directory containing all test programs
IS_OSX = platform.system().lower() == "darwin"
EXPECTED_RESULTS: dict[str, Any]

with open(ROOT_DIR / "expected_results.json", "r", encoding="utf-8") as f:
    EXPECTED_RESULTS = json.load(f)

EXTRA_CREDIT_PROGRAMS: dict[str, List[str]]
REQUIRES_MATHLIB: List[str]

# TODO Consider handling C and assembly dependencies uniformly
# (but remember that assembly files have different Linux/OS X variants)
DEPENDENCIES: Dict[str, List[str]]
ASSEMBLY_DEPENDENCIES: Dict[str, List[str]]
with open(ROOT_DIR / "test_properties.json", "r", encoding="utf-8") as f:
    test_info = json.load(f)
    EXTRA_CREDIT_PROGRAMS = test_info["extra_credit_tests"]
    REQUIRES_MATHLIB = test_info["requires_mathlib"]
    ASSEMBLY_DEPENDENCIES = test_info["assembly_libs"]
    DEPENDENCIES = test_info["libs"]

MAC_SUFFIX = "_osx.s"
LINUX_SUFFIX = "_linux.s"
ASSEMBLY_LIBS = set(
    Path(platform_specific_lib).name
    for libs in ASSEMBLY_DEPENDENCIES.values()
    for lib in libs
    for platform_specific_lib in [lib + MAC_SUFFIX, lib + LINUX_SUFFIX]
)

# main TestChapter class + related utilities


def get_platform() -> str:
    if IS_OSX:
        return "os_x"
    else:
        return "linux"


def get_platform_suffix() -> str:
    if IS_OSX:
        return MAC_SUFFIX
    else:
        return LINUX_SUFFIX


def get_props_key(source_file: Path) -> str:
    """key to use in EXPECTED_RESULTS, REQUIRES_MATHLIB, EXTRA_CREDIT_PROGRAMS
    If this ends with _client.c, use corresponding lib as props key
    """
    if source_file.stem.endswith("_client"):
        source_file = replace_stem(source_file, source_file.stem[: -len("_client")])
    return str(source_file.relative_to(TEST_DIR))


def needs_mathlib(prog: Path) -> bool:
    key = get_props_key(prog)
    return key in REQUIRES_MATHLIB and not IS_OSX


def get_libs(prog: Path) -> List[Path]:
    """Get extra libraries this test program depends on (aside from lib/client pairs)"""
    props_key = get_props_key(prog)
    libs = []
    if props_key in ASSEMBLY_DEPENDENCIES:
        for asm_dep in ASSEMBLY_DEPENDENCIES[props_key]:
            asm_filename = asm_dep + get_platform_suffix()
            asm_path = TEST_DIR / asm_filename
            libs.append(asm_path)
    if props_key in DEPENDENCIES:
        lib_filenames = DEPENDENCIES[props_key]
        for l in lib_filenames:
            lib_path = TEST_DIR / l
            libs.append(lib_path)
    return libs


def print_stderr(proc: subprocess.CompletedProcess[str]) -> None:
    """Print out stderr of CompletedProcess if it's not empty. Intended to print assembler/linker warnings"""
    if proc.stderr:
        print(proc.stderr)


def gcc_compile_and_run(
    source_files: List[Path], options: List[str]
) -> subprocess.CompletedProcess[str]:
    """Compile input files using 'gcc' command and run the resulting executable

    Args:
        source_files: list of input files - could be C, assembly, or object files
        options: command-line options

    Returns:
        a CompletedProecess object that captures the executable's return code and output
    """

    # output file is same as first input without suffix
    exe = source_files[0].with_suffix("")

    # compile it
    try:
        result = subprocess.run(
            ["gcc", "-D", "SUPPRESS_WARNINGS"] + source_files + options + ["-o", exe],
            check=True,
            text=True,
            capture_output=True,
        )
        # print any warnings even if it succeeded
        print_stderr(result)
    except subprocess.CalledProcessError as err:
        # This is an internal error in the test suite
        # TODO better handling of internal problems with test suite
        raise RuntimeError(err.stderr) from err

    # run it
    return subprocess.run(
        [exe], check=False, text=True, capture_output=True, timeout=10.0
    )


def replace_stem(path: Path, new_stem: str) -> Path:
    """Return a new path with the stem changed and suffix the same"""
    if sys.version_info >= (3, 9):
        return path.with_stem(new_stem)

    # workaround for 3.8: stick old suffix on new stem
    return path.with_name(new_stem).with_suffix(path.suffix)


class TestChapter(unittest.TestCase):
    """Base per-chapter test class - should be subclassed, not instantiated directly.

    For each chapter under test, we construct a subclass of TestChapter and generate
    a test method for each C program in the corresponding directory. Each dynamically generated
    test calls one of the main test methods defined below:

    * compile_failure: compilation should fail)
    * compile_success: compilation should succeed up to some intermediate stage)
    * compile_and_run: compiling and running the test program should give the expected result)
    * compile_client_and_run: the test program consists of a client and library.
        compiling the client with our compiler and library with the system compiler,
        run the compiled program, and validate the result
    * compile_lib_and_run:
        like compile_client_and_run, but compile the *library* withour compiler
        and *client* with the system compiler
    * compile_with_helper_lib_and_run:
        like compile_client_and_run except the library is defined in test_properties.json and is not under test
        library should be in TEST_DIR/helper_libs/
    * compile_with_asm_lib_and_run:
        like compile_client_and_run except the library is an assembly file defined in test_properties.json, not a C file

    The other methods in TestChapter are all utilties called by the compile_* methods.
    """

    longMessage = False

    # Attributes that each subclass must override

    # absolute path to this chapter's subdirectory
    # (e.g. /path/to/write-a-c-compiler-tests/chapter_1/)
    test_dir: Path

    # absolute path to the compiler under test
    cc: Path

    # list of command-line options to pass through to the compiler under test
    options: list[str]

    # last stage of the compiler we're testing; None if we're testing the whole thing
    exit_stage: str

    # expected compiler exit codes when rejecting invalid programs (None if we accept any non-zero exit code)
    error_codes: list[int]

    def tearDown(self) -> None:
        """Delete files produced during this test run (e.g. assembly and object files)"""
        garbage_files = (
            f
            for f in self.test_dir.rglob("*")
            if not f.is_dir()
            and f.suffix not in [".c", ".h", ".md"]
            and f.name not in ASSEMBLY_LIBS
        )

        for junk in garbage_files:
            junk.unlink()

    def invoke_compiler(
        self, source_file: Path, cc_opt: Optional[str] = None
    ) -> subprocess.CompletedProcess[str]:
        """Compile the test program (possibly up to some intermediate stage), but don't run it.

        Args:
            source_file: Absolute path to source file
            cc_opt (optional): Additional command-line options to pass to compiler
                (in addition to exit stage and anything specified in self.options).
                Used to compile without linking (for library tests);
                to link math library; and to compile to assembly (for optimization tests)

        Returns:
            A CompletedObject the captures the result of compilation (including an exit code
            indicating whether it succeeded and any error messages produced by the compiler)
        """
        if cc_opt is None and self.exit_stage is not None:
            cc_opt = f"--{self.exit_stage}"

        args = [self.cc] + self.options
        if cc_opt is not None:
            args.append(cc_opt)

        args.append(source_file)

        # run the command: '{self.cc} {options} {source_file}'
        proc = subprocess.run(args, capture_output=True, check=False, text=True)

        return proc

    def validate_no_output(self, source_file: Path) -> None:
        """Make sure the compiler under test didn't emit executable or assembly code.

        Used when compiling invalid test cases or testing intermediate stages."""

        # if we compiled /path/to/foo.c, look for /path/to/foo.s
        stem = source_file.stem
        assembly_file = source_file.parent / f"{stem}.s"
        self.assertFalse(
            assembly_file.exists(),
            msg=f"Found assembly file {assembly_file} for invalid program!",
        )

        # now look for /path/to/foo
        executable_file = source_file.parent / stem
        self.assertFalse(executable_file.exists())

    def validate_runs(
        self, source_file: Path, actual: subprocess.CompletedProcess[str]
    ) -> None:
        """Validate that the running compiled executable gave the expected result.

        Compare return code and stdout to values in EXPECTED_RESULTS.

        Args:
            source_file: Absolute path of the source file for a test program
            actual: result of compiling this source file with self.cc and running it
        """
        key = get_props_key(source_file)
        expected = EXPECTED_RESULTS[key]
        expected_retcode = expected["return_code"]
        expected_stdout = expected.get("stdout", "")

        exe = actual.args[0]
        self.assertEqual(
            expected_retcode,
            actual.returncode,
            msg=f"Expected return code {expected_retcode}, found {actual.returncode} in {exe}",
        )
        self.assertEqual(
            expected_stdout,
            actual.stdout,
            msg=f"Expected output {expected_stdout}, found {actual.stdout} in {exe}",
        )

        # none of our test programs write to stderr
        self.assertFalse(
            actual.stderr, msg=f"Unexpected error output {actual.stderr} in {exe}"
        )

    def compile_failure(self, source_file: Path) -> None:
        """Test that compiling an invalid program returns a non-zero exit code

        Use this when compilation of the test program should fail at or before the stage under test.
        E.g. if type_error.c contains a type error,
        when we use the --stage validate option, test_type_error will call compile_failure
        but when we use the --stage parse option, test_type_error will call compile_success (below)
        """
        result: subprocess.CompletedProcess[str]
        with self.assertRaises(
            subprocess.CalledProcessError, msg=f"Didn't catch error in {source_file}"
        ):
            result = self.invoke_compiler(source_file)
            result.check_returncode()  # raise CalledProcessError if return code is non-zero

        # make sure we got an expected error code, if specified
        if self.error_codes:
            exit_code_list = ", ".join(str(e) for e in self.error_codes)
            self.assertIn(
                result.returncode,
                self.error_codes,
                msg=f"Compilation failed with exit code {result.returncode}, but expected one of the following exit codes: {exit_code_list}.",
            )

        self.validate_no_output(source_file)

    def compile_success(self, source_file: Path) -> None:
        """Test that compiling a valid program returns exit code of 0.

        Use this when compilation of the program should succeed up until the stage under test.
        This is only used when testing an intermediate stage; when testing the whole compiler,
        use compile_and_run instead."""
        # run compiler up to stage, make sure it doesn't throw an exception
        result = self.invoke_compiler(source_file)
        self.assertEqual(
            result.returncode,
            0,
            msg=f"compilation of {source_file} failed with error:\n{result.stderr}",
        )

        # make sure we didn't emit executable or assembly code
        self.validate_no_output(source_file)

    def compile_and_run(self, source_file: Path) -> None:
        """Compile a valid test program, run it, and validate the results"""

        # if this depends on extra libraries, call library_test_helper instead
        extra_libs = get_libs(source_file)
        if extra_libs:
            self.library_test_helper(source_file, extra_libs)
            return

        # include -lm for standard library test on linux
        if needs_mathlib(source_file):
            cc_opt = "-lm"
        else:
            cc_opt = None

        # run compiler, make sure it succeeds
        compile_result = self.invoke_compiler(source_file, cc_opt=cc_opt)
        self.assertEqual(
            compile_result.returncode,
            0,
            msg=f"compilation of {source_file} failed with error:\n{compile_result.stderr}",
        )

        # print stderr (might have warnings we care about even if compilation succeeded)
        # TODO make this controlled by verbosity maybe?
        print_stderr(compile_result)

        # run the executable
        # TODO cleaner handling if executable doesn't exist? or check that it exists above?
        exe = source_file.with_suffix("")
        result = subprocess.run(
            [exe], check=False, capture_output=True, text=True, timeout=10.0
        )

        self.validate_runs(source_file, result)

    def library_test_helper(
        self, file_under_test: Path, other_files: List[Path]
    ) -> None:
        """Compile one file in a multi-file program and validate the results.

        Compile file_under_test with compiler under test and other_files with 'gcc' command.
        Link 'em together, run the resulting executable, make validate the results.

        Args:
            file_under_test: Absolute path of one file in a multi-file program.
                Usually a C file we want to compile with self.cc, but sometimes
                (in optimization tests) an assembly file that we've alerady
                compiled with self.cc and inspected
            other_files: Absolute paths to other files in the multi-file program
        """

        # If file_under_test is a C program, compile it with self.cc;
        # otherwise assume it's already been compiled with self.cc
        if file_under_test.suffix == ".c":
            # make sure compilation succeeds
            compilation_result = self.invoke_compiler(file_under_test, cc_opt="-c")
            self.assertEqual(
                compilation_result.returncode,
                0,
                msg=f"compilation of {file_under_test} failed with error:\n{compilation_result.stderr}",
            )
            # print stderr (might have warnings we care about even if compilation succeeded)
            # TODO make this controlled by verbosity maybe?
            print_stderr(compilation_result)
            compiled_file_under_test = file_under_test.with_suffix(".o")
            validation_key = file_under_test
        else:
            compiled_file_under_test = file_under_test
            validation_key = file_under_test.with_suffix(".c")

        # compile other files, link with object file produced by compiler under test,
        # and run resulting executable
        source_files = [compiled_file_under_test] + other_files
        options = []
        if needs_mathlib(file_under_test) or any(needs_mathlib(f) for f in other_files):
            options.append("-lm")
        result = gcc_compile_and_run(source_files, options)

        # validate results
        self.validate_runs(validation_key, result)

    def compile_client_and_run(self, client_path: Path) -> None:
        """Multi-file program test where our compiler compiles the client"""

        # <FOO>_client.c should have corresponding library <FOO>.c in the same directory
        lib_path = replace_stem(client_path, client_path.stem[: -len("_client")])
        self.library_test_helper(client_path, [lib_path])

    def compile_lib_and_run(self, lib_path: Path) -> None:
        """Multi-file program test where our compiler compiles the library"""

        # program path <FOO>.c should have corresponding <FOO>_client.c in same directory
        client_path = replace_stem(lib_path, lib_path.stem + "_client")
        self.library_test_helper(lib_path, [client_path])


# Automatically generating test classes + methods


class TestDirs:
    """Subdirectory names within each test directory"""

    # invalid programs
    INVALID_LEX = "invalid_lex"
    INVALID_PARSE = "invalid_parse"
    INVALID_SEMANTICS = "invalid_semantics"
    INVALID_DECLARATIONS = "invalid_declarations"
    INVALID_TYPES = "invalid_types"
    INVALID_LABELS = "invalid_labels"
    INVALID_STRUCT_TAGS = "invalid_struct_tags"
    # valid test programs for parts I & II
    # (we'll handle part III test sdifferently)
    VALID = "valid"


dirs = {
    "invalid": [
        TestDirs.INVALID_LEX,
        TestDirs.INVALID_PARSE,
        TestDirs.INVALID_SEMANTICS,
        TestDirs.INVALID_DECLARATIONS,
        TestDirs.INVALID_TYPES,
        TestDirs.INVALID_LABELS,
        TestDirs.INVALID_STRUCT_TAGS,
    ],
    "valid": [TestDirs.VALID],
}

# For a particular stage under test (specified by --test option),
# look up which test programs compiler should process successfully
# and which ones it should reject
DIRECTORIES_BY_STAGE = {
    "lex": {
        "invalid": [TestDirs.INVALID_LEX],
        "valid": [
            TestDirs.INVALID_PARSE,
            TestDirs.INVALID_SEMANTICS,
            TestDirs.INVALID_DECLARATIONS,
            TestDirs.INVALID_TYPES,
            TestDirs.INVALID_LABELS,
            TestDirs.INVALID_STRUCT_TAGS,
        ]
        + dirs["valid"],
    },
    "parse": {
        "invalid": [TestDirs.INVALID_LEX, TestDirs.INVALID_PARSE],
        "valid": [
            TestDirs.INVALID_SEMANTICS,
            TestDirs.INVALID_DECLARATIONS,
            TestDirs.INVALID_TYPES,
            TestDirs.INVALID_LABELS,
            TestDirs.INVALID_STRUCT_TAGS,
        ]
        + dirs["valid"],
    },
    "validate": dirs,
    "tacky": dirs,
    "codegen": dirs,
    "run": dirs,
}


@unique
class ExtraCredit(Flag):
    """An ExtraCredit flag represents a set of enabled extra-credit features"""

    BITWISE = auto()
    COMPOUND = auto()
    INCREMENT = auto()
    GOTO = auto()
    SWITCH = auto()
    NAN = auto()
    UNION = auto()
    NONE = 0
    # spurious pylint error (https://github.com/PyCQA/pylint/issues/7381)
    # pylint: disable=unsupported-binary-operation
    ALL = BITWISE | COMPOUND | INCREMENT | GOTO | SWITCH | NAN | UNION


def excluded_extra_credit(source_prog: Path, extra_credit_flags: ExtraCredit) -> bool:
    """Based on our current extra credit settings, should we include this test program?

    Args:
        source_prog: Absolute path to a C test program
        extra_credit_flags: extra credit features to test (specified on the command line)

    Returns:
        true if we should _exclude_ this program from test run, false if we should include it.
    """

    if "extra_credit" not in source_prog.parts:
        # this isn't an extra-credit test so we shouldn't exclude it
        return False

    # convert list of strings representing required extra credit features for this program
    # to list of ExtraCredit flags
    key = get_props_key(source_prog)

    features_required = (
        ExtraCredit[str.upper(feature)] for feature in EXTRA_CREDIT_PROGRAMS[key]
    )

    # exclude this test if it requires any extra credit features that
    # aren't included in this test run
    return any(f not in extra_credit_flags for f in features_required)


def make_invalid_test(program: Path) -> Callable[[TestChapter], None]:
    """Generate a test method for an invalid source program"""

    def test_invalid(self: TestChapter) -> None:
        self.compile_failure(program)

    return test_invalid


def make_test_valid(program: Path) -> Callable[[TestChapter], None]:
    """Generate one test method to compile a valid program.

    Only used when testing intermediate stages. Use make_test_run when testing
    the whole compiler"""

    def test_valid(self: TestChapter) -> None:
        self.compile_success(program)

    return test_valid


def make_test_run(program: Path) -> Callable[[TestChapter], None]:
    """Generate one test method to compile and run a valid single-file program
    (the program may depend on additional source or assembly files that are not under test)
    """

    def test_run(self: TestChapter) -> None:
        self.compile_and_run(program)

    return test_run


def make_test_client(program: Path) -> Callable[[TestChapter], None]:
    """Generate one test method for client in multi-file program"""

    def test_client(self: TestChapter) -> None:
        self.compile_client_and_run(program)

    return test_client


def make_test_lib(program: Path) -> Callable[[TestChapter], None]:
    """Generate one test method for library in multi-file program"""

    def test_lib(self: TestChapter) -> None:
        self.compile_lib_and_run(program)

    return test_lib


def make_invalid_tests(
    test_dir: Path, stage: str, extra_credit_flags: ExtraCredit
) -> list[tuple[str, Callable[[TestChapter], None]]]:
    """Generate one test method for each invalid test program in test_dir.

    We use extra_credit_flags and stage to discover invalid test cases within test_dir.

    Args:
        test_dir: Absolute path to the test directory for a specific chapter
                  (e.g. /path/to/write-a-c-compiler-tests/chapter_1/)
        stage: only compile programs through this stage. this dictates which programs
               are considered invalid (e.g. if stage is "parse" programs with type errors
               are valid, because we stop before typechecking)
        extra_credit_flags: extra credit features to test (specified on the command line)

    Returns:
        A list of (name, test method) tuples, intended to be included on a dynamically generated
        subclass of TestChapter
    """
    tests: list[tuple[str, Callable[[TestChapter], None]]] = []
    for invalid_subdir in DIRECTORIES_BY_STAGE[stage]["invalid"]:
        invalid_test_dir = test_dir / invalid_subdir
        for program in invalid_test_dir.rglob("*.c"):
            if excluded_extra_credit(program, extra_credit_flags):
                continue

            # derive name of test method from name of source file
            key = program.relative_to(test_dir).with_suffix("")
            # TODO maybe don't have / in function names, it's weird!
            # maybe use source filename as ID?
            test_name = f"test_{key}"

            test_method = make_invalid_test(program)
            tests.append((test_name, test_method))

    return tests


def make_valid_tests(
    test_dir: Path, stage: str, extra_credit_flags: ExtraCredit
) -> list[tuple[str, Callable[[TestChapter], None]]]:
    """Generate one test method for each valid test program in test_dir.

    We use stage and extra_credit_flags to discover valid test cases in test_dir. We also
    use stage to determine what sort of test to run (e.g. if stage is "run" we actually run the
    executable we compile; otherwise we just check that compilation succeeded).

    Args:
        test_dir: Absolute path to the test directory for a specific chapter
                  (e.g. /path/to/write-a-c-compiler-tests/chapter_1/)
        stage: only compile programs through this stage. this dictates which programs
               are considered valid (e.g. if stage is "parse" programs with type errors
               are valid, because we stop before typechecking)
        extra_credit_flags: extra credit features to test (specified on the command line)

    Returns:
        A list of (name, test method) tuples, intended to be included on a dynamically generated
        subclass of TestChapter
    """
    tests: list[tuple[str, Callable[[TestChapter], None]]] = []
    for valid_subdir in DIRECTORIES_BY_STAGE[stage]["valid"]:
        valid_testdir = test_dir / valid_subdir
        for program in valid_testdir.rglob("*.c"):
            if excluded_extra_credit(program, extra_credit_flags):
                # this requires extra credit features that aren't enabled
                continue

            # derive name of test method from name of source file
            key = program.relative_to(test_dir).with_suffix("")
            test_name = f"test_{key}"

            test_method: Callable[[TestChapter], None]
            # test depends on the stage and whether this is a library test
            if stage == "run":
                # all library/multi-file tests are in "library" subdirectories
                if "libraries" not in key.parts:
                    test_method = make_test_run(program)
                # if it's a library test, figure out whether this is lib or client
                elif program.stem.endswith("client"):
                    test_method = make_test_client(program)
                else:
                    test_method = make_test_lib(program)
            else:
                # for stages besides "run", just test that compilation succeeds
                test_method = make_test_valid(program)
            tests.append((test_name, test_method))
    return tests


def build_test_class(
    compiler: Path,
    chapter: int,
    *,
    options: Sequence[str],
    stage: str,
    extra_credit_flags: ExtraCredit,
    skip_invalid: bool,
    error_codes: list[int],
) -> Type[unittest.TestCase]:
    """Construct the test class for a normal (non-optimization) chapter.

    Construct a subclass of TestChapter, generating a test method for each
    program in this chapter's test suite (possibly including some extra credit programs,
    depending on the extra_credit argument).

    Args:
        compiler: absolute path to compiler under test
        chapter: the chapter we're testing
        options: extra command-line options to pass through to compiler
        stage: only compile programs up through this stage
        extra_credit_flags: extra credit features to test, represented as a bit vector
        skip_invalid: true if we should skip invalid test programs
        error_codes: expected compiler exit codes when rejecting invalid programs
    """

    # base directory with all of this chapter's test programs
    test_dir = TEST_DIR.joinpath(f"chapter_{chapter}").resolve()

    testclass_name = f"TestChapter{chapter}"

    # dictionary of class attributes (including properties and methods)
    testclass_attrs = {
        "test_dir": test_dir,
        "cc": compiler,
        "options": options,
        "exit_stage": None if stage == "run" else stage,
        "error_codes": error_codes,
    }

    # generate tests for invalid test programs and add them to testclass_attrs
    if not skip_invalid:
        invalid_tests = make_invalid_tests(test_dir, stage, extra_credit_flags)
        # test_name is the method name
        for test_name, test_cls in invalid_tests:
            testclass_attrs[test_name] = test_cls

    # generate tests for valid test programs
    valid_tests = make_valid_tests(test_dir, stage, extra_credit_flags)
    for test_name, test_cls in valid_tests:
        # test_name is the method name
        testclass_attrs[test_name] = test_cls

    return type(testclass_name, (TestChapter,), testclass_attrs)
