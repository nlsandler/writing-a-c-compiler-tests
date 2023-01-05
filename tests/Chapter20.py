from __future__ import annotations

from . import TestBase
from . import AssemblyParser as Asm
from .AssemblyParser import Opcode, Register
from . import AssemblyTest
from pathlib import Path
from typing import Callable, Iterable, Union, Optional

from enum import Enum, unique, auto
import itertools
from collections import defaultdict
import unittest
import sys

TEST_DIR = Path(__file__).parent.parent.joinpath("chapter20").resolve()

@unique
class Optimizations(Enum):
    """Which TACKY optimizations to test"""
    CONSTANT_FOLD = auto()
    UNREACHABLE_CODE_ELIM = auto()
    COPY_PROP = auto()
    DEAD_STORE_ELIM = auto()
    ALL = auto()

# instructions we'd expect to find even when we've constant folded the whole function
NOT_COMPUTE_INSTRUCTIONS = [Opcode.PUSH,
                            Opcode.POP, Opcode.MOV, Opcode.RET, Opcode.JMP]

def is_computation(i: Union[Asm.Instruction, Asm.Label]):
    """Check whether this is an acceptable instruction to see in a fully constant-folded function"""
    if isinstance(i, Asm.Label):
        return False

    if i.mnemonic in NOT_COMPUTE_INSTRUCTIONS:
        return False

    if i.mnemonic == Opcode.SUB and i.operands[1] == Register.SP:
        return False

    return True

def destination(i: Asm.Instruction):
    # no (explicit) destination operand
    if i.mnemonic in [Opcode.PUSH, Opcode.CDQ, Opcode.JMP, Opcode.JMPCC, Opcode.CMP, Opcode.CALL, Opcode.RET]:
        return None
    # otherwise last operand is desintation
    return i.operands[-1]


def is_mov_to(i: Union[Asm.Label, Asm.Instruction], r: Asm.Register) -> bool:
    return isinstance(i, Asm.Instruction) and i.mnemonic == Opcode.MOV and i.operands[1] == r


def could_overwrite_reg(i: Union[Asm.Label, Asm.Instruction], r: Asm.Register) -> bool:
    # if this appears after an instruction of the form mov something, eax, could it clobber return value
    if isinstance(i, Asm.Label):
        return True  # could jump over mov instruction to reach ret

    # function calls can clobber registers and jmp means we'll never reach ret
    # conditional jump is actually okay if this is still last mov before ret
    # and there are no intervening labels (it's still in ret's only predecessor)
    if i.mnemonic in [Opcode.CALL, Opcode.JMP]:
        return True

    if i.mnemonic in [Opcode.DIV, Opcode.IDIV] and r in [Register.AX, Register.DX]:
        return True

    if i.mnemonic == Opcode.CDQ and r == Register.DX:
        return True

    if destination(i) == r:
        return True

    return False

class ConstantFoldingTest(AssemblyTest.OptimizationTest):

    def validate_assembly(self, parsed_asm, *, program_path: Path):

        compute_instructions = [
            i for i in parsed_asm.instructions if is_computation(i)]
        self.assertFalse(compute_instructions, msg=AssemblyTest.build_msg(
            "Found instructions that should have been constant folded",
            bad_instructions=compute_instructions, full_prog=parsed_asm, program_path=program_path))

