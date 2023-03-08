"""Dead store elimination tests."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from .. import basic
from ..parser import asm
from . import common


class TestDeadStoreElimination(common.TackyOptimizationTest):

    """Test cases for dead store elimination.


    We'll generate a test method for each C program in the chapter19/dead_store_elimination/ directory.
    Each dynamically generated test calls one of the following main test methods:

    * compile_and_run, defined in TestChapter: validate behavior but don't inspect assembly
    * store_eliminated_test: make sure a particular mov instrucion was eliminated
    * return_const_test: make sure entire funcion is reduce to a return instruction
    """

    test_dir = common.TEST_DIR / "dead_store_elimination"

    def store_eliminated_test(self, *, source_file: Path, redundant_const: int) -> None:
        """Make sure a dead store of the form mov $redundant_const, <something> was eliminated."""

        def is_dead_store(i: asm.AsmItem) -> bool:

            # returns true if we find _any_ instruction where redundant_const is source operand
            # this is more general than just looking for mov so we'll also catch any
            # spurious copy propagation of this constant
            return (
                isinstance(i, asm.Instruction)
                and bool(i.operands)
                and i.operands[0] == asm.Immediate(redundant_const)
            )

        parsed_asm = self.run_and_parse(source_file)

        bad_instructions = [i for i in parsed_asm.instructions if is_dead_store(i)]
        self.assertFalse(
            bad_instructions,
            msg=common.build_msg(
                "Found dead store that should have been eliminated",
                bad_instructions=bad_instructions,
                full_prog=parsed_asm,
                program_path=source_file,
            ),
        )

    def return_const_test(self, *, source_file: Path, returned_const: int) -> None:
        """Validate that the function doesn't do anything except return a constant."""

        def ok(i: asm.AsmItem) -> bool:
            """We should optimize out everything except prologue, epilogue, and mov into EAX"""
            if common.is_prologue_or_epilogue(i):
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
            msg=common.build_msg(
                "Found instruction that should have been optimized out",
                bad_instructions=bad_instructions,
                full_prog=parsed_asm,
                program_path=source_file,
            ),
        )


# programs to validate with store_eliminated_test, and the constants that should be eliminated
STORE_ELIMINATED = {
    # int-only
    "dead_store_static_var.c": 5,
    "elim_second_copy.c": 10,
    "fig_19_12.c": 10,
    "loop_dead_store.c": 5,
    "simple.c": 10,
    # other types
    "aliased_dead_at_exit.c": 50,
    "copy_to_dead_struct.c": 10,
    "getaddr_doesnt_gen.c": 4,
}

# programs to validate with return_const_test, with expected return value
RETURN_CONST = {
    "use_and_kill.c": 5,
}


def make_dse_test(program: Path) -> Callable[[TestDeadStoreElimination], None]:
    """Generate test method for one test program."""

    if "dont_elim" in program.parts:
        return basic.make_test_run(program)

    if program.name in STORE_ELIMINATED:
        redundant_const = STORE_ELIMINATED[program.name]

        def test(self: TestDeadStoreElimination) -> None:
            self.store_eliminated_test(
                source_file=program, redundant_const=redundant_const
            )

    elif program.name in RETURN_CONST:
        returned_constant = RETURN_CONST[program.name]

        def test(self: TestDeadStoreElimination) -> None:
            self.return_const_test(
                source_file=program, returned_const=returned_constant
            )

        test.__doc__ = str(program)
    else:
        raise RuntimeError(f"Don't know what to do with {program.name}")

    return test
