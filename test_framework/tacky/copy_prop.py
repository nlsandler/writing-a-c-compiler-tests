"""Copy propagation tests"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Union, Mapping

from .. import basic
from ..parser import asm
from ..parser.asm import Opcode, Register
from . import common


def destination(i: asm.Instruction) -> Optional[asm.Operand]:
    """Get the instruction's destination operand"""
    # no (explicit) destination operand
    if i.opcode in [
        Opcode.PUSH,
        Opcode.CDQ,
        Opcode.CDQE,
        Opcode.JMP,
        Opcode.JMPCC,
        Opcode.CMP,
        Opcode.CALL,
        Opcode.RET,
    ]:
        return None

    if not i.operands:
        return None  # an instruction w/ no operands has no destination
    # otherwise last operand is desintation
    # NOTE: may lead to spurious failures for UNKNOWN instructions
    # that don't actually have destinations
    return i.operands[-1]


def get_src_val(i: asm.AsmItem, r: asm.Register) -> Optional[asm.Operand]:
    """If i sets r to some value, return that value. Otherwise return None."""
    # count xor %r, %r as equivalent to mov $0, %r
    if common.is_zero_instr(i) and i.operands[1] == r:  # type: ignore   # is_zero_instr proves it's an instruction
        return asm.Immediate(0)
    if common.is_mov(i) and i.operands[1] == r:  # type: ignore  # is_mov proves it's an instruction
        return i.operands[0]  # type: ignore  # is_mov proves it's an instruction
    return None


def stops_reaching_copy(i: asm.AsmItem, r: asm.Register) -> bool:
    """Check whether this instruction might prevent copy mov <val>, %r from reaching a later point.

    I.e. if this instruction appears between mov <val>, %r and some point P,
    does that imply that %r may not have value <val> at point P?

    This is much more conservative/less precise than full-blown reaching copies analysis,
    since it only needs to work for the specific arguments and return values we care about
    in our test programs, not for reaching copies in assembly programs in general.
    """

    # We might jump over mov <val>, %r to this label
    if isinstance(i, asm.Label):
        return True

    # function calls can clobber registers
    # jmp means there may not be a path from earlier mov to P
    # conditional jump is fine if there are no intervening labels,
    # (mov would still be on only path to P)
    if i.opcode in [Opcode.CALL, Opcode.JMP]:
        return True

    # div, idiv and cdq clobber specific registers
    if i.opcode in [Opcode.DIV, Opcode.IDIV] and r in [Register.AX, Register.DX]:
        return True

    if i.opcode == Opcode.CDQ and r == Register.DX:
        return True

    if i.opcode == Opcode.CDQE and r == Register.AX:
        return True

    # every instruction clobbers its destination (if it has one)
    if destination(i) == r:
        return True

    return False


def find_reaching_copies(
    parsed_asm: asm.AssemblyFunction,
    *,
    point_reached: asm.AsmItem,
    dest_regs: Sequence[asm.Register],
) -> List[Optional[asm.Operand]]:
    """Determine the values of some registers at a particular point.

    Args:
        parsed_asm: the assembly function to analyze
        point_reached: the label or instruction where we want to know the value of each register
            NOTE: there must be exactly one instance of this label or instruction in the function
        dest_regs: Registers whose values we want to know
    Returns:
        Each register's value, in order; None for any register whose value we couldn't determine
    """
    # TODO test this function
    # make sure point_reached only appears once
    count = parsed_asm.instructions.count(point_reached)
    if count != 1:
        raise RuntimeError(
            f"Expected exactly one instance of {point_reached} but found {count}"
        )

    point_idx = parsed_asm.instructions.index(point_reached)
    # get reversed list of all instructions prior to this point
    instructions_before_point = list(reversed(parsed_asm.instructions[:point_idx]))

    # now determine value of each dest reg
    vals: List[Optional[asm.Operand]] = []
    for reg in dest_regs:
        # find the latest instruction (i.e. first instruction in reversed list)
        # that moves a value into this register (or, equivalently, zeros it out)
        maybe_movs = enumerate(get_src_val(i, reg) for i in instructions_before_point)
        try:
            mov_instr_idx, mov_src = next(
                (idx, op) for (idx, op) in maybe_movs if op is not None
            )
            # are there any instructions between mov_instr and point P
            # that might prevent mov_instr from reaching P?
            if any(
                stops_reaching_copy(instr, reg)
                for instr in instructions_before_point[:mov_instr_idx]
            ):
                # mov_instr might not reach point P, so we can't determine the register's value
                vals.append(None)
            else:
                # mov_instr reaches P, so r will still have the value we moved into it at this point
                vals.append(mov_src)
        except StopIteration:
            # didn't find an instruction that sets this register
            vals.append(None)

    return vals