class UnreachableCodeTest(AssemblyTest.OptimizationTest):

    def validate_just_one_return(self, parsed_asm, *, program_path: Path):
        ret_instruction_count = sum(1 for i in parsed_asm.instructions if isinstance(
            i, Asm.Instruction) and i.mnemonic == Opcode.RET)
        self.assertLessEqual(ret_instruction_count, 1,
                             msg=f"Expected at most one ret instruction, but found {ret_instruction_count}")

    def validate_assembly(self, parsed_asm, *, program_path: Path):
        # make sure that we've eliminated all jumps, labels, and function calls
        # (in our test cases, all calls to other functions from target are in dead code)
        def bad(i):
            if isinstance(i, Asm.Label):
                return True
            if i.mnemonic in [Opcode.JMP, Opcode.JMPCC, Opcode.CALL]:
                return True
            return False

        bad_instructions = [i for i in parsed_asm.instructions if bad(i)]
        self.assertFalse(bad_instructions, msg=AssemblyTest.build_msg(
            "Found instructions that should have been eliminated",
            bad_instructions=bad_instructions, full_prog=parsed_asm, program_path=program_path))
        self.validate_just_one_return(parsed_asm, program_path=program_path)

    def validate_no_function_calls(self, parsed_asm, *, program_path: Path):
        """Validate that there are no call instructions, but allow other control flow"""
        def bad(i):
            if isinstance(i, Asm.Instruction) and i.mnemonic == Opcode.CALL:
                return True
            return False

        bad_instructions = [i for i in parsed_asm.instructions if bad(i)]
        self.assertFalse(bad_instructions, msg=AssemblyTest.build_msg(
            "Found instructions that should have been eliminated",
            bad_instructions=bad_instructions, full_prog=parsed_asm, program_path=program_path))

    def test_dead_after_branch(self):
        program_path = self.test_dir / "dead_after_if_else.c"
        self.optimization_test(
            program_path, validator=self.validate_no_function_calls)

    def test_dead_after_return(self):
        program_path = self.test_dir / "dead_after_return.c"
        self.optimization_test(program_path)

    def test_constant_if_else(self):
        program_path = self.test_dir / "constant_if_else.c"
        self.optimization_test(program_path)

    def test_for_loop(self):
        program_path = self.test_dir / "dead_for_loop.c"
        self.optimization_test(program_path)

    def test_branch_in_loop(self):
        program_path = self.test_dir / "dead_branch_inside_loop.c"
        self.optimization_test(
            program_path, validator=self.validate_no_function_calls)

    def test_empty_blocks(self):
        program_path = self.test_dir / "empty_block.c"
        self.optimization_test(program_path)

    def test_useless_start_label(self):
        program_path = self.test_dir / "remove_useless_starting_label.c"
        self.optimization_test(program_path)

    def test_loop_in_dead_branch(self):
        program_path = self.test_dir / "loop_in_dead_branch.c"
        self.optimization_test(program_path)

    # test for:
    # - we _do_ remove unreachable blocks
    #   x constant_if_else and dead_after_if_else give basic coverage
    #    x including blocks w/out predecessors and blocks whose predecessors are unreachable
    #    - how to test? make sure some function call is gone
    # x we _do not_ remove blocks that have both reachable and unreachable predecessors
    #    - covered by constant_if_else.c
    # x we can handle loops
    #    x include test where loop itself isn't eliminated but branch w/in loop is
    # x we can handle optimizations that result in empty blocks
    # x we remove useless jumps (conditional and unconditional)
    #     x unconditional: in basic dead branch test, make sure jump is gone
    #           constant_if_else covers this
    #     x conditional: non-constant branch wrapping constant branch? or || / &&  ?
    #         - empty_block covers this
    # x we remove useless labels (including at start of block #1)
    #   remove_useless_starting_label and others
    # x we do not remove jump at end of final block

