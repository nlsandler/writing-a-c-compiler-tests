"""Base class for compiler tests"""
from pathlib import Path
from enum import Flag, auto, unique
from typing import Optional, Tuple, Callable, Iterable, Any
import re
import itertools
import json
import subprocess
import unittest


EXPECTED_RESULTS : dict[str, Any]

with open("expected_results.json", "r") as f:
    EXPECTED_RESULTS = json.load(f)

def replace_stem(path: Path, new_stem: str) -> Path:
    try:
        return path.with_stem(new_stem)
    except AttributeError:
        # python versions before 3.9
        # stick old suffix on new stem
        return path.with_name(new_stem).with_suffix(path.suffix)


class TestDirs:
    # invalid programs
    INVALID_LEX = "invalid_lex"
    INVALID_PARSE = "invalid_parse"
    INVALID_SEMANTICS = "invalid_semantics"
    INVALID_DECLARATIONS = "invalid_declarations"
    INVALID_TYPES = "invalid_types"
    INVALID_STRUCT_TAGS = "invalid_struct_tags"
    # valid test programs for parts I & II
    # (we'll handle part III test sdifferently)
    VALID = "valid"


dirs = {"invalid": [TestDirs.INVALID_LEX,
                    TestDirs.INVALID_PARSE,
                    TestDirs.INVALID_SEMANTICS,
                    TestDirs.INVALID_DECLARATIONS,
                    TestDirs.INVALID_TYPES,
                    TestDirs.INVALID_STRUCT_TAGS],
        "valid": [TestDirs.VALID]
        }

DIRECTORIES_BY_STAGE = {
    "lex": {"invalid": [TestDirs.INVALID_LEX],
            "valid": [TestDirs.INVALID_PARSE,
                      TestDirs.INVALID_SEMANTICS,
                      TestDirs.INVALID_DECLARATIONS,
                      TestDirs.INVALID_TYPES,
                      TestDirs.INVALID_STRUCT_TAGS] + dirs["valid"]},
    "parse": {"invalid": [TestDirs.INVALID_LEX, TestDirs.INVALID_PARSE],
              "valid": [TestDirs.INVALID_SEMANTICS,
                        TestDirs.INVALID_DECLARATIONS,
                        TestDirs.INVALID_TYPES,
                        TestDirs.INVALID_STRUCT_TAGS] + dirs["valid"]},
    "validate": dirs,
    "tacky": dirs,
    "codegen": dirs,
    "run": dirs
}

# maybe use a bitwise enum here to combine them?


@unique
class ExtraCredit(Flag):
    """All extra-credit features"""
    BITWISE = auto()
    COMPOUND = auto()
    GOTO = auto()
    SWITCH = auto()
    NAN = auto()
    NONE = 0
    ALL = BITWISE | COMPOUND | GOTO | SWITCH | NAN

    def to_regex(self):
        pattern = '|'.join(name.lower()
                           for name, v in ExtraCredit.__members__.items() if v in self)
        return re.compile(pattern)

# adapted from https://eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases


