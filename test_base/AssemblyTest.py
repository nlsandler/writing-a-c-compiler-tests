from itertools import zip_longest
import sys
from collections import defaultdict
from enum import Enum, unique, auto
from test_base import TestBase
from test_base import AssemblyParser
from test_base.AssemblyParser import Immediate, Instruction, Label, Opcode, Operand, Register
from typing import Union, Optional, Callable
from pathlib import Path
import subprocess


@unique
class Optimizations(Enum):
    """Which TACKY optimizations to test"""
    CONSTANT_FOLD = auto()
    UNREACHABLE_CODE_ELIM = auto()
    COPY_PROP = auto()
    DEAD_STORE_ELIM = auto()
    ALL = auto()


# instructions we'd expect to find even when we've constant folded the whole function
NOT_COMPUTE_INSTRUCTIONS = [Opcode.PUSH,
                            Opcode.POP, Opcode.MOV, Opcode.RET, Opcode.JMP]


class OptimizationTest(TestBase.TestChapter):

    def get_target_functions(self, asm_file, *, target_fun: str, other_funs: set[str]) -> AssemblyParser.AssemblyFunction:
        if sys.platform == "darwin":
            target_fun = "_" + target_fun
            other_funs = set("_" + n for n in other_funs)
        other_funs.add(target_fun)
        asm = AssemblyParser.parse(
            asm_file, other_funs)
        target_asm = next(f for f in asm if f.name == target_fun)
        return target_asm

    def validate_assembly(self, parsed_asm: AssemblyParser.AssemblyFunction, *, program_path: Path):
        raise NotImplementedError("This is supposed to be subclassed")

    def optimization_test(self, program_path: Path, validator=None):
        """Make sure compiled program has correct results, then inspect its assembly code"""

        # first compile and run the program with GCC
        expected_result = self.gcc_compile_and_run(
            program_path, prefix_output=True)

        # now compile to assembly
        # note: don't need to add --fold-constants b/c it's already in cc_opt
        try:
            self.invoke_compiler(program_path, cc_opt="-s").check_returncode()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(e.stderr) from e
        asm = program_path.with_suffix(".s")

        # compile the assembly code with GCC, run it, and make sure it gives expected result
        actual_result = self.gcc_compile_and_run(asm)
        self.validate_runs(expected_result, actual_result)

        # make sure we actually performed the optimization
        parsed_asm = self.get_target_functions(
            asm, target_fun="target", other_funs=set(["main", "callee", "callee2", "count_down", "set_x", "get" ,"consume"]))

        # validate_assembly is baseline assembly validation but we can override it for specific programs
        if not validator:
            validator = self.validate_assembly
        validator(parsed_asm, program_path=program_path)


def build_msg(msg, *, bad_instructions=None, full_prog=None, program_path=None):
    msg_lines = [msg]
    if bad_instructions:
        printed_instructions = [str(i) for i in bad_instructions]
        msg_lines.append("Bad instructions:")
        msg_lines.extend(printed_instructions)
    if full_prog:
        msg_lines.extend(["Complete program:", str(full_prog)])
    if program_path:
        msg_lines.append(f"Program: {program_path}")
    return '\n'.join(msg_lines)


def is_computation(i: Union[AssemblyParser.Instruction, Label]):
    """Check whether this is an acceptable instruction to see in a fully constant-folded function"""
    if isinstance(i, Label):
        return False

    if i.mnemonic in NOT_COMPUTE_INSTRUCTIONS:
        return False

    if i.mnemonic == Opcode.SUB and i.operands[1] == AssemblyParser.Register.SP:
        return False

    return True


class ConstantFoldingTest(OptimizationTest):

    def validate_assembly(self, parsed_asm, *, program_path: Path):

        compute_instructions = [
            i for i in parsed_asm.instructions if is_computation(i)]
        self.assertFalse(compute_instructions, msg=build_msg(
            "Found instructions that should have been constant folded",
            bad_instructions=compute_instructions, full_prog=parsed_asm, program_path=program_path))