class CopyPropTest(AssemblyTest.OptimizationTest):

    TESTS = None

    @classmethod
    def get_test_for_path(cls, path: Path):
        if cls.TESTS is None:
            test_dict = {
                "copy_prop_const_fold": lambda path: cls.make_retval_test(6, path),
                "fig_20_8": lambda path: cls.make_retval_test(4, path),
                "init_all_copies": lambda path: cls.make_retval_test(3, path),
                "prop_static_var": lambda path: cls.make_retval_test(10, path),
                "killed_then_redefined": lambda path: cls.make_retval_test(2, path),
                "complex_const_fold": lambda path: cls.make_retval_test(-1, path),
                "remainder_test": lambda path: cls.make_retval_test(1, path),
                "multi_path": lambda path: cls.make_retval_test(3, path),
                "loop": lambda path: cls.make_retval_test(10, path),
                "multi_path_no_kill": lambda path: cls.make_retval_test(3, path),
                "propagate_fun_args": lambda path: cls.make_arg_test("callee", [None, 20], path),
                "kill_and_add_copies": lambda path: cls.make_arg_test("callee", [10, None], path),
                "propagate_var": lambda path: cls.make_same_arg_test("callee", path),
                "multi_instance_same_copy": lambda path: cls.make_same_arg_test("callee", path),
                "redundant_copies": lambda path: cls.make_redundant_copies_test(path),
                "redundant_copies_2": lambda path: cls.make_redundant_copies_test(path),
                "alias_analysis": lambda path: cls.make_retval_test(24, path),
                "char_type_conversion": lambda path: cls.make_retval_test(1, path),
                "copy_struct": lambda path: cls.make_same_arg_test("callee", path),
                "store_doesnt_kill": lambda path: cls.make_same_arg_test("callee", path),
                "propagate_null_pointer": lambda path: cls.make_retval_test(0, path),
                "const_fold_sign_extend": lambda path: cls.make_retval_test(-1000, path),
                "const_fold_sign_extend_2": lambda path: cls.make_retval_test(-1000, path),
                "char_round_trip": lambda path: cls.make_retval_test(1, path),
                "char_round_trip_2": lambda path: cls.make_retval_test(-1, path),
                "unsigned_compare": lambda path: cls.make_retval_test(1, path),
                "not_char": lambda path: cls.make_retval_test(1, path),
                "signed_unsigned_conversion": lambda path: cls.make_retval_test(-11, path),
                "unsigned_wraparound": lambda path: cls.make_retval_test(0, path),
                "const_fold_type_conversions": lambda path: cls.make_retval_test(83333, path),
                "pointer_arithmetic": lambda path: cls.make_no_computations_test(path),
                "propagate_doubles": lambda path: cls.make_retval_test(3000, path)
            }
            # default test: compile, run and check results without inspecting assembly

            def default(p: Path):
                def test_valid(self: TestBase.TestChapter):
                    self.compile_and_run(p)
                return test_valid

            cls.TESTS = defaultdict(lambda: default, test_dict)

        return cls.TESTS[path.stem](path)

    @staticmethod
    def find_return_value(parsed_asm: Asm.AssemblyFunction) -> Asm.Operand:
        # TODO this assumes int return value
        reversed_instrs = list(reversed(parsed_asm.instructions))
        # last instruction should be ret
        last_instruction = reversed_instrs[0]

        def is_ret(i):
            return (isinstance(i, Asm.Instruction) and i.mnemonic == Opcode.RET)

        # if asssembly doesn't match our expectations in ways that aren't specifically under test (e.g. there are multiple return value)
        # raise an error
        if not is_ret(last_instruction):
            raise RuntimeError(
                f"Last instruction in function should be ret but found {last_instruction}")

        # no other ret instructions in the program
        if any(is_ret(
                i) for i in reversed_instrs[1:]):
            raise RuntimeError(
                "Last instruction should be only ret instruction")

        # find instruction of the form mov op, eax
        retval_instr: Asm.Instruction
        retval_idx, retval_instr = next((idx, instr) for idx, instr in enumerate(
            reversed_instrs) if is_mov_to(instr, Register.AX))

        # make sure this is definitely the correct instruction
        clobber_instr = next((could_overwrite_reg(i, Register.AX)
                              for i in reversed_instrs[:retval_idx]), None)
        if clobber_instr:
            raise RuntimeError(
                f"Couldn't find return value: might be clobbered by {clobber_instr} ")

        # now return src of mov instruction; this is our return value
        return retval_instr.operands[0]

    @ staticmethod
    def make_retval_test(expected_retval: Union[int, str], program_path: Path) -> Callable:

        expected_op: Asm.Operand
        if isinstance(expected_retval, int):
            expected_op = Asm.Immediate(expected_retval)
        else:
            if sys.platform == "darwin":
                expected_op = "_" + expected_retval
            expected_op = Asm.Memory(
                disp=[expected_retval], base=Register.IP, idx=None, scale=1)

        def test(self):
            def validate_return_value(parsed_asm, *, program_path: Path):
                actual_retval = self.find_return_value(parsed_asm)
                self.assertEqual(expected_op, actual_retval,
                                 msg=f"Expected {expected_op} as return value, found {actual_retval} ({program_path})")
            self.optimization_test(program_path=program_path,
                                   validator=validate_return_value)
        return test

    @ staticmethod
    def find_args(callee: str, arg_count: int, parsed_asm: Asm.AssemblyFunction) -> list[Optional[Asm.Operand]]:
        # TODO handle floating args
        # TODO refactor w/ find_return-value
        reversed_instrs = list(reversed(parsed_asm.instructions))
        if sys.platform == "darwin":
            callee = "_" + callee
        funcall_idx = reversed_instrs.index(Asm.Instruction(Opcode.CALL, [callee]))
        before_funcall = reversed_instrs[funcall_idx + 1:]
        arg_regs = [Register.DI, Register.SI, Register.DX,
                    Register.CX, Register.R8, Register.R9]

        args: list[Optional[Asm.Operand]] = []
        for r in arg_regs[:arg_count]:
            try:
                mov_instr_idx, mov_instr = next((idx, instr) for (
                    idx, instr) in enumerate(before_funcall) if is_mov_to(instr, r))

                # found a possible move instruction
                if any(could_overwrite_reg(instr, r) for instr in before_funcall[:mov_instr_idx]):
                    # None means "we couldn't find move instruction that populates this argument"
                    # only a problem if we expect this specific argument to be a constant
                    args.append(None)
                else:
                    args.append(mov_instr.operands[0])
            except StopIteration:
                # couldn't find a mov to this argument; sometimes expected one we've implemented coalescing
                args.append(None)

        return args

    @staticmethod
    def make_arg_test(callee: str, expected_args: list[Optional[int]], program_path: Path):
        expected_ops: list[Optional[Asm.Operand]] = [
            Asm.Immediate(i) if i else None for i in expected_args]

        def test(self):
            def validate_args(parsed_asm, *, program_path: Path):

                actual_args = self.find_args(
                    callee, len(expected_args), parsed_asm)
                for idx, (actual, expected) in enumerate(itertools.zip_longest(actual_args, expected_ops)):
                    if expected is not None:
                        self.assertEqual(
                            actual, expected, msg=f"Expected argument {idx} to function {callee} to be {expected}, found {actual}")
            self.optimization_test(program_path=program_path,
                                   validator=validate_args)

        return test

    @staticmethod
    def make_same_arg_test(callee: str, program_path: Path):
        """Test that first and second arguments to callee are the same"""

        def test(self):
            def validate_args(parsed_asm, *, program_path: Path):
                actual_args = self.find_args(
                    callee, 2, parsed_asm)
                # they're the same value if:
                # same value moved into EDI and ESI, or
                # EDI is moved into ESI, or
                # ESI is moved into EDI
                same_value = ((actual_args[0] is not None and actual_args[0] == actual_args[1])
                              or actual_args[0] == Register.SI or actual_args[1] == Register.DI)
                self.assertTrue(
                    same_value, msg=f"Bad arguments {actual_args[0]} and {actual_args[1]} to {callee}: both args should have same value")

            self.optimization_test(program_path=program_path,
                                   validator=validate_args)
        return test

    @staticmethod
    def make_redundant_copies_test(program_path: Path):

        def test(self):
            def validator(parsed_asm, *, program_path: Path):
                """ validate no control flow"""
                def bad(i):
                    if isinstance(i, Asm.Label):
                        return True
                    if i.mnemonic in [Opcode.JMP, Opcode.JMPCC]:
                        return True
                    return False

                bad_instructions = [
                    i for i in parsed_asm.instructions if bad(i)]
                self.assertFalse(bad_instructions, msg=AssemblyTest.build_msg(
                    "Found instructions that should have been eliminated",
                    bad_instructions=bad_instructions, full_prog=parsed_asm, program_path=program_path))

            self.optimization_test(program_path, validator)
        return test

    @staticmethod
    def make_no_computations_test(program_path: Path):

        def is_lea(i):
            if isinstance(i, Asm.Instruction) and i.mnemonic == Opcode.LEA:
                mem: Asm.Memory = i.operands[0]
                if mem.idx is None and mem.scale == 1:
                    return True

            return False

        def test(self):
            # TODO refactor w/ ConstantFoldingTest
            def validate_assembly(parsed_asm, *, program_path: Path):

                compute_instructions = [
                    i for i in parsed_asm.instructions if is_computation(i) and not is_lea(i)]
                self.assertFalse(compute_instructions, msg=AssemblyTest.build_msg(
                    "Found instructions that should have been constant folded",
                    bad_instructions=compute_instructions, full_prog=parsed_asm, program_path=program_path))
            self.optimization_test(program_path, validate_assembly)

        return test


