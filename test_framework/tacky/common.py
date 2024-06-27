"""Base class for TACKY optimization tests"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Sequence


from .. import basic
from ..parser import asm, parse
from ..parser.asm import Opcode, Register

CHAPTER = 19
TEST_DIR = basic.TEST_DIR / f"chapter_{CHAPTER}"


class TackyOptimizationTest(basic.TestChapter):

    """Base class for TACKY (chapter 19) tests.

    There are two kinds of tests for these chapters. The first is the same kind of test we use
    in Parts I & II: we compile the test program, run it, and make sure it has the correct
    observable behavior. These test methods should call compile_and_run, defined in TestChapter.

    In the second kind of test, we still compile the program, run it, and validate its behavior,
    but we also inspect its assembly code to make sure it's been optimized. These test methods
    should call run_and_parse or run_and_parse_all, defined below.

    This class defines two test methods used in dead store elimination and whole pipeline tests:
    * store_eliminated_test: Test that stores of particular constants were eliminated
    * return_const_test: Test that the only thing this function does is return a specific consatnt

    Notes:
    * This class isn't designed to test intermediate stages
        (i.e. exit_stage should always be "run").
        TODO enforce this?
    * There are no invalid test programs for this chapter
    """

    def run_and_parse_all(self, source_file: Path) -> dict[str, asm.AssemblyFunction]:
        """Compile and run a program, validate result, then return parsed assembly.

        The caller can then perform additional validation on the parsed assembly.

        Args:
            program_path: Absolute path to test program

        Returns: parsed assembly code for whole program
        """

        # first compile to assembly
        compile_result = self.invoke_compiler(source_file, cc_opt="-s")
        self.assertEqual(
            compile_result.returncode,
            0,
            msg=f"compilation of {source_file} failed with error:\n{compile_result.stderr}",
        )
        basic.print_stderr(
            compile_result
        )  # print compiler warnings even if it succeeded
        asm_file = source_file.with_suffix(".s")
        libs = basic.get_libs(source_file)
        # assemble/link asm_file, run it, and make sure it gives expected result
        actual_result = basic.gcc_compile_and_run([asm_file] + libs, [])
        self.validate_runs(source_file, actual_result)

        # now parse the assembly file and extract the function named "target"
        return parse.parse_file(asm_file)

    def run_and_parse(self, source_file: Path) -> asm.AssemblyFunction:
        """Compile and run a program, validate result, then return parsed assembly for 'target' function.

        The caller can then perform additional validation on the parsed assembly.

        Args:
            program_path: Absolute path to test program

        Returns: parsed assembly code for whole program
        """
        return self.run_and_parse_all(source_file)["target"]

    # methods used by dead store elimination and whole pipeline tests
    def store_eliminated_test(
        self, *, source_file: Path, redundant_consts: List[int]
    ) -> None:
        """Make sure any stores of the form mov $const, <something> were eliminated.

        The test program should contain a single 'target' function.
        Args:
            source_file: absolute path to program under test
            redundant_consts: any constants that were sources of mov instructions in the
                original program but shouldn't be after dead store elimination
        """
        redundant_operands = [asm.Immediate(c) for c in redundant_consts]

        def is_dead_store(i: asm.AsmItem) -> bool:
            # returns true if we find _any_ instruction where redundant_const is source operand
            # this is more general than just looking for mov so we'll also catch any
            # spurious copy propagation of this constant
            return (
                isinstance(i, asm.Instruction)
                and bool(i.operands)
                and i.operands[0] in redundant_operands
            )

        parsed_asm = self.run_and_parse(source_file)

        bad_instructions = [i for i in parsed_asm.instructions if is_dead_store(i)]
        self.assertFalse(
            bad_instructions,
            msg=build_msg(
                "Found dead store that should have been eliminated",
                bad_instructions=bad_instructions,
                full_prog=parsed_asm,
                program_path=source_file,
            ),
        )

    def return_const_test(self, *, source_file: Path, returned_const: int) -> None:
        """Validate that the function doesn't do anything except return a constant.

        The test program should contain a single 'target' function.
        """

        def ok(i: asm.AsmItem) -> bool:
            """We should optimize out everything except prologue, epilogue, and mov into EAX"""
            if is_prologue_or_epilogue(i):
                return True

            # only okay instruction is mov $return_const, %eax (or %rax, we don't distinguish)
            if i == asm.Instruction(
                asm.Opcode.MOV, [asm.Immediate(returned_const), asm.Register.AX]
            ):
                return True

            # if retval is 0, also accept xor %eax, %eax
            if returned_const == 0 and i == asm.Instruction(
                asm.Opcode.XOR, [asm.Register.AX, asm.Register.AX]
            ):
                return True
            return False

        parsed_asm = self.run_and_parse(source_file)

        bad_instructions = [i for i in parsed_asm.instructions if not ok(i)]
        self.assertFalse(
            bad_instructions,
            msg=build_msg(
                "Found instruction that should have been optimized out",
                bad_instructions=bad_instructions,
                full_prog=parsed_asm,
                program_path=source_file,
            ),
        )


def build_msg(
    msg: str,
    *,
    bad_instructions: Optional[Sequence[asm.AsmItem]] = None,
    full_prog: Optional[asm.AssemblyFunction] = None,
    program_path: Optional[Path] = None,
) -> str:
    """Utility function for validators to report invalid assembly code"""
    msg_lines = [msg]
    if bad_instructions:
        printed_instructions = [str(i) for i in bad_instructions]
        msg_lines.append("Bad instructions:")
        msg_lines.extend(printed_instructions)
    if full_prog:
        msg_lines.extend(["Complete program:", str(full_prog)])
    if program_path:
        msg_lines.append(f"Program: {program_path}")
    return "\n".join(msg_lines)


# Utilties for validating parsed assembly
def is_prologue_or_epilogue(i: asm.AsmItem) -> bool:
    """Is this an instruction you might find in the function prologue or epilogue?

    These will be present even when everything else was optimized out."""
    if isinstance(i, asm.Label):
        return False

    return (
        is_ret(i)
        or (i.opcode in [Opcode.PUSH, Opcode.POP] and i.operands[0] == Register.BP)
        or (i.opcode == Opcode.SUB and i.operands[1] == Register.SP)
        or (
            i.opcode == Opcode.MOV
            and all(o in [Register.SP, Register.BP] for o in i.operands)
        )
    )


def is_control_flow(i: asm.AsmItem) -> bool:
    return isinstance(i, asm.Label) or i.opcode in [
        Opcode.JMP,
        Opcode.JMPCC,
        Opcode.CALL,
        Opcode.CMOV,
    ]


def is_ret(i: asm.AsmItem) -> bool:
    return isinstance(i, asm.Instruction) and i.opcode in [Opcode.RET, Opcode.LEAVE]


def is_mov(i: asm.AsmItem) -> bool:
    return isinstance(i, asm.Instruction) and i.opcode == Opcode.MOV


def is_zero_instr(i: asm.AsmItem) -> bool:
    """Is this an instruction of the form xor %reg, %reg used to zero out a register?"""
    return (
        isinstance(i, asm.Instruction)
        and i.opcode == Opcode.XOR
        and i.operands[0] == i.operands[1]
    )