def gcc_build_obj(prog: Path) -> None:
    """Compile source file to an object file"""
    objfile = prog.with_suffix('.o')

    # IMPORTANT: if we're building a library, and 'gcc' command actually
    # points to clang, which it does on macOS, we must _not_ enable optimizations
    # Clang optimizes out sign-/zero-extension for narrow args
    # which violates the System V ABI and breaks ABI compatibility
    # with our implementation
    # see https://stackoverflow.com/a/36760539
    try:
        subprocess.run(["gcc", prog, "-c", "-fstack-protector-all", "-Wno-incompatible-library-redeclaration",
                        "-o", objfile], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(e.stderr) from e


class TestChapter(unittest.TestCase):
    """Base per-chapter test case"""
    longMessage = False

    # properties overridden by subclass
    test_dir: Path = None
    cc: Path = None
    options: list[str]
    exit_stage: str = None

    def tearDown(self) -> None:

        # delete any non-C files aproduced during this testrun
        garbage_files = (f for f in self.test_dir.rglob(
            "*") if not f.is_dir() and f.suffix not in ['.c', '.h'])

        for f in garbage_files:
            f.unlink()

    def gcc_compile_and_run(self, *args: Path, prefix_output=False) -> subprocess.CompletedProcess:
        exe = args[0].with_suffix('')
        if prefix_output:
            exe = replace_stem(exe, f"expected_{exe.stem}")

        # capture output so we don't see warnings, and so we can report failures
        try:
            subprocess.run(["gcc", "-Wno-incompatible-library-redeclaration"] + list(args) + ["-o", exe],
                           check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(e.stderr) from e
        return subprocess.run([exe], check=False, text=True, capture_output=True)

    def invoke_compiler(self, program_path: Path, cc_opt: Optional[str] = None) -> subprocess.CompletedProcess:
        """Invoke compiler and return CompletedProcess object"""
        # when testing early stages, pass current stage as compiler option (e.g. --lex)
        # for testing library functions, we'll use -c to assemble without linking
        # and to test optimizations we'll use -s to keep assembly code
        if cc_opt is None and self.exit_stage is not None:
            cc_opt = f"--{self.exit_stage}"

        args = [self.cc] + self.options
        if cc_opt is not None:
            args.append(cc_opt)

        args.append(program_path)
        proc = subprocess.run(args, capture_output=True,
                              check=False, text=True)
        return proc

    def validate_no_output(self, program_path: Path):
        """make sure we didn't emit executable or assembly code"""

        # if we compiled /path/to/foo.c, look for /path/to/foo.s
        stem = program_path.stem
        assembly_path = program_path.parent / f'{stem}.s'
        self.assertFalse(assembly_path.exists(
        ), msg=f"Found assembly file {assembly_path} for invalid program!")

        # now look for /path/to/foo
        executable_path = program_path.parent / stem
        self.assertFalse(executable_path.exists())

    def validate_runs(self, expected_retcode: int, expected_stdout: str, actual: subprocess.CompletedProcess):
        exe = actual.args[0]
        self.assertEqual(expected_retcode, actual.returncode,
                         msg=f"Expected return code {expected_retcode}, found {actual.returncode} in {exe}")
        self.assertEqual(expected_stdout, actual.stdout,
                         msg=f"Expected output {expected_stdout}, found {actual.stdout} in {exe}")
        self.assertFalse(actual.stderr, msg=f"Unexpected error output {actual.stderr} in {exe}")

    def compile_failure(self, program_path):

        # make sure compiler returned non-zero exit code -
        # if it does, subprocess.run will raise CalledProcessError
        with self.assertRaises(subprocess.CalledProcessError, msg=f"Didn't catch error in {program_path}"):
            result = self.invoke_compiler(program_path)
            result.check_returncode()

        self.validate_no_output(program_path)

    def compile_success(self, program_path):
        # run compiler up to stage, make sure it doesn't throw an exception
        result = self.invoke_compiler(program_path)
        self.assertEqual(result.returncode, 0,
                         msg=f"compilation failed with error: {result.stderr}")

        # make sure we didn't emit executable or assembly code
        self.validate_no_output(program_path)

    def compile_and_run(self, program_path):

        # first compile and run the program with GCC
        expected_result = EXPECTED_RESULTS[str(program_path)]

        # HACK: include -lm for standard library test on linux
        if "linux" in self.options and "standard_library_call" in str(program_path):
            cc_opt = "-lm"
        else:
            cc_opt = None

        # run compiler, make sure it doesn't throw an exception

        compile_result = self.invoke_compiler(program_path, cc_opt=cc_opt)
        self.assertEqual(compile_result.returncode, 0,
                         msg=f"compilation failed with error: {compile_result.stderr}")

        # run the executable
        exe = program_path.with_suffix('')

        result = subprocess.run(
            [exe], check=False, capture_output=True, text=True)

        self.validate_runs(expected_result["return_code"], expected_result.get("stdout", ''), result)

    def compile_client_and_run(self, program_path: Path):
        """Compile client with self.cc and library with GCC, make sure they work together"""
        lib_source = replace_stem(program_path,
                                  program_path.stem[:-len('_client')])  # strip _client from filename

        gcc_build_obj(lib_source)
        compilation_result = self.invoke_compiler(program_path, cc_opt="-c")
        self.assertEqual(compilation_result.returncode, 0,
                         msg=f"compilation failed with error: {compilation_result.stderr}")

        # link both object files and run resulting executable
        result = self.gcc_compile_and_run(lib_source.with_suffix(
            '.o'), program_path.with_suffix('.o'))

        # now compile both with gcc and run resulting executable
        expected_result = self.gcc_compile_and_run(
            lib_source, program_path, prefix_output=True)

        # make sure results are the same
        self.validate_runs(expected_result.returncode, expected_result.stdout, result)

    def compile_lib_and_run(self, program_path: Path):
        """Compile lib with self.cc and client with GCC, make sure they work together"""
        client_source = replace_stem(program_path, program_path.stem+"_client")

        gcc_build_obj(client_source)

        compilation_result = self.invoke_compiler(program_path, cc_opt="-c")
        self.assertEqual(compilation_result.returncode, 0,
                         msg=f"Compilation failed for cmd: {compilation_result.args} with output {compilation_result.stdout} and stderr {compilation_result.stderr}")

        # link both object files and run resulting executable
        result = self.gcc_compile_and_run(program_path.with_suffix(
            '.o'), client_source.with_suffix('.o'))

        # now compile both with gcc and run resulting executable
        expected_result = self.gcc_compile_and_run(
            program_path, client_source, prefix_output=True)

        # make sure results are the same
        self.validate_runs(expected_result.returncode, expected_result.stdout, result)


def extra_credit_programs(source_dir: Path, extra_credit_flags: Optional[ExtraCredit]) -> Iterable[Path]:
    if not extra_credit_flags:
        return
    extra_cred_regex = extra_credit_flags.to_regex()
    for source_prog in source_dir.rglob("*.c"):
        if extra_cred_regex.search(source_prog.stem):
            yield source_prog


def get_programs(base_dir: Path, sub_dir: str, extra_credit_flags: ExtraCredit) -> Iterable[Path]:
        normal_directory = base_dir / sub_dir
        extra_credit_dir = base_dir/ f"{sub_dir}_extra_credit"
        normal_progs = normal_directory.rglob("*.c")
        extra_credit_progs = extra_credit_programs(extra_credit_dir, extra_credit_flags)
        return itertools.chain(normal_progs, extra_credit_progs)

def make_invalid_test(program: Path) -> Callable:
    def test_invalid(self: TestChapter):
        self.compile_failure(program)
    return test_invalid

def make_invalid_tests(test_dir: Path, stage: str, extra_credit_flags: ExtraCredit) -> list[Tuple[str, Callable]]:
    """Generate one test method for each invalid test program under path"""
    tests : list[Tuple[str, Callable]] = []
    for invalid_subdir in DIRECTORIES_BY_STAGE[stage]["invalid"]:

        for program in get_programs(test_dir, invalid_subdir, extra_credit_flags):
            key = program.relative_to(test_dir).with_suffix("")
            test_name = f"test_{key}"
            test_method = make_invalid_test(program)
            tests.append((test_name, test_method))

    return tests

def make_test_run(program: Path) -> Callable:
    def test_run(self: TestChapter):
        self.compile_and_run(program)
    return test_run

def make_test_client(program: Path) -> Callable:
    def test_client(self: TestChapter):
        self.compile_client_and_run(program)
    return test_client

def make_test_lib(program: Path) -> Callable:
    def test_lib(self: TestChapter):
        self.compile_lib_and_run(program)
    return test_lib

def make_test_valid(program: Path) -> Callable:
    def test_valid(self: TestChapter):
        self.compile_success(program)
    return test_valid

def make_valid_tests(test_dir: Path, stage: str, extra_credit_flags: ExtraCredit) -> list[Tuple[str, Callable]]:
    tests : list[Tuple[str, Callable]] = []
    for valid_subdir in DIRECTORIES_BY_STAGE[stage]["valid"]:

        for program in get_programs(test_dir, valid_subdir, extra_credit_flags):
            key = program.relative_to(test_dir).with_suffix("")
            test_name = f"test_{key}"
            test_method: Callable
            # test depends on the stage and whether this is a library test
            if stage == "run":
                if "libraries" not in key.parts:
                    test_method = make_test_run(program)

                elif program.stem.endswith("client"):
                    test_method = make_test_client(program)
                else:
                    test_method = make_test_lib(program)
            else:
                test_method = make_test_valid(program)
            tests.append((test_name, test_method))
    return tests