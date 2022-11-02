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
            asm, target_fun="target", other_funs=set(["main", "callee", "count_down", "set_x"]))

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

    @classmethod
    def get_test_for_path(cls, path: Path):
        TESTS = {
            "copy_prop_const_fold": cls.make_retval_test(6, path),
            "fig_20_8": cls.make_retval_test(4, path),
            "init_all_copies": cls.make_retval_test(3, path),
            "prop_static_var": cls.make_retval_test(10, path),
            "killed_then_redefined": cls.make_retval_test(2, path),
            "complex_const_fold": cls.make_retval_test(-1, path),
            "remainder_test": cls.make_retval_test(1, path),
            "multi_path": cls.make_retval_test(3, path),
            "loop": cls.make_retval_test(10, path),
            "multi_path_no_kill": cls.make_retval_test(3, path),
            "propagate_fun_args": cls.make_arg_test("callee", [None, 20], path),
            "kill_and_add_copies": cls.make_arg_test("callee", [10, None], path),
            "propagate_var": cls.make_same_arg_test("callee", path),
            "multi_instance_same_copy": cls.make_same_arg_test("callee", path),
            "redundant_copies": cls.make_redundant_copies_test(path),
            "alias_analysis": cls.make_retval_test(24, path),
            "char_type_conversion": cls.make_retval_test(1, path),
            "copy_struct": cls.make_same_arg_test("callee", path),
            "store_doesnt_kill": cls.make_same_arg_test("callee", path)
        }

        # default test: compile, run and check results without inspecting assembly
        def test_valid(self: TestBase.TestChapter):
            self.compile_and_run(path)

        test_dict = defaultdict(lambda: test_valid, TESTS)
        return test_dict[path.stem]

    @ staticmethod
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
                # only a problem if we expet this specific argument to be a constant
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
