"""Constant-folding tests"""

from __future__ import annotations

import itertools
from pathlib import Path
from typing import Any, Callable, Iterable

from .. import basic
from ..parser.asm import AsmItem, Label, Opcode
from . import common


class TestConstantFolding(common.TackyOptimizationTest):
    """Test class for constant folding.

    We'll generate a test method for each C program in the chapter19/constant_folding/ directory.
    Each dynamically generated test calls const_fold_test."""

    def const_fold_test(self, program: Path) -> None:
        """Constant folding should eliminate all computations from our test programs

        Won't eliminate prologue, epilogue mov, label, and unconditional jumps"""
        parsed_asm = self.run_and_parse(program)

        def ok(i: AsmItem) -> bool:
            return (
                isinstance(i, Label)
                or common.is_prologue_or_epilogue(i)
                or i.opcode in [Opcode.MOV, Opcode.JMP]
            )

        bad_instructions = [i for i in parsed_asm.instructions if not ok(i)]
        self.assertFalse(
            bad_instructions,
            msg=common.build_msg(
                "Found instructions that should have been constant folded",
                bad_instructions=bad_instructions,
                full_prog=parsed_asm,
                program_path=program,
            ),
        )


def make_constant_fold_test(program: Path) -> Callable[[TestConstantFolding], None]:
    """Generate test method for a single test program."""

    def test(self: TestConstantFolding) -> None:

        self.const_fold_test(program)

    return test


def configure_tests(
    common_attrs: dict[str, Any],
    extra_credit_flags: basic.ExtraCredit,
    int_only: bool,
) -> None:
    """Dynamically add test methods and attributes to TestConstantFolding."""
    dir_under_test = common.TEST_DIR / "constant_folding"
    testclass_attrs = {"test_dir": dir_under_test} | common_attrs

    for k, v in testclass_attrs.items():
        setattr(TestConstantFolding, k, v)

    test_programs: Iterable[Path] = (dir_under_test / "int_only").rglob("*.c")
    if not int_only:
        partii_programs = (dir_under_test / "all_types").rglob("*.c")
        test_programs = itertools.chain(test_programs, partii_programs)

    for program in test_programs:
        if basic.excluded_extra_credit(program, extra_credit_flags):
            continue
        key = program.relative_to(dir_under_test).with_suffix("")
        name = f"test_{key}"
        setattr(TestConstantFolding, name, make_constant_fold_test(program))