class UnreachableCodeTest(OptimizationTest):

    def validate_just_one_return(self, parsed_asm, *, program_path: Path):
        ret_instruction_count = sum(1 for i in parsed_asm.instructions if isinstance(
            i, AssemblyParser.Instruction) and i.mnemonic == Opcode.RET)
        self.assertLessEqual(ret_instruction_count, 1,
                             msg=f"Expected at most one ret instruction, but found {ret_instruction_count}")

    def validate_assembly(self, parsed_asm, *, program_path: Path):
        # make sure that we've eliminated all jumps, labels, and function calls
        # (in our test cases, all calls to other functions from target are in dead code)
        def bad(i):
            if isinstance(i, Label):
                return True
            if i.mnemonic in [Opcode.JMP, Opcode.JMPCC, Opcode.CALL]:
                return True
            return False

        bad_instructions = [i for i in parsed_asm.instructions if bad(i)]
        self.assertFalse(bad_instructions, msg=build_msg(
            "Found instructions that should have been eliminated",
            bad_instructions=bad_instructions, full_prog=parsed_asm, program_path=program_path))
        self.validate_just_one_return(parsed_asm, program_path=program_path)

    def validate_no_function_calls(self, parsed_asm, *, program_path: Path):
        """Validate that there are no call instructions, but allow other control flow"""
        def bad(i):
            if isinstance(i, AssemblyParser.Instruction) and i.mnemonic == Opcode.CALL:
                return True
            return False

        bad_instructions = [i for i in parsed_asm.instructions if bad(i)]
        self.assertFalse(bad_instructions, msg=build_msg(
            "Found instructions that should have been eliminated",
            bad_instructions=bad_instructions, full_prog=parsed_asm, program_path=program_path))

    def test_dead_after_branch(self):
        program_path = self.test_dir / "dead_after_if_else.c"
        self.optimization_test(
            program_path, validator=self.validate_no_function_calls)

    def test_dead_after_return(self):
        program_path = self.test_dir / "dead_after_return.c"
        self.optimization_test(program_path)

    def test_constant_if_else(self):
        program_path = self.test_dir / "constant_if_else.c"
        self.optimization_test(program_path)

    def test_for_loop(self):
        program_path = self.test_dir / "dead_for_loop.c"
        self.optimization_test(program_path)

    def test_branch_in_loop(self):
        program_path = self.test_dir / "dead_branch_inside_loop.c"
        self.optimization_test(
            program_path, validator=self.validate_no_function_calls)

    def test_empty_blocks(self):
        program_path = self.test_dir / "empty_block.c"
        self.optimization_test(program_path)

    def test_useless_start_label(self):
        program_path = self.test_dir / "remove_useless_starting_label.c"
        self.optimization_test(program_path)

    def test_loop_in_dead_branch(self):
        program_path = self.test_dir / "loop_in_dead_branch.c"
        self.optimization_test(program_path)

    # test for:
    # - we _do_ remove unreachable blocks
    #   x constant_if_else and dead_after_if_else give basic coverage
    #    x including blocks w/out predecessors and blocks whose predecessors are unreachable
    #    - how to test? make sure some function call is gone
    # x we _do not_ remove blocks that have both reachable and unreachable predecessors
    #    - covered by constant_if_else.c
    # x we can handle loops
    #    x include test where loop itself isn't eliminated but branch w/in loop is
    # x we can handle optimizations that result in empty blocks
    # x we remove useless jumps (conditional and unconditional)
    #     x unconditional: in basic dead branch test, make sure jump is gone
    #           constant_if_else covers this
    #     x conditional: non-constant branch wrapping constant branch? or || / &&  ?
    #         - empty_block covers this
    # x we remove useless labels (including at start of block #1)
    #   remove_useless_starting_label and others
    # x we do not remove jump at end of final block


