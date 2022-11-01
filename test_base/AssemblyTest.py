import sys
from enum import Enum, unique, auto
from test_base import TestBase
from test_base import AssemblyParser
from test_base.AssemblyParser import Immediate, Instruction, Label, Opcode, Operand, Register
from typing import Union
from pathlib import Path


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
        self.invoke_compiler(program_path, cc_opt="-s")
        asm = program_path.with_suffix(".s")

        # compile the assembly code with GCC, run it, and make sure it gives expected result
        actual_result = self.gcc_compile_and_run(asm)
        self.validate_runs(expected_result, actual_result)

        # make sure we actually performed the optimization
        parsed_asm = self.get_target_functions(
            asm, target_fun="target", other_funs=set(["main", "callee"]))

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
        # make sure that we've eliminated all jumps, labels, and function cals
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


class CopyPropTest(OptimizationTest):

    def find_return_value(self, parsed_asm: AssemblyParser.AssemblyFunction) -> Operand:
        # TODO this assumes int return value
        reversed_instrs = list(reversed(parsed_asm.instructions))
        # last instruction should be ret
        last_instruction = reversed_instrs[0]

        def is_ret(i):
            return (isinstance(i, Instruction) and i.mnemonic == Opcode.RET)

        def is_mov_to_eax(i):
            return isinstance(i, Instruction) and i.mnemonic == Opcode.MOV and i.operands[1] == Register.AX

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
            reversed_instrs) if is_mov_to_eax(instr))

        def could_overwrite_eax(i: Union[Label, Instruction]):
            # if this appears after an instruction of the form mov something, eax, could it clobber return value
            if isinstance(i, Label):
                return True  # could jump over mov instruction to reach ret

            if i.mnemonic in [Opcode.CALL, Opcode.JMP, Opcode.JMPCC, Opcode.DIV, Opcode.IDIV]:
                return True

            if destination(i) == Register.AX:
                return True

            return False

        # make sure this is definitely the correct instruction
        clobber_instr = next((could_overwrite_eax(i)
                             for i in reversed_instrs[:retval_idx]), None)
        if clobber_instr:
            raise RuntimeError(
                f"Couldn't find return value: might be clobbered by {clobber_instr} ")

        # now return src of mov instruction; this is our return value
        return retval_instr.operands[0]

    def retval_test(self, expected_retval: int, program_path: Path):

        def validate_return_value(parsed_asm, *, program_path: Path):
            expected_op = Immediate(expected_retval)
            actual_retval = self.find_return_value(parsed_asm)
            self.assertEqual(expected_op, actual_retval,
                             msg=f"Expected {expected_op} as return value, found {actual_retval} ({program_path})")

        self.optimization_test(program_path=program_path,
                               validator=validate_return_value)

    def test_constant_prop(self):
        program_path = self.test_dir / "copy_prop_const_fold.c"

        self.retval_test(6, program_path=program_path)

    def test_fig_20_8(self):
        program_path = self.test_dir / "fig_20_8.c"
        self.retval_test(4, program_path=program_path)
    """
    things we could test with generic "make sure there are no jumps/labels/function calls and exactly one ret":
        - remove unreachable blocks
        - don't remove blocks w/ reachable/unreachable preds (just don't inspect assembly there)
        - empty blocks
        - useless jump
    things we can't:
        dead code inside of loop(need to specify what should be eliminated)
    """
