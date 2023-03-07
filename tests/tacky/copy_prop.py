"""Copy propagation tests"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path
from typing import Any, Callable, Iterable, List, Optional, Sequence, Union

from typing_extensions import TypeGuard

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
        Opcode.JMP,
        Opcode.JMPCC,
        Opcode.CMP,
        Opcode.CALL,
        Opcode.RET,
    ]:
        return None
    # otherwise last operand is desintation
    return i.operands[-1]


def is_mov_to(i: asm.AsmItem, r: asm.Register) -> TypeGuard[asm.Instruction]:
    return common.is_mov(i) and i.operands[1] == r


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
        try:
            # find the last instruction before point P
            # that moves a value in register r
            mov_instr_idx, mov_instr = next(
                (idx, instr)
                for (idx, instr) in enumerate(instructions_before_point)
                if is_mov_to(instr, reg)
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
                vals.append(mov_instr.operands[0])
        except StopIteration:
            # couldn't find a mov to this register;
            # sometimes expected one we've implemented coalescing
            vals.append(None)

    return vals


def find_args(
    callee: str, parsed_asm: asm.AssemblyFunction, *, arg_count: int
) -> List[Optional[asm.Operand]]:
    """Determine values in integer parameter-passing registers when function is called"""
    if sys.platform == "darwin":
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

    We'll generate a test method for each C program in the chapter19/copy_propagation/ directory.
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

    def arg_test(self, expected_args: Sequence[Optional[int]], program: Path) -> None:
        """Validate that propagate expected values into function arguments.

        The copy propagation pass should be able to determine the constant values of
        some arguments to the "callee" function. Make sure we move these constants into
        the corresponding parameter passing registers before calling "callee".

        Args:
            * expected_args: expected constant value of each argument
              None if we don't expect to figure this out at compile time
            * program_path: absolute path to source file"""
        expected_ops: List[Optional[asm.Operand]] = [
            asm.Immediate(i) if i else None for i in expected_args
        ]

        parsed_asm = self.run_and_parse(program)

        # we assume that we're looking for arguments to function named "callee"
        actual_args = find_args(
            "callee",
            parsed_asm,
            arg_count=len(expected_args),
        )
        for idx, (actual, expected) in enumerate(
            itertools.zip_longest(actual_args, expected_ops)
        ):
            if expected is not None:
                self.assertEqual(
                    actual,
                    expected,
                    msg=f"Expected argument {idx} to callee to be {expected}, found {actual}",
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
            return common.is_prologue_or_epilogue(i) or (
                isinstance(i, asm.Instruction)
                and i.opcode
                in [
                    Opcode.MOV,
                    Opcode.LEA,
                ]
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
    "complex_const_fold.c": -1,
    "copy_prop_const_fold.c": 6,
    "fig_19_8.c": 4,
    "init_all_copies.c": 3,
    "killed_then_redefined.c": 2,
    "loop.c": 10,
    "multi_path.c": 3,
    "multi_path_no_kill.c": 3,
    "prop_static_var.c": 10,
    "remainder_test.c": 1,
    # other types
    "alias_analysis.c": 24,
    "char_round_trip.c": 1,
    "char_round_trip_2.c": -1,
    "char_type_conversion.c": 1,
    "const_fold_sign_extend.c": -1000,
    "const_fold_sign_extend_2.c": -1000,
    "const_fold_type_conversions.c": 83333,
    "not_char.c": 1,
    "propagate_doubles.c": 3000,
    "propagate_null_pointer.c": 0,
    "signed_unsigned_conversion.c": -11,
    "unsigned_compare.c": 1,
    "unsigned_wraparound.c": 0,
}

# programs we'll validate with arg_test, and their expected arguments
ARG_TESTS = {"propagate_fun_args.c": [None, 20], "kill_and_add_copies.c": [10, None]}

# programs we'll validate with same_arg_test
SAME_ARG_TESTS = [
    "store_doesnt_kill.c",
    "copy_struct.c",
    "multi_instance_same_copy.c",
    "propagate_var.c",
]

# programs we'll validate with redundant_copies_test
REDUNDANT_COPIES_TESTS = ["redundant_copies.c", "redundant_copies_2.c"]

# programs we'll validate with no_computations_test
NO_COMPUTATIONS_TESTS = ["pointer_arithmetic.c"]


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


def configure_tests(
    common_attrs: dict[str, Any],
    extra_credit_flags: basic.ExtraCredit,
    int_only: bool,
) -> None:
    """Dynamically add test methods and attributes to TestCopyProp."""
    dir_under_test = basic.ROOT_DIR / f"chapter{common.CHAPTER}" / "copy_propagation"

    for k, v in common_attrs.items():
        setattr(TestCopyProp, k, v)
    setattr(TestCopyProp, "test_dir", dir_under_test)

    tests: Iterable[Path] = (dir_under_test / "int_only").rglob("*.c")
    if not int_only:
        partii_tests = (dir_under_test / "all_types").rglob("*.c")
        tests = itertools.chain(tests, partii_tests)

    for program in tests:
        if basic.excluded_extra_credit(program, extra_credit_flags):
            continue
        key = program.relative_to(dir_under_test).with_suffix("")
        name = f"test_{key}"

        setattr(TestCopyProp, name, make_copy_prop_test(program))