def destination(i: Instruction):
    # no (explicit) destination operand
    if i.mnemonic in [Opcode.PUSH, Opcode.CDQ, Opcode.JMP, Opcode.JMPCC, Opcode.CMP, Opcode.CALL, Opcode.RET]:
        return None
    # otherwise last operand is desintation
    return i.operands[-1]


def is_mov_to(i: Union[Label, Instruction], r: Register) -> bool:
    return isinstance(i, Instruction) and i.mnemonic == Opcode.MOV and i.operands[1] == r


def could_overwrite_reg(i: Union[Label, Instruction], r: Register) -> bool:
    # if this appears after an instruction of the form mov something, eax, could it clobber return value
    if isinstance(i, Label):
        return True  # could jump over mov instruction to reach ret

    # function calls can clobber registers and jmp means we'll never reach ret
    # conditional jump is actually okay if this is still last mov before ret
    # and there are no intervening labels (it's still in ret's only predecessor)
    if i.mnemonic in [Opcode.CALL, Opcode.JMP]:
        return True

    if i.mnemonic in [Opcode.DIV, Opcode.IDIV] and r in [Register.AX, Register.DX]:
        return True

    if i.mnemonic == Opcode.CDQ and r == Register.DX:
        return True

    if destination(i) == r:
        return True

    return False