class DeadStoreEliminationTest(AssemblyTest.OptimizationTest):

    TESTS = None

    @classmethod
    def get_test_for_path(cls, path: Path):
        if cls.TESTS is None:
            test_dict = {
                "simple": lambda path: cls.make_dse_test(10, path),
                "dead_store_static_var": lambda path: cls.make_dse_test(5, path),
                "elim_second_copy": lambda path: cls.make_dse_test(10, path),
                "fig_20_12": lambda path: cls.make_dse_test(10, path),
                "loop_dead_store": lambda path: cls.make_dse_test(5, path),
                "use_and_kill": lambda path: cls.make_return_const_test(5, path),
                "aliased_dead_at_exit": lambda path: cls.make_dse_test(50, path)
            }
            # default test: compile, run and check results without inspecting assembly

            def default(p: Path):
                def test_valid(self: TestBase.TestChapter):
                    self.compile_and_run(p)
                return test_valid

            cls.TESTS = defaultdict(lambda: default, test_dict)

        return cls.TESTS[path.stem](path)

    @staticmethod
    def make_dse_test(redundant_const: int, program_path: Path):

        def bad(i: Asm.Instruction):
            # we expect to remove an instruction of the form mov $redundant_const, <something>,
            # so make sure $redundant_const never shows up in the program
            return isinstance(i, Asm.Instruction) and i.operands and i.operands[0] == Asm.Immediate(redundant_const)

        def test(self):
            def validate(parsed_asm, *, program_path: Path):
                bad_instructions = [
                    i for i in parsed_asm.instructions if bad(i)]
                self.assertFalse(bad_instructions, msg=AssemblyTest.build_msg(
                    "Found dead store that should have been eliminated", bad_instructions=bad_instructions, full_prog=parsed_asm, program_path=program_path))

            self.optimization_test(
                program_path=program_path, validator=validate)

        return test

    @classmethod
    def make_return_const_test(cls, const: int, program_path: Path):
        """Validate that we don't have any computations or move instructions other than mov $const, %eax"""

        def test(self):

            allowed_moves : dict[Asm.Register, dict[str, bool]]= {r : { "to": True, "from": True} for r in cls.CALLEE_SAVED}

            def bad(i: Asm.Instruction):

                if is_computation(i):
                    return True
                if i.mnemonic == Opcode.MOV:
                    # only permitted mov instructions:
                    # 1. mov specified return value into AX
                    # 2. manage stack frame
                    # 3. save/restore callee-saved regs (in case we've implemented register allocation but not coalescing yet)
                    # NOTE: save/restore moves could have callee-saved regs as source _and_ dest,
                    # so we rely on the fact that we process instructions in order (and will see save instructions first) to figure out which is which
                    src, dst = i.operands[0], i.operands[1]
                    if src == Asm.Immediate(const) and dst == Register.AX:
                        return False
                    if src in [Register.SP, Register.BP]:
                        return False
                    if src in cls.CALLEE_SAVED and isinstance(dst, Register) and allowed_moves[src]["from"]:
                        # this mov instruction is allowed b/c it saves this callee-saved reg
                        # we shouldn't see any other moves rom this register
                        allowed_moves[src]["from"]  = False
                        return False
                    if dst in cls.CALLEE_SAVED and isinstance(src, Register) and allowed_moves[dst]["to"]:
                        allowed_moves[dst]["to"] = False
                        return False
                    return True
                return False

            def validate(parsed_asm, *, program_path: Path):
                bad_instructions = [
                    i for i in parsed_asm.instructions if bad(i)]
                self.assertFalse(bad_instructions, msg=AssemblyTest.build_msg(
                    "Found instruction that should have been optimized out", bad_instructions=bad_instructions, full_prog=parsed_asm, program_path=program_path))

            self.optimization_test(
                program_path=program_path, validator=validate)

        return test


