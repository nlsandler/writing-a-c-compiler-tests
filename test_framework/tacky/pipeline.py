"""Tests for whole compiler pipeline"""

from pathlib import Path
from typing import Callable, List

from ..basic import IS_OSX
from ..parser.asm import (
    AsmItem,
    Opcode,
    Label,
    Immediate,
    Memory,
    Register,
    Instruction,
)
from . import common


class TestWholePipeline(common.TackyOptimizationTest):
    """Test cases for whole pipeline
    Run tests in whole_pipeline subdirectory but use same logic as dead store elimination tests.
    """

    test_dir = common.TEST_DIR / "whole_pipeline"

    def fold_const_test(self, *, source_file: Path) -> None:
        """Constant folding should eliminate all computations from the target_* functions

        Similar to TackyOptimizationTest::return_const_test
        but we allow any immediate (or RIP-relative operand, in case its a double)
        rather than requiring a specific immediate
        """

        parsed_asm = self.run_and_parse_all(source_file)

        def ok(i: AsmItem) -> bool:
            if common.is_prologue_or_epilogue(i):
                return True

            # zeroing out EAX with xor is okay
            if i == Instruction(Opcode.XOR, [Register.AX, Register.AX]):
                return True

            if isinstance(i, Label) or i.opcode != Opcode.MOV:
                return False  # aside from prologue/epilogue or zeroing EAX, only mov allowed

            # can only mov into return register
            src, dst = i.operands[0], i.operands[1]
            if dst not in [Register.XMM0, Register.AX]:
                return False

            # source must be immediate or RIP-relative
            if isinstance(src, Immediate):
                return True

            if isinstance(src, Memory) and src.base == Register.IP:
                return True

            # source isn't immediate or RIP-relative
            return False

        for fn_name, fn_body in parsed_asm.items():
            if fn_name.startswith("target"):
                bad_instructions = [i for i in fn_body.instructions if not ok(i)]
                self.assertFalse(
                    bad_instructions,
                    msg=common.build_msg(
                        "Found instructions that should have been constant folded",
                        bad_instructions=bad_instructions,
                        full_prog=fn_body,
                        program_path=source_file,
                    ),
                )

    def global_store_eliminated_test(
        self, *, source_file: Path, redundant_instructions: List[Instruction]
    ) -> None:
        """Make sure any stores of the form mov $const, $var(%rip) were eliminated.

        The test program should contain a single 'target' function.
        Args:
            source_file: absolute path to program under test
            redundant_instructions: instructions that would appear in the original program
            but shouldn't appear after optimization

        TODO consider refactoring to combine with store_eliminated_test in common.py
        """

        def is_dead_store(i: AsmItem) -> bool:
            # returns true if we find _any_ instruction where redundant_const is source operand
            # this is more general than just looking for mov so we'll also catch any
            # spurious copy propagation of this constant
            return isinstance(i, Instruction) and i in redundant_instructions

        parsed_asm = self.run_and_parse(source_file)

        bad_instructions = [i for i in parsed_asm.instructions if is_dead_store(i)]
        self.assertFalse(
            bad_instructions,
            msg=common.build_msg(
                "Found dead store to global variable that should have been eliminated",
                bad_instructions=bad_instructions,
                full_prog=parsed_asm,
                program_path=source_file,
            ),
        )


RETVAL_TESTS = {
    # Part I
    "dead_condition.c": 10,
    "elim_and_copy_prop.c": 10,
    "remainder_test.c": 1,
    "listing_19_5.c": 9,
    "int_min.c": -2147483648,
    # Part II
    "listing_19_5_more_types.c": 9,
    "integer_promotions.c": 0,
}
STORE_ELIMINATED = {"alias_analysis_change.c": [5, 10]}

globvar = "glob"
if IS_OSX:
    globvar = "_" + globvar
GLOBAL_STORE_ELIMINATED = {
    "propagate_into_copytooffset.c": [
        Instruction(Opcode.MOV, [Immediate(30), Memory([globvar], Register.IP, None)])
    ]
}
FOLD_CONST_TESTS = {
    "fold_cast_to_double.c",
    "fold_cast_from_double.c",
    "fold_negative_zero.c",
    "fold_infinity.c",
    "fold_negative_values.c",
    "signed_unsigned_conversion.c",
    "fold_char_condition.c",
    "fold_extension_and_truncation.c",
}


def make_whole_pipeline_test(program: Path) -> Callable[[TestWholePipeline], None]:
    if program.name in RETVAL_TESTS:
        expected_retval = RETVAL_TESTS[program.name]

        def test(self: TestWholePipeline) -> None:
            self.return_const_test(source_file=program, returned_const=expected_retval)

    elif program.name in STORE_ELIMINATED:
        consts = STORE_ELIMINATED[program.name]

        def test(self: TestWholePipeline) -> None:
            self.store_eliminated_test(source_file=program, redundant_consts=consts)

    elif program.name in GLOBAL_STORE_ELIMINATED:
        instrs = GLOBAL_STORE_ELIMINATED[program.name]

        def test(self: TestWholePipeline) -> None:
            self.global_store_eliminated_test(
                source_file=program, redundant_instructions=instrs
            )

    elif program.name in FOLD_CONST_TESTS:

        def test(self: TestWholePipeline) -> None:
            self.fold_const_test(source_file=program)

    else:
        raise RuntimeError(f"Don't know what to do with {program.name}")

    return test