class CopyPropTest(OptimizationTest):

    TESTS = None

    @classmethod
    def get_test_for_path(cls, path: Path):
        if cls.TESTS is None:
            test_dict = {
                "copy_prop_const_fold": lambda path: cls.make_retval_test(6, path),
                "fig_20_8": lambda path: cls.make_retval_test(4, path),
                "init_all_copies": lambda path: cls.make_retval_test(3, path),
                "prop_static_var": lambda path: cls.make_retval_test(10, path),
                "killed_then_redefined": lambda path: cls.make_retval_test(2, path),
                "complex_const_fold": lambda path: cls.make_retval_test(-1, path),
                "remainder_test": lambda path: cls.make_retval_test(1, path),
                "multi_path": lambda path: cls.make_retval_test(3, path),
                "loop": lambda path: cls.make_retval_test(10, path),
                "multi_path_no_kill": lambda path: cls.make_retval_test(3, path),
                "propagate_fun_args": lambda path: cls.make_arg_test("callee", [None, 20], path),
                "kill_and_add_copies": lambda path: cls.make_arg_test("callee", [10, None], path),
                "propagate_var": lambda path: cls.make_same_arg_test("callee", path),
                "multi_instance_same_copy": lambda path: cls.make_same_arg_test("callee", path),
                "redundant_copies": lambda path: cls.make_redundant_copies_test(path),
                "alias_analysis": lambda path: cls.make_retval_test(24, path),
                "char_type_conversion": lambda path: cls.make_retval_test(1, path),
                "copy_struct": lambda path: cls.make_same_arg_test("callee", path),
                "store_doesnt_kill": lambda path: cls.make_same_arg_test("callee", path),
                "propagate_null_pointer": lambda path: cls.make_retval_test(0, path),
                "const_fold_sign_extend": lambda path: cls.make_retval_test(-1000, path),
                "const_fold_sign_extend_2": lambda path: cls.make_retval_test(-1000, path),
                "char_round_trip": lambda path: cls.make_retval_test(1, path),
                "char_round_trip_2": lambda path: cls.make_retval_test(-1, path),
                "unsigned_compare": lambda path: cls.make_retval_test(1, path),
                "not_char": lambda path: cls.make_retval_test(1, path),
                "signed_unsigned_conversion": lambda path: cls.make_retval_test(-11, path),
                "unsigned_wraparound": lambda path: cls.make_retval_test(0, path),
                "const_fold_type_conversions": lambda path: cls.make_retval_test(83333, path),
                "pointer_arithmetic": lambda path: cls.make_no_computations_test(path),
                "propagate_doubles": lambda path: cls.make_retval_test(3000, path)
            }
            # default test: compile, run and check results without inspecting assembly

            def default(p: Path):
                def test_valid(self: TestBase.TestChapter):
                    self.compile_and_run(p)
                return test_valid

            cls.TESTS = defaultdict(lambda: default, test_dict)

        return cls.TESTS[path.stem](path)

    @staticmethod
    def find_return_value(parsed_asm: AssemblyParser.AssemblyFunction) -> Operand:
        # TODO this assumes int return value
        reversed_instrs = list(reversed(parsed_asm.instructions))
        # last instruction should be ret
        last_instruction = reversed_instrs[0]

        def is_ret(i):
            return (isinstance(i, Instruction) and i.mnemonic == Opcode.RET)

        # if asssembly doesn't match our expectations in ways that aren't specifically under test (e.g. there are multiple return value)
        # raise an error
        if not is_ret(last_instruction):
            raise RuntimeError(
                f"Last instruction in function should be ret but found {last_instruction}")

        # no other ret instructions in the program
        if any(is_ret(
                i) for i in reversed_instrs[1:]):
            raise RuntimeError(
                "Last instruction should be only ret instruction")

        # find instruction of the form mov op, eax
        retval_instr: Instruction
        retval_idx, retval_instr = next((idx, instr) for idx, instr in enumerate(
            reversed_instrs) if is_mov_to(instr, Register.AX))

        # make sure this is definitely the correct instruction
        clobber_instr = next((could_overwrite_reg(i, Register.AX)
                              for i in reversed_instrs[:retval_idx]), None)
        if clobber_instr:
            raise RuntimeError(
                f"Couldn't find return value: might be clobbered by {clobber_instr} ")

        # now return src of mov instruction; this is our return value
        return retval_instr.operands[0]

    @ staticmethod
    def make_retval_test(expected_retval: Union[int, str], program_path: Path) -> Callable:

        expected_op: Operand
        if isinstance(expected_retval, int):
            expected_op = Immediate(expected_retval)
        else:
            if sys.platform == "darwin":
                expected_op = "_" + expected_retval
            expected_op = AssemblyParser.Memory(
                disp=[expected_retval], base=Register.IP, idx=None, scale=1)

        def test(self):
            def validate_return_value(parsed_asm, *, program_path: Path):
                actual_retval = self.find_return_value(parsed_asm)
                self.assertEqual(expected_op, actual_retval,
                                 msg=f"Expected {expected_op} as return value, found {actual_retval} ({program_path})")
            self.optimization_test(program_path=program_path,
                                   validator=validate_return_value)
        return test

    @ staticmethod
    def find_args(callee: str, arg_count: int, parsed_asm: AssemblyParser.AssemblyFunction) -> list[Optional[Operand]]:
        # TODO handle floating args
        # TODO refactor w/ find_return-value
        reversed_instrs = list(reversed(parsed_asm.instructions))
        if sys.platform == "darwin":
            callee = "_" + callee
        funcall_idx = reversed_instrs.index(Instruction(Opcode.CALL, [callee]))
        before_funcall = reversed_instrs[funcall_idx + 1:]
        arg_regs = [Register.DI, Register.SI, Register.DX,
                    Register.CX, Register.R8, Register.R9]

        args: list[Optional[Operand]] = []
        for r in arg_regs[:arg_count]:
            mov_instr_idx, mov_instr = next((idx, instr) for (
                idx, instr) in enumerate(before_funcall) if is_mov_to(instr, r))

            # found a possible move instruction
            if any(could_overwrite_reg(instr, r) for instr in before_funcall[:mov_instr_idx]):
                # None means "we couldn't find move instruction that populates this argument"
                # only a problem if we expect this specific argument to be a constant
                args.append(None)
            else:
                args.append(mov_instr.operands[0])

        return args

    @staticmethod
    def make_arg_test(callee: str, expected_args: list[Optional[int]], program_path: Path):
        expected_ops: list[Optional[Operand]] = [
            Immediate(i) if i else None for i in expected_args]

        def test(self):
            def validate_args(parsed_asm, *, program_path: Path):

                actual_args = self.find_args(
                    callee, len(expected_args), parsed_asm)
                for idx, (actual, expected) in enumerate(zip_longest(actual_args, expected_ops)):
                    if expected is not None:
                        self.assertEqual(
                            actual, expected, msg=f"Expected argument {idx} to function {callee} to be {expected}, found {actual}")
            self.optimization_test(program_path=program_path,
                                   validator=validate_args)

        return test

    @staticmethod
    def make_same_arg_test(callee: str, program_path: Path):
        """Test that first and second arguments to callee are the same"""

        def test(self):
            def validate_args(parsed_asm, *, program_path: Path):
                actual_args = self.find_args(
                    callee, 2, parsed_asm)
                # they're the same value if:
                # same value moved into EDI and ESI, or
                # EDI is moved into ESI, or
                # ESI is moved into EDI
                same_value = (actual_args[0] == actual_args[1] or actual_args[0]
                              == Register.SI or actual_args[1] == Register.DI)
                self.assertTrue(
                    same_value, msg=f"Bad arguments {actual_args[0]} and {actual_args[1]} to {callee}: both args should have same value")

            self.optimization_test(program_path=program_path,
                                   validator=validate_args)
        return test

    @staticmethod
    def make_redundant_copies_test(program_path: Path):

        def test(self):
            def validator(parsed_asm, *, program_path: Path):
                """ validate no control flow"""
                def bad(i):
                    if isinstance(i, Label):
                        return True
                    if i.mnemonic in [Opcode.JMP, Opcode.JMPCC]:
                        return True
                    return False

                bad_instructions = [
                    i for i in parsed_asm.instructions if bad(i)]
                self.assertFalse(bad_instructions, msg=build_msg(
                    "Found instructions that should have been eliminated",
                    bad_instructions=bad_instructions, full_prog=parsed_asm, program_path=program_path))

            self.optimization_test(program_path, validator)
        return test

    @staticmethod
    def make_no_computations_test(program_path: Path):

        def is_lea(i):
            if isinstance(i, Instruction) and i.mnemonic == Opcode.LEA:
                mem: AssemblyParser.Memory = i.operands[0]
                if mem.idx is None and mem.scale == 1:
                    return True

            return False

        def test(self):
            # TODO refactor w/ ConstantFoldingTest
            def validate_assembly(parsed_asm, *, program_path: Path):

                compute_instructions = [
                    i for i in parsed_asm.instructions if is_computation(i) and not is_lea(i)]
                self.assertFalse(compute_instructions, msg=build_msg(
                    "Found instructions that should have been constant folded",
                    bad_instructions=compute_instructions, full_prog=parsed_asm, program_path=program_path))
            self.optimization_test(program_path, validate_assembly)

        return test


