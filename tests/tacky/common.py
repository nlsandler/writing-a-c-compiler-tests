"""Base class for TACKY optimization tests"""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence

from typing_extensions import TypeGuard

from .. import basic
from ..parser import asm, parse
from ..parser.asm import Opcode, Register

CHAPTER = 20  # TODO update chapter number
TEST_DIR = basic.ROOT_DIR / f"chapter{CHAPTER}"


class TackyOptimizationTest(basic.TestChapter):

    """Base class for TACKY (chapter 19) tests.

    There are two kinds of tests for these chapters. The first is the same kind of test we use
    in Parts I & II: we compile the test program, run it, and make sure it has the correct
    observable behavior. These test methods should call compile_and_run, defined in TestChapter.

    In the second kind of test, we still compile the program, run it, and validate its behavior,
    but we also inspect its assembly code to make sure it's been optimized. These test methods
    should call run_and_parse, defined below.

    Notes:
    * This class isn't designed to test intermediate stages
        (i.e. exit_stage should always be "run").
        TODO enforce this?
    * There are no invalid test programs for this chapter
    """

    def run_and_parse(self, source_file: Path) -> asm.AssemblyFunction:
        """Compile and run a program, validate result, then return parsed assembly.

        The caller can then perform additional validation on the parsed assembly.
        NOTE: The name of the relevant function must be "target"

        Args:
            program_path: Absolute path to test program

        Returns: parsed assembly code for "target"
        """

        # first compile to assembly
        compile_result = self.invoke_compiler(source_file, cc_opt="-s")
        self.assertEqual(
            compile_result.returncode,
            0,
            msg=f"compilation of {source_file} failed with error:\n{compile_result.stderr}",
        )
        asm_file = source_file.with_suffix(".s")

        # assemble/link asm_file, run it, and make sure it gives expected result
        actual_result = self.gcc_compile_and_run(asm_file)
        self.validate_runs(source_file, actual_result)

        # now parse the assembly file and extra the function named "target"
        return parse.parse_target_function(asm_file, target_fun="target")


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
    ]


def is_ret(i: asm.AsmItem) -> bool:
    return isinstance(i, asm.Instruction) and i.opcode in [Opcode.RET, Opcode.LEAVE]


def is_mov(i: asm.AsmItem) -> TypeGuard[asm.Instruction]:
    return isinstance(i, asm.Instruction) and i.opcode == Opcode.MOV