def get_programs(dir_under_test: Path, extra_credit: TestBase.ExtraCredit, int_only: bool) -> Iterable[Path]:
    programs = TestBase.get_programs(dir_under_test, "int_only", extra_credit)
    if not int_only:
        pt_ii_programs = TestBase.get_programs(dir_under_test, "all_types", extra_credit)
        programs = itertools.chain(programs, pt_ii_programs)
    return programs

def make_constant_fold_test(program: Path) -> Callable:

    def test_const_fold(self: ConstantFoldingTest):
        self.optimization_test(program)
    return test_const_fold

def build_constant_folding_class(compiler: Path, cc_options: list[str], extra_credit: TestBase.ExtraCredit, int_only: bool):
    dir_under_test = TEST_DIR / "constant_folding"

    # TODO: testclass_attrs are copy-pasta, refactor them
    testclass_attrs = {"test_dir": dir_under_test,
                       "cc": compiler,
                       "options": cc_options,
                       "exit_stage": None}

    for program in get_programs(dir_under_test, extra_credit, int_only):
        key = program.relative_to(dir_under_test).with_suffix("")
        name = f"test_{key}"
        testclass_attrs[name] = make_constant_fold_test(program)
    
    return type("TestConstantFolding", (ConstantFoldingTest,), testclass_attrs)