class DeadStoreEliminationTest(OptimizationTest):

    TESTS = None

    @classmethod
    def get_test_for_path(cls, path: Path):
        if cls.TESTS is None:
            test_dict = {
                "simple": lambda path: cls.make_dse_test(10, path),
                "dead_store_static_var": lambda path: cls.make_dse_test(5, path),
                "elim_second_copy": lambda path: cls.make_dse_test(10, path),
                "fig_20_12": lambda path: cls.make_dse_test(10, path),
                "loop_dead_store": lambda path: cls.make_dse_test(5, path),
                "use_and_kill": lambda path: cls.make_return_const_test(5, path),
                "aliased_dead_at_exit": lambda path: cls.make_dse_test(50, path)
            }
            # default test: compile, run and check results without inspecting assembly

            def default(p: Path):
                def test_valid(self: TestBase.TestChapter):
                    self.compile_and_run(p)
                return test_valid

            cls.TESTS = defaultdict(lambda: default, test_dict)

        return cls.TESTS[path.stem](path)

    @staticmethod
    def make_dse_test(redundant_const: int, program_path: Path):

        def bad(i: Instruction):
            # we expect to remove an instruction of the form mov $redundant_const, <something>,
            # so make sure $redundant_const never shows up in the program
            return isinstance(i, Instruction) and i.operands and i.operands[0] == Immediate(redundant_const)

        def test(self):
            def validate(parsed_asm, *, program_path: Path):
                bad_instructions = [
                    i for i in parsed_asm.instructions if bad(i)]
                self.assertFalse(bad_instructions, msg=build_msg(
                    "Found dead store that should have been eliminated", bad_instructions=bad_instructions, full_prog=parsed_asm, program_path=program_path))

            self.optimization_test(
                program_path=program_path, validator=validate)

        return test

    @staticmethod
    def make_return_const_test(const: int, program_path: Path):
        """Validate that we don't have any computations or move instructions other than mov $const, %eax"""

        def bad(i: Instruction):
            if is_computation(i):
                return True
            if i.mnemonic == Opcode.MOV:
                # only permitted mov instructions: mov specified return value into AX and manage stack frame
                if i.operands[0] == Immediate(const) and i.operands[1] == Register.AX:
                    return False
                if i.operands[1] in [Register.SP, Register.BP]:
                    return False
                return True
            return False

        def test(self):
            def validate(parsed_asm, *, program_path: Path):
                bad_instructions = [
                    i for i in parsed_asm.instructions if bad(i)]
                self.assertFalse(bad_instructions, msg=build_msg(
                    "Found instruction that should have been optimized out", bad_instructions=bad_instructions, full_prog=parsed_asm, program_path=program_path))

            self.optimization_test(
                program_path=program_path, validator=validate)

        return test

