"""Dead store elimination tests."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from .. import basic
from . import common


class TestDeadStoreElimination(common.TackyOptimizationTest):
    """Test cases for dead store elimination.


    We'll generate a test method for each C program in the chapter_19/dead_store_elimination/ directory.
    Each dynamically generated test calls one of the following main test methods:

    * compile_and_run, defined in TestChapter: validate behavior but don't inspect assembly
    * store_eliminated_test, defined in TackyOptimizationTest: make sure a particular mov instruction was eliminated
    * return_const_test, defined in TackyOptimizationTest: make sure entire funcion is reduce to a return instruction
    """

    test_dir = common.TEST_DIR / "dead_store_elimination"


# programs to validate with store_eliminated_test, and the constants that should be eliminated
STORE_ELIMINATED = {
    # int-only
    "dead_store_static_var.c": 5,
    "elim_second_copy.c": 100,
    "fig_19_11.c": 10,
    "loop_dead_store.c": 5,
    "static_not_always_live.c": 30,
    "initialize_blocks_with_empty_set.c": 10,
    # other types
    "aliased_dead_at_exit.c": 50,
    "copy_to_dead_struct.c": 10,
    "getaddr_doesnt_gen.c": 4,
    "compound_assign_to_dead_struct_member.c": 4,
    "copy_to_dead_union.c": 123,
}

# programs to validate with return_const_test, with expected return value
RETURN_CONST = {
    "delete_arithmetic_ops.c": 5,
    "simple.c": 3,
    "delete_dead_pt_ii_instructions.c": 5,
    "dead_incr_decr.c": 10,
    "decr_struct_member.c": 15,
    "dead_compound_assignment.c": 10,
}


def make_dse_test(program: Path) -> Callable[[TestDeadStoreElimination], None]:
    """Generate test method for one test program."""

    if "dont_elim" in program.parts:
        return basic.make_test_run(program)

    if program.name in STORE_ELIMINATED:
        redundant_const = STORE_ELIMINATED[program.name]

        def test(self: TestDeadStoreElimination) -> None:
            self.store_eliminated_test(
                source_file=program, redundant_consts=[redundant_const]
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