def find_args(
    callee: str, parsed_asm: asm.AssemblyFunction, *, arg_count: int
) -> List[Optional[asm.Operand]]:
    """Determine values in integer parameter-passing registers when function is called"""
    if basic.IS_OSX:
        callee = "_" + callee
    call_instruction = asm.Instruction(Opcode.CALL, [callee])
    arg_regs = [
        Register.DI,
        Register.SI,
        Register.DX,
        Register.CX,
        Register.R8,
        Register.R9,
    ]
    return find_reaching_copies(
        parsed_asm, point_reached=call_instruction, dest_regs=arg_regs[:arg_count]
    )


class TestCopyProp(common.TackyOptimizationTest):
    """Test class for copy propagation.

    We'll generate a test method for each C program in the chapter_19/copy_propagation/ directory.
    Each dynamically generated test calls one of the following main test methods:

    * compile_and_run, defined in TestChapter: Validate behavior but don't inspect assembly.
    * retval_test: make sure we propagated expected constant or static variable into return statement
    * arg_test: make sure we propaged expected constants as arguments to some function call
    * same_arg_test: make sure we propagate same value as first and second argument to some function
    * redundant_copies_test: make sure we eliminate redundant copies
      (where the source and destination already have the same value)
    * no_computations_test: make sure that copy propagation, in conjunction with prior
      optimizations, allows us to eliminate all computations (e.g. arithmetic and type conversions)
    """

    test_dir = common.TEST_DIR / "copy_propagation"

    def retval_test(self, expected_retval: Union[int, str], program_path: Path) -> None:
        """Validate that we propagate the expected value into return statement.

        The copy propagation pass should be able to determine which constant or
        static variable this function will return. Make sure we move the expected value
        into the EAX register before the ret instruction.

        Args:
            * expected_retval: constant or variable name
                e.g. 'foo' if returned operand should be foo(%rip)
            * program_path: absolute path to source file
        """
        expected_op: asm.Operand
        if isinstance(expected_retval, int):
            expected_op = asm.Immediate(expected_retval)
        else:
            if sys.platform == "darwin":
                expected_op = "_" + expected_retval
            expected_op = asm.Memory(
                disp=[expected_retval], base=Register.IP, idx=None, scale=1
            )

        parsed_asm = self.run_and_parse(program_path)
        # find the value in EAX when the function returns
        retval_result = find_reaching_copies(
            parsed_asm,
            point_reached=asm.Instruction(Opcode.RET, []),
            dest_regs=[Register.AX],
        )
        actual_retval = retval_result[0]
        self.assertEqual(
            expected_op,
            actual_retval,
            msg=f"Expected {expected_op} as return value, found {actual_retval} ({program_path})",
        )

    def arg_test(
        self, expected_args: Mapping[str, Sequence[Optional[int]]], program: Path
    ) -> None:
        """Validate that we propagate expected values into function arguments.

        The copy propagation pass should be able to determine the constant values of
        some arguments to some function calls. Make sure we move these constants into
        the corresponding parameter passing registers before calling those functions.

        Args:
            * expected_args: mapping from function names to expected constant
              value of each argument.
              An argument's value is None if we don't expect to know it at compile time.
            * program_path: absolute path to source file
        """

        # convert constants to assembly operands
        expected_ops: Mapping[str, List[Optional[asm.Operand]]] = {
            f: [asm.Immediate(i) if i else None for i in args]
            for f, args in expected_args.items()
        }

        parsed_asm = self.run_and_parse(program)

        # validate the args to each function call
        # assume that each function is called only once in 'target'
        for f, expected_f_args in expected_ops.items():
            actual_args = find_args(
                f,
                parsed_asm,
                arg_count=len(expected_f_args),
            )
            for idx, (actual, expected) in enumerate(
                itertools.zip_longest(actual_args, expected_f_args)
            ):
                if expected is not None:
                    self.assertEqual(
                        actual,
                        expected,
                        msg=f"Expected argument {idx} to {f} to be {expected}, found {actual}",
                    )

    def same_arg_test(self, program: Path) -> None:
        """Test that first and second arguments to callee are the same."""

        parsed_asm = self.run_and_parse(program)

        # assume the name of the function we're interested in is "callee"
        actual_args = find_args("callee", parsed_asm, arg_count=2)
        # they're the same value if:
        # same value moved into EDI and ESI, or
        # EDI is moved into ESI, or
        # ESI is moved into EDI
        same_value = (
            (actual_args[0] is not None and actual_args[0] == actual_args[1])
            or actual_args[0] == Register.SI
            or actual_args[1] == Register.DI
        )
        self.assertTrue(
            same_value,
            msg=f"Bad arguments {actual_args[0]} and {actual_args[1]} to callee: \
                both args should have same value",
        )

    def redundant_copies_test(self, program: Path) -> None:
        """Test that we eliminate redundant copy instructions.

        We use this for test programs where a redundant copy is in a branch by itself;
        to confirm that we've removed these redundant copies, make sure the optimized program
        has no control-flow instructions.
        """
        parsed_asm = self.run_and_parse(program)

        control_flow_instructions = [
            i for i in parsed_asm.instructions if common.is_control_flow(i)
        ]
        self.assertFalse(
            control_flow_instructions,
            msg=common.build_msg(
                "Found control-flow instructions for branch that should be dead",
                bad_instructions=control_flow_instructions,
                full_prog=parsed_asm,
                program_path=program,
            ),
        )

    def no_computations_test(self, program_path: Path) -> None:
        """Copy propagation and constant folding together should eliminate all computations.

        The compiled assembly code will still contain mov and lea instructions and the function
        prologue and epilogue, but nothing else.
        """

        parsed_asm = self.run_and_parse(program_path)

        def ok(i: asm.AsmItem) -> bool:
            return (
                common.is_prologue_or_epilogue(i)
                or common.is_zero_instr(i)
                or (
                    isinstance(i, asm.Instruction)
                    and i.opcode
                    in [
                        Opcode.MOV,
                        Opcode.LEA,
                    ]
                )
            )

        bad_instructions = [i for i in parsed_asm.instructions if not ok(i)]
        self.assertFalse(
            bad_instructions,
            msg=common.build_msg(
                "Found instructions that should have been optimized out",
                bad_instructions=bad_instructions,
                full_prog=parsed_asm,
                program_path=program_path,
            ),
        )


