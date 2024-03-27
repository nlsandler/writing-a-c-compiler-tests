"""Constant-folding tests"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from ..parser.asm import AsmItem, Label, Opcode
from . import common


class TestConstantFolding(common.TackyOptimizationTest):
    """Test class for constant folding.

    We'll generate a test method for each C program in the chapter_19/constant_folding/ directory.
    Each dynamically generated test calls const_fold_test."""

    test_dir = common.TEST_DIR / "constant_folding"

    def const_fold_test(self, program: Path) -> None:
        """Constant folding should eliminate all computations from our test programs

        Won't eliminate prologue, epilogue mov, label, and unconditional jumps"""
        parsed_asm = self.run_and_parse_all(program)

        def ok(i: AsmItem) -> bool:
            return (
                isinstance(i, Label)
                or common.is_prologue_or_epilogue(i)
                or i.opcode in [Opcode.MOV, Opcode.JMP]
                # xor %r, %r is okay bcause it's equivalent to mov $0, %r
                or common.is_zero_instr(i)
            )

        for fn_name, fn_body in parsed_asm.items():
            if fn_name.startswith("target"):
                bad_instructions = [i for i in fn_body.instructions if not ok(i)]
                self.assertFalse(
                    bad_instructions,
                    msg=common.build_msg(
                        "Found instructions that should have been constant folded",
                        bad_instructions=bad_instructions,
                        full_prog=fn_body,
                        program_path=program,
                    ),
                )


def make_constant_fold_test(program: Path) -> Callable[[TestConstantFolding], None]:
    """Generate test method for a single test program."""

    def test(self: TestConstantFolding) -> None:
        self.const_fold_test(program)

    return test
