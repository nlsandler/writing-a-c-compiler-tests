"""Tests for whole compiler pipeline"""

from pathlib import Path
from typing import Callable, List

from ..basic import IS_OSX, make_test_run
from ..parser.asm import (
    AsmItem,
    Operand,
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

    def global_var_unused_test(self, *, source_file: Path, unused_var: str) -> None:
        """
        Make sure all uses of $var(%rip) are eliminated (because we propagated
        the value that was copied to it into all its uses). Writes *to* var may still be present.

        The test program should contain a single 'target' function.

        Args:
            source_file: absolute path to program under test
            unused_var: var that shouldn't be used in target
        """

        if IS_OSX:
            objname = "_" + unused_var
        else:
            objname = unused_var

        def is_unused_op(o: Operand) -> bool:
            """x(%rip) and x+4(%rip) both count as operands we shouldn't use"""
            if (
                isinstance(o, Memory)
                and o.base == Register.IP
                and o.disp is not None  # to make mypy happy
                and objname in o.disp
            ):
                return True
            return False

        def is_use_of_var(i: AsmItem) -> bool:
            """Is this an instruction that uses unused_op?"""
            if isinstance(i, Instruction) and any(is_unused_op(o) for o in i.operands):
                # okay only if this is move _to_ (not from) op
                if common.is_mov(i) and not is_unused_op(i.operands[0]):
                    return False
                return True

            return False

        parsed_asm = self.run_and_parse(source_file)

        bad_instructions = [i for i in parsed_asm.instructions if is_use_of_var(i)]
        self.assertFalse(
            bad_instructions,
            msg=common.build_msg(
                "Found use of global variable that should have been eliminated",
                bad_instructions=bad_instructions,
                full_prog=parsed_asm,
                program_path=source_file,
            ),
        )

    def instruction_eliminated_test(
        self, *, source_file: Path, redundant_instructions: List[Instruction]
    ) -> None:
        """Make sure specified instructions were eliminated.

        The test program should contain a single 'target' function.
        We use this to detect instructions with constant and global RIP-relative operands
        since we can't predict the exact location of operands on the stack
        Args:
            source_file: absolute path to program under test
            redundant_instructions: instructions that would appear in the original program
            but shouldn't appear after optimization

        TODO consider refactoring to combine with store_eliminated_test in common.py
        """

        parsed_asm = self.run_and_parse(source_file)

        bad_instructions = [
            i
            for i in parsed_asm.instructions
            if isinstance(i, Instruction) and i in redundant_instructions
        ]
        self.assertFalse(
            bad_instructions,
            msg=common.build_msg(
                "Found instruction that should have been eliminated",
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
    "fold_negative_bitshift.c": -2500,
    "fold_incr_and_decr.c": 0,
    "fold_compound_assignment.c": 0,
    "fold_bitwise_compound_assignment.c": 0,
    "evaluate_switch.c": 0,
    # Part II
    "fold_negative_long_bitshift.c": -262144,
    "listing_19_5_more_types.c": 9,
    "integer_promotions.c": 0,
    "nan.c": 0,
    "fold_incr_decr_doubles.c": 0,
    "fold_incr_decr_unsigned.c": 0,
    "fold_incr_decr_chars.c": 0,
    "eval_nan_condition.c": 0,
}
STORE_ELIMINATED = {"alias_analysis_change.c": [5, 10]}


def mk_globvar(varname: str) -> Memory:
    """Given a variable name x, construct the operand x(%rip), accounting for name mangling"""
    if IS_OSX:
        objname = "_" + varname
    else:
        objname = varname
    return Memory([objname], Register.IP, None)


# tests where copy prop should allow us to eliminate a store
# of a specific constant to a specific global variable;
# can't use STORE_ELIMINATED because that constant will
# still be written to other location
GLOBAL_STORE_ELIMINATED = {
    "propagate_into_copytooffset.c": [
        Instruction(Opcode.MOV, [Immediate(30), mk_globvar("glob")])
    ],
    "propagate_into_store.c": [
        Instruction(Opcode.MOV, [Immediate(30), mk_globvar("glob")])
    ],
}

# tests where copy prop lets us eliminate all uses of a particular
# global variable, but not writes to that variable
GLOBAL_VAR_USE_ELIMINATED = {
    "propagate_into_copyfromoffset.c": "glob",
    "propagate_into_load.c": "glob",
}

# Test programs we can constant fold down to a single return statement
FOLD_CONST_TESTS = {
    "fold_cast_to_double.c",
    "fold_cast_from_double.c",
    "fold_negative_zero.c",
    "fold_infinity.c",
    "fold_negative_values.c",
    "signed_unsigned_conversion.c",
    "fold_char_condition.c",
    "fold_extension_and_truncation.c",
    "fold_compound_assign_all_types.c",
    "fold_compound_bitwise_assign_all_types.c",
    "return_nan.c",
}

# Tests we're just checking for correct behavior rather than inspecting
# assembly
BASIC_TESTS = {"compound_assign_exceptions.c"}


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
            self.instruction_eliminated_test(
                source_file=program, redundant_instructions=instrs
            )

    elif program.name in GLOBAL_VAR_USE_ELIMINATED:
        v = GLOBAL_VAR_USE_ELIMINATED[program.name]

        def test(self: TestWholePipeline) -> None:
            self.global_var_unused_test(source_file=program, unused_var=v)

    elif program.name in FOLD_CONST_TESTS:

        def test(self: TestWholePipeline) -> None:
            self.fold_const_test(source_file=program)

    elif program.name in BASIC_TESTS:
        return make_test_run(program)

    else:
        raise RuntimeError(f"Don't know what to do with {program.name}")

    return test
