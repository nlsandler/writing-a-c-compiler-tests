"""Tests for unreachable code elimination"""

from pathlib import Path
from typing import Callable

from .. import basic
from ..parser import asm
from ..parser.asm import Opcode
from . import common


class TestUnreachableCodeElim(common.TackyOptimizationTest):
    test_dir = common.TEST_DIR / "unreachable_code_elimination"

    def no_control_flow_test(self, program: Path) -> None:
        parsed_asm = self.run_and_parse(program)

        # first validate that there's exactly one ret instruction
        ret_instruction_count = sum(
            1 for i in parsed_asm.instructions if common.is_ret(i)
        )
        self.assertLessEqual(
            ret_instruction_count,
            1,
            msg=f"Expected at most one ret instruction, but found {ret_instruction_count}",
        )

        # now validate that we've eliminated all control-flow instructions
        # including jumps, labels, function calls
        # (in these tests function calls only show up in dead code)
        useless_instructions = [
            i for i in parsed_asm.instructions if common.is_control_flow(i)
        ]
        self.assertFalse(
            useless_instructions,
            msg=common.build_msg(
                "Found instructions that should have been eliminated",
                bad_instructions=useless_instructions,
                full_prog=parsed_asm,
                program_path=program,
            ),
        )

    def no_function_calls_test(self, program_path: Path) -> None:
        """Validate that there are no call instructions, but allow other control flow"""

        parsed_asm = self.run_and_parse(program_path)

        def is_funcall(i: asm.AsmItem) -> bool:
            if isinstance(i, asm.Instruction) and i.opcode == Opcode.CALL:
                return True
            return False

        funcalls = [i for i in parsed_asm.instructions if is_funcall(i)]
        self.assertFalse(
            funcalls,
            msg=common.build_msg(
                "Found instructions that should have been eliminated",
                bad_instructions=funcalls,
                full_prog=parsed_asm,
                program_path=program_path,
            ),
        )


# unreachable cdoe elimination removes function calls but not other
# control flow instructions for these programs
NO_FUNCALLS_TESTS = [
    "dead_branch_inside_loop.c",
    "dead_after_if_else.c",
    "dead_before_first_switch_case.c",
    "dead_in_switch_body.c",
]

# don't inspect assembly for this program, just validate its behavior
BASIC_TESTS = [
    "keep_final_jump.c",
    "empty.c",
    "remove_jump_keep_label.c",
    "infinite_loop.c",
]


def make_unreachable_code_test(
    program: Path,
) -> Callable[[TestUnreachableCodeElim], None]:
    if program.name in BASIC_TESTS:
        return basic.make_test_run(program)

    if program.name in NO_FUNCALLS_TESTS:

        def test(self: TestUnreachableCodeElim) -> None:
            self.no_function_calls_test(program)

        return test

    else:

        def test(self: TestUnreachableCodeElim) -> None:
            self.no_control_flow_test(program)

        return test