# programs we'll validate with retval_test, and their expected return values
RETVAL_TESTS = {
    # int-only
    "constant_propagation.c": 6,
    "propagate_into_complex_expressions.c": 25,
    "fig_19_8.c": 4,
    "init_all_copies.c": 3,
    "killed_then_redefined.c": 2,
    "different_paths_same_copy.c": 3,
    "multi_path_no_kill.c": 3,
    "propagate_static.c": 10,
    "goto_define.c": 20,
    "propagate_from_default.c": 3,
    # other types
    "alias_analysis.c": 24,
    "propagate_into_type_conversions.c": 83826,
    "propagate_all_types.c": 3500,
    "propagate_null_pointer.c": 0,
    "funcall_kills_aliased.c": 10,
}

# programs we'll validate with arg_test, and mappings to callees with their expected arguments
ARG_TESTS: dict[str, dict[str, list[Optional[int]]]] = {
    "kill_and_add_copies.c": {"callee": [10, None]},
    "propagate_into_case.c": {"callee": [10]},
    "nested_loops.c": {
        "inner_loop1": [None, None, None, None, None, 100],
        "inner_loop2": [None, None, None, None, None, 100],
        "inner_loop3": [None, None, None, None, None, 100],
        "validate": [None, None, None, None, None, 100],
    },
}

# programs we'll validate with same_arg_test
SAME_ARG_TESTS = [
    # int only
    "different_source_values_same_copy.c",
    "propagate_static_var.c",
    "propagate_var.c",
    "propagate_params.c",
    "prefix_result.c",
    # other types
    "store_doesnt_kill.c",
    "copy_struct.c",
    "char_type_conversion.c",
    "copy_union.c",
]

# programs we'll validate with redundant_copies_test
REDUNDANT_COPIES_TESTS = [
    # int only
    "redundant_copies.c",
    # other types
    "redundant_double_copies.c",
    "redundant_struct_copies.c",
    "redundant_nan_copy.c",
    "redundant_union_copy.c",
]

# programs we'll validate with no_computations_test
NO_COMPUTATIONS_TESTS = [
    "pointer_arithmetic.c",
    "pointer_incr.c",
    "pointer_compound_assignment.c",
]


def make_copy_prop_test(program: Path) -> Callable[[TestCopyProp], None]:
    """Generate test method for a single test program."""
    if "dont_propagate" in program.parts:
        return basic.make_test_run(program)

    if program.name in RETVAL_TESTS:
        expected_retval = RETVAL_TESTS[program.name]

        def test(self: TestCopyProp) -> None:
            self.retval_test(expected_retval, program)

    elif program.name in ARG_TESTS:
        expected_args = ARG_TESTS[program.name]

        def test(self: TestCopyProp) -> None:
            self.arg_test(expected_args, program)

    elif program.name in SAME_ARG_TESTS:

        def test(self: TestCopyProp) -> None:
            self.same_arg_test(program)

    elif program.name in REDUNDANT_COPIES_TESTS:

        def test(self: TestCopyProp) -> None:
            self.redundant_copies_test(program)

    elif program.name in NO_COMPUTATIONS_TESTS:

        def test(self: TestCopyProp) -> None:
            self.no_computations_test(program)

    else:
        raise RuntimeError(f"Don't know how to handle {program.name}")

    test.__doc__ = str(program)

    return test