class RegAllocTest(OptimizationTest):
    TESTS = None
    CALLEE_SAVED = [ Register.BX, Register.R12, Register.R13, Register.R14, Register.R15 ]


    @property
    def wrapper_script(self):
        return self.test_dir.joinpath("wrapper.s")

    @property
    def lib_path(self):
        return self.test_dir.joinpath("libraries")

    def tearDown(self) -> None:
        
        # identical to base TestChapter tearDown but don't kill wrapper_script

        # delete any non-C files aproduced during this testrun
        garbage_files = (f for f in self.test_dir.rglob(
            "*") if not f.is_dir() and f.suffix not in ['.c', '.h'] and f.stem != "wrapper")

        for f in garbage_files:
            f.unlink()

    def regalloc_test(self, program_path: Path, validator, extra_lib: Optional[Path]=None, target_fun: str="target"):
        """Base class for register allocation tests
        1. Compile the file at program_path to assembly
        2. Link against check_calleed_saved_regs.s wrapper code
        3. Run, compare results against same code compiled w/ GCC
        4. Inspect assembly code w/ validator
        """

        extra_lib_path = None
        if extra_lib:
            extra_lib_path = self.lib_path / extra_lib

        progs = [program_path, self.wrapper_script]

        if extra_lib_path:
            progs.append(extra_lib_path)
        # compile w/ GCC, check result
        expected_result = self.gcc_compile_and_run(*progs, prefix_output=True)
        
        # assemble
                # now compile to assembly
        # note: don't need to add --fold-constants b/c it's already in cc_opt
        try:
            self.invoke_compiler(program_path, cc_opt="-s").check_returncode()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(e.stderr) from e
        asm = program_path.with_suffix(".s")

        progs = [ asm, self.wrapper_script]
        if extra_lib_path:
            progs.append(extra_lib_path)
        actual_result = self.gcc_compile_and_run(*progs)
        # make sure behavior is the same
        self.validate_runs(expected_result, actual_result)

        # make sure we actually performed the optimization
        parsed_asm = self.get_target_functions(
            asm, target_fun=target_fun, other_funs=set(["main", "client", "callee", "use_value", "reset_globals", "target", "validate_globs", "use", "get", "increase_globals"]))


        validator(parsed_asm, program_path=program_path)


    @classmethod
    def get_test_for_path(cls, path: Path):
        if cls.TESTS is None:
            test_dict = {
                "trivially_colorable": lambda path: cls.make_no_spills_test(path),
                "use_all_hardregs": lambda path: cls.make_no_spills_test(path),
                "spill_callee_saved": lambda path: cls.make_only_callee_saved_spills_test(path),
                "preserve_across_fun_call": lambda path: cls.make_only_callee_saved_spills_test(path, max_regs_spilled=3),
                "track_arg_registers": lambda path: cls.make_no_spills_test(path, extra_lib=Path("track_arg_registers_lib.c")),
                "force_spill": lambda path: cls.make_spill_test(path, max_spilled_instructions=3, max_spilled_pseudos=1, extra_lib=Path("force_spill_lib.c")),
                "test_spill_metric": lambda path: cls.make_spill_test(path, max_spilled_instructions=3, max_spilled_pseudos=1, extra_lib=Path("test_spill_metric_lib.c")),
                "test_spill_metric_2": lambda path: cls.make_spill_test(path, max_spilled_instructions=3, max_spilled_pseudos=1, extra_lib=Path("test_spill_metric_2_lib.c")),
                "cmp_liveness": lambda path: cls.make_only_callee_saved_spills_test(path),
                "copy_no_interference": lambda path: cls.make_only_callee_saved_spills_test(path),
                "copy_and_separate_interference": lambda path: cls.make_spill_test(path, max_spilled_pseudos=1, max_spilled_instructions=3),
                "many_pseudos_fewer_conflicts": lambda path: cls.make_no_spills_test(path, extra_lib=Path("many_pseudos_fewer_conflicts_lib.c"), target_fun="no_spills"),
                "same_instr_no_interference": lambda path: cls.make_only_callee_saved_spills_test(path),
                "optimistic_coloring": lambda path: cls.make_spill_test(path, max_spilled_pseudos=5, max_spilled_instructions=20, target_fun="five_spills"),
                "loop": lambda path: cls.make_no_spills_test(path),
                "dbl_trivially_colorable": lambda path: cls.make_no_spills_test(path),
                "fourteen_pseudos_interfere": lambda path: cls.make_no_spills_test(path),
                "push_xmm": lambda path: cls.make_no_spills_test(path),
                "track_dbl_arg_registers": lambda path: cls.make_no_spills_test(path, extra_lib=Path('track_dbl_arg_registers_lib.c')),
                "store_pointer_in_register": lambda path: cls.make_no_spills_test(path)
            }
            # default test: compile, run and check results without inspecting assembly

            def default(p: Path):
                def test_valid(self: TestBase.TestChapter):
                    self.compile_and_run(p)
                return test_valid

            cls.TESTS = defaultdict(lambda: default, test_dict)

        return cls.TESTS[path.stem](path)

    @staticmethod
    def uses_stack(i: Union[Instruction, Label]):
        if isinstance(i, Label):
            return False

        if i.mnemonic == Opcode.POP and i.operands[0] != Register.BP:
            # popping a value off the stack is a memory access (unelss we're popping RBP to manage the stack frame)
            return True

        def is_stack(operand):
            return isinstance(operand, AssemblyParser.Memory) and operand.base == Register.BP
        
        return any(is_stack(op) for op in i.operands)
    
    @staticmethod
    def make_no_spills_test(program_path: Path, extra_lib: Optional[Path]=None, target_fun: str="target"):

        def test(self):

            def validate(parsed_asm, *, program_path: Path):
                bad_instructions = [i for i in parsed_asm.instructions if self.uses_stack(i)]
                self.assertFalse(bad_instructions, msg=build_msg("Found instructions that use operands on the stack", bad_instructions=bad_instructions, full_prog=parsed_asm, program_path=program_path))
            self.regalloc_test(program_path=program_path, validator=validate, extra_lib=extra_lib, target_fun=target_fun)
        
        return test
    
    @classmethod
    def find_spills(cls, parsed_asm: AssemblyParser.AssemblyFunction):
        stack_instructions : list[AssemblyParser.Instruction] = [i for i in parsed_asm.instructions if cls.uses_stack(i)]

        # for each callee-saved reg, we accept one move from it and one move to it
        # TODO recognize saving and restoring with push/pop too
        allowed_moves : dict[AssemblyParser.Register, dict[str, list]]= {r : { "to": [], "from": []} for r in cls.CALLEE_SAVED}

        spill_instructions = []
        for si in stack_instructions:
            if si.mnemonic != Opcode.MOV:
                spill_instructions.append(si)
                continue
            src, dst = si.operands[0], si.operands[1]
            if src in cls.CALLEE_SAVED:
                allowed_moves[src]["from"].append(si)
            
            elif dst in cls.CALLEE_SAVED:
                allowed_moves[dst]["to"].append(si)
            else:
                spill_instructions.append(si)
        
        for v in allowed_moves.values():
            # if there's more than one copy to or from a particular callee-saved reg, that's bad
            spill_instructions.extend(v["to"][1:])
            spill_instructions.extend(v["from"][:-1])
        return stack_instructions, spill_instructions

    @staticmethod
    def make_only_callee_saved_spills_test(program_path: Path, max_regs_spilled=5):
        """Create a test that validates that there are no spills, except for copies to/from callee-saved regs at start and end
        
        Optionally, specify maximum number of callee-saved regs we're allowed to spill (all 5 by default)
        """

        def test(self):

            def validate(parsed_asm, *, program_path: Path):
                stack_instructions, bad = self.find_spills(parsed_asm)

                self.assertFalse(bad, msg=build_msg("Found uses of spilled pseudos besides callee-saved tmps", bad_instructions=bad, full_prog=parsed_asm, program_path=program_path))

                # make sure we don't spill more than the allowable number of callee-saved regs
                max_stack_instructions = max_regs_spilled * 2
                self.assertLessEqual(len(stack_instructions), max_stack_instructions,
                    msg=build_msg(f"At most {max_stack_instructions/2} callee-saved registers should be spilled, but it looks like {len(stack_instructions)/2} were spilled.",
                    bad_instructions=stack_instructions, full_prog=parsed_asm, program_path=program_path))
            self.regalloc_test(program_path=program_path, validator=validate)

        return test
    
    @staticmethod
    def make_spill_test(program_path: Path,  max_spilled_instructions: int, max_spilled_pseudos: int, extra_lib: Optional[Path]=None, target_fun: str="target"):
        """Test for a program with so many conflicts that it spills (not just callee-saved regs)
           Validate that our only stack instructions are:
           - saving/restoring callee-saved regs
           - up to 2 instructions using one spilled pseudo
        """
    
        def test(self):

            def validate(parsed_asm, *, program_path: Path):

                _, spill_instructions = self.find_spills(parsed_asm)
                self.assertLessEqual(len(spill_instructions), max_spilled_instructions,
                                     msg=build_msg(f"Should only need {max_spilled_instructions} instructions involving spilled pseudo but found {len(spill_instructions)}",
                                     bad_instructions=spill_instructions, full_prog=parsed_asm, program_path=program_path))
                
                spilled_operands = set([op for i in spill_instructions for op in i if isinstance(op, AssemblyParser.Memory) ])
                self.assertLessEqual(len(spilled_operands), max_spilled_pseudos, msg=build_msg(f"At most {max_spilled_pseudos} pseudoregs should have been spilled, looks like {len(spilled_operands)} were",
                                     bad_instructions=spill_instructions, full_prog=parsed_asm, program_path=program_path))
                
            self.regalloc_test(program_path=program_path, validator=validate, target_fun=target_fun, extra_lib=extra_lib)
        
        return test