def build_unreachable_code_test(compiler: Path, cc_options: list[str]):
    testclass_attrs = {"test_dir": TEST_DIR / "unreachable_code_elimination",
                    "cc": compiler,
                    "options": cc_options,
                    "exit_stage": None }
    return type("TestUnreachableCodeElimination", (UnreachableCodeTest,), testclass_attrs)

def build_copy_prop_class(compiler: Path, cc_options: list[str], extra_credit: TestBase.ExtraCredit, int_only: bool):
    dir_under_test = TEST_DIR / "copy_propagation"
    testclass_attrs = {"test_dir": dir_under_test,
                       "cc": compiler,
                       "options": cc_options,
                       "exit_stage": None}

    for program in get_programs(dir_under_test, extra_credit, int_only):
        key = program.relative_to(dir_under_test).with_suffix("")
        name = f"test_{key}"
        testclass_attrs[name] = CopyPropTest.get_test_for_path(program)
    
    return type("TestCopyPropagation", (CopyPropTest,), testclass_attrs)

def build_dse_class(compiler: Path, cc_options: list[str], extra_credit: TestBase.ExtraCredit, int_only: bool):
    dir_under_test = TEST_DIR / "dead_store_elimination"
    testclass_attrs = {"test_dir": dir_under_test,
                       "cc": compiler,
                       "options": cc_options,
                       "exit_stage": None}

    for program in get_programs(dir_under_test, extra_credit, int_only):
        key = program.relative_to(dir_under_test).with_suffix("")
        name = f"test_{key}"
        testclass_attrs[name] = DeadStoreEliminationTest.get_test_for_path(program)
    
    return type("TestDeadStoreElimination", (DeadStoreEliminationTest,), testclass_attrs)

def build_test_suite(compiler: Path, cc_options: list[str], extra_credit: TestBase.ExtraCredit, optimization_under_test: Optimizations, int_only: bool) -> list[type[unittest.TestCase]]:

    if optimization_under_test is None or optimization_under_test == Optimizations.ALL:
        # testing the whole pipeline; return all four classes
        constant_folding_class = build_constant_folding_class(compiler, cc_options, extra_credit, int_only)
        unreachable_code_elim_class = build_unreachable_code_test(compiler, cc_options) # may want to include extra-credit here later, but don't for now
        copy_prop_class = build_copy_prop_class(compiler, cc_options, extra_credit, int_only)
        dse_class = build_dse_class(compiler, cc_options, extra_credit, int_only)
        return [constant_folding_class, unreachable_code_elim_class, copy_prop_class, dse_class]
    if optimization_under_test == Optimizations.CONSTANT_FOLD:
        return [build_constant_folding_class(compiler, cc_options, extra_credit, int_only)]
    if optimization_under_test == Optimizations.UNREACHABLE_CODE_ELIM:
        return [build_unreachable_code_test(compiler, cc_options)]
    if optimization_under_test == Optimizations.COPY_PROP:
        return [build_copy_prop_class(compiler, cc_options, extra_credit, int_only)]
    if optimization_under_test == Optimizations.DEAD_STORE_ELIM:
        return [build_dse_class(compiler, cc_options, extra_credit, int_only)]
    raise ValueError(f"Unknown optimization {optimization_under_test}")