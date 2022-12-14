from . import AssemblyTest, TestBase
from .AssemblyParser import Register, Opcode
from . import AssemblyParser as Asm
from typing import Optional, Union, Iterable, Callable, Tuple
from pathlib import Path
import subprocess
from collections import defaultdict
import platform
import itertools

TEST_DIR = Path(__file__).parent.parent.joinpath("chapter21").resolve()
IS_OSX = platform.system().lower() == 'darwin'

class RegAllocTest(AssemblyTest.OptimizationTest):
    TESTS = None


    @property
    def wrapper_script(self):
        if IS_OSX:
            return self.test_dir.joinpath("wrapper_osx.s")
        else:
            return self.test_dir.joinpath("wrapper_linux.s")

    @property
    def lib_path(self):
        return self.test_dir.joinpath("libraries")

    def tearDown(self) -> None:
        
        # identical to base TestChapter tearDown but don't kill wrapper_script

        # delete any non-C files aproduced during this testrun
        garbage_files = (f for f in self.test_dir.rglob(
            "*") if not f.is_dir() and f.suffix not in ['.c', '.h'] and f.stem not in  ["wrapper_osx", "wrapper_linux"])

        for f in garbage_files:
            f.unlink()

    def regalloc_test(self, program_path: Path, validator, extra_lib: Optional[Path]=None, target_fun: str="target"):
        """Base class for register allocation tests
        1. Compile the file at program_path to assembly
        2. Link against check_calleed_saved_regs.s wrapper code
        3. Run, compare results against same code compiled w/ GCC
        4. Inspect assembly code w/ validator
        """

        extra_lib_path = None
        if extra_lib:
            extra_lib_path = self.lib_path / extra_lib

        progs = [program_path, self.wrapper_script]

        if extra_lib_path:
            progs.append(extra_lib_path)
        # compile w/ GCC, check result
        expected_result = self.gcc_compile_and_run(*progs, prefix_output=True)
        
        # assemble
                # now compile to assembly
        # note: don't need to add --fold-constants b/c it's already in cc_opt
        try:
            self.invoke_compiler(program_path, cc_opt="-s").check_returncode()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(e.stderr) from e
        asm = program_path.with_suffix(".s")

        progs = [ asm, self.wrapper_script]
        if extra_lib_path:
            progs.append(extra_lib_path)
        actual_result = self.gcc_compile_and_run(*progs)
        # make sure behavior is the same
        self.validate_runs(expected_result, actual_result)

        # make sure we actually performed the optimization
        parsed_asm = self.get_target_functions(
            asm, target_fun=target_fun)


        validator(parsed_asm, program_path=program_path)


    @classmethod
    def get_test_for_path(cls, path: Path):
        if cls.TESTS is None:
            test_dict = {
                "trivially_colorable": lambda path: cls.make_no_spills_test(path),
                "use_all_hardregs": lambda path: cls.make_no_spills_test(path),
                "spill_callee_saved": lambda path: cls.make_only_callee_saved_spills_test(path),
                "preserve_across_fun_call": lambda path: cls.make_only_callee_saved_spills_test(path, max_regs_spilled=3),
                "track_arg_registers": lambda path: cls.make_no_spills_test(path, extra_lib=Path("track_arg_registers_lib.c")),
                "force_spill": lambda path: cls.make_spill_test(path, max_spilled_instructions=3, max_spilled_pseudos=1, extra_lib=Path("force_spill_lib.c")),
                "test_spill_metric": lambda path: cls.make_spill_test(path, max_spilled_instructions=3, max_spilled_pseudos=1, extra_lib=Path("test_spill_metric_lib.c")),
                "test_spill_metric_2": lambda path: cls.make_spill_test(path, max_spilled_instructions=3, max_spilled_pseudos=1, extra_lib=Path("test_spill_metric_2_lib.c")),
                "cmp_liveness": lambda path: cls.make_only_callee_saved_spills_test(path),
                "copy_no_interference": lambda path: cls.make_only_callee_saved_spills_test(path),
                "copy_and_separate_interference": lambda path: cls.make_spill_test(path, max_spilled_pseudos=1, max_spilled_instructions=3),
                "many_pseudos_fewer_conflicts": lambda path: cls.make_no_spills_test(path, extra_lib=Path("many_pseudos_fewer_conflicts_lib.c"), target_fun="no_spills"),
                "same_instr_no_interference": lambda path: cls.make_only_callee_saved_spills_test(path),
                "optimistic_coloring": lambda path: cls.make_spill_test(path, max_spilled_pseudos=5, max_spilled_instructions=20, target_fun="five_spills"),
                "loop": lambda path: cls.make_no_spills_test(path),
                "dbl_trivially_colorable": lambda path: cls.make_no_spills_test(path),
                "fourteen_pseudos_interfere": lambda path: cls.make_no_spills_test(path),
                "push_xmm": lambda path: cls.make_no_spills_test(path),
                "track_dbl_arg_registers": lambda path: cls.make_no_spills_test(path, extra_lib=Path('track_dbl_arg_registers_lib.c')),
                "store_pointer_in_register": lambda path: cls.make_no_spills_test(path),
                "test_spilling_dbls": lambda path: cls.make_spill_test(path, max_spilled_instructions=4, max_spilled_pseudos=1, extra_lib=Path("force_spill_dbl_lib.c")),
                "mixed_ints": lambda path: cls.make_spill_test(path, max_spilled_instructions=2, max_spilled_pseudos=1, extra_lib=Path("force_spill_mixed_int_lib.c")),
                "callee_saved_live_at_exit": lambda path: cls.make_no_spills_test(path, extra_lib=Path("callee_saved_live_at_exit_lib.c"), target_fun="cant_coalesce_fully"),
                "funcall_generates_args": lambda path: cls.make_no_spills_test(path, extra_lib=Path("funcall_generates_args_lib.c")),
                "briggs_coalesce": lambda path: cls.make_coalescing_test(path),
                "briggs_coalesce_tmps": lambda path: cls.make_coalescing_test(path, target_fun="briggs"),
                "george_coalesce": lambda path: cls.make_coalescing_test(path, extra_lib=Path("george_lib.c")),
                "coalesce_prevents_spill": lambda path: cls.make_coalescing_test(path, extra_lib=Path("coalesce_prevents_spill_lib.c"), max_moves=10)
            }
            # default test: compile, run and check results without inspecting assembly

            def default(p: Path):
                def test_valid(self: TestBase.TestChapter):
                    self.compile_and_run(p)
                return test_valid

            cls.TESTS = defaultdict(lambda: default, test_dict)

        return cls.TESTS[path.stem](path)

    @staticmethod
    def uses_stack(i: Union[Asm.Instruction, Asm.Label]):
        if isinstance(i, Asm.Label):
            return False

        if i.mnemonic == Opcode.POP and i.operands[0] != Register.BP:
            # popping a value off the stack is a memory access (unelss we're popping RBP to manage the stack frame)
            return True

        def is_stack(operand):
            return isinstance(operand, Asm.Memory) and operand.base == Register.BP
        
        return any(is_stack(op) for op in i.operands)
    
    @staticmethod
    def make_no_spills_test(program_path: Path, extra_lib: Optional[Path]=None, target_fun: str="target"):

        def test(self):

            def validate(parsed_asm, *, program_path: Path):
                bad_instructions = [i for i in parsed_asm.instructions if self.uses_stack(i)]
                self.assertFalse(bad_instructions, msg=AssemblyTest.build_msg("Found instructions that use operands on the stack", bad_instructions=bad_instructions, full_prog=parsed_asm, program_path=program_path))
            self.regalloc_test(program_path=program_path, validator=validate, extra_lib=extra_lib, target_fun=target_fun)
        
        return test
    

    @staticmethod
    def make_coalescing_test(program_path: Path, extra_lib: Optional[Path]=None, target_fun: str="target", max_moves: int=0):

        def is_mov(i : Union[Asm.Instruction, Asm.Label]):
            """Check whetehr this is a move between registers (other than RBP/RSP) """
            if isinstance(i, Asm.Label):
                return False
            if i.mnemonic != Opcode.MOV:
                return False
            src, dst = i.operands[0], i.operands[1]
            if isinstance(src, Asm.Register) and src not in [ Register.BP, Register.SP] and \
                isinstance(dst, Asm.Register) and dst not in [ Register.BP, Register.SP]:
                return True


        def test(self):

            def validate(parsed_asm, *, program_path: Path):
                bad_instructions = [i for i in parsed_asm.instructions if self.uses_stack(i)]
                mov_instructions = [i for i in parsed_asm.instructions if is_mov(i)]
                self.assertFalse(bad_instructions, msg=AssemblyTest.build_msg("Found instructions that use operands on the stack", bad_instructions=bad_instructions, full_prog=parsed_asm, program_path=program_path))
                self.assertLessEqual(len(mov_instructions), max_moves, msg=AssemblyTest.build_msg(f"Expected at most {max_moves} move instructions but found {len(mov_instructions)}", bad_instructions=mov_instructions, full_prog=parsed_asm, program_path=program_path))
            self.regalloc_test(program_path, validator=validate, extra_lib=extra_lib, target_fun=target_fun)
        
        return test


    @classmethod
    def find_spills(cls, parsed_asm: Asm.AssemblyFunction):
        stack_instructions : list[Asm.Instruction] = [i for i in parsed_asm.instructions if cls.uses_stack(i)]

        # for each callee-saved reg, we accept one move from it and one move to it
        # (recognize saving and restoring with push/pop too TODO maybe don't bother w/ this
        # since alternate approach to saving/restoring callee saved tmps won't work with our tests anyway)
        allowed_moves : dict[Asm.Register, dict[str, list]]= {r : { "to": [], "from": []} for r in cls.CALLEE_SAVED}

        spill_instructions = []
        for si in stack_instructions:
            if si.mnemonic == Opcode.MOV:
                src, dst = si.operands[0], si.operands[1]
                if src in cls.CALLEE_SAVED:
                    allowed_moves[src]["from"].append(si)
                elif dst in cls.CALLEE_SAVED:
                    allowed_moves[dst]["to"].append(si)
                else:
                    spill_instructions.append(si)
            elif si.mnemonic == Opcode.POP and si.operands[0] in cls.CALLEE_SAVED:
                # let people use push/pop instead of mov to save/restore callee-saved regs
                # (note that we don't know whether "push" is saving a callee-saved reg or passing an arg, so we don't track it)
                pop_dst = si.operands[0]
                allowed_moves[pop_dst]["to"].append(si)
            else:
                spill_instructions.append(si)

        for v in allowed_moves.values():
            # if there's more than one copy to or from a particular callee-saved reg, that's bad
            spill_instructions.extend(v["to"][1:])
            spill_instructions.extend(v["from"][:-1])
        return stack_instructions, spill_instructions

    @staticmethod
    def make_only_callee_saved_spills_test(program_path: Path, max_regs_spilled=5):
        """Create a test that validates that there are no spills, except for copies to/from callee-saved regs at start and end
        
        Optionally, specify maximum number of callee-saved regs we're allowed to spill (all 5 by default)
        """

        def test(self):

            def validate(parsed_asm, *, program_path: Path):
                stack_instructions, bad = self.find_spills(parsed_asm)

                self.assertFalse(bad, msg=AssemblyTest.build_msg("Found uses of spilled pseudos besides callee-saved tmps", bad_instructions=bad, full_prog=parsed_asm, program_path=program_path))

                # make sure we don't spill more than the allowable number of callee-saved regs
                max_stack_instructions = max_regs_spilled * 2
                self.assertLessEqual(len(stack_instructions), max_stack_instructions,
                    msg=AssemblyTest.build_msg(f"At most {max_stack_instructions/2} callee-saved registers should be spilled, but it looks like {len(stack_instructions)/2} were spilled.",
                    bad_instructions=stack_instructions, full_prog=parsed_asm, program_path=program_path))
            self.regalloc_test(program_path=program_path, validator=validate)

        return test
    
    @staticmethod
    def make_spill_test(program_path: Path,  max_spilled_instructions: int, max_spilled_pseudos: int, extra_lib: Optional[Path]=None, target_fun: str="target"):
        """Test for a program with so many conflicts that it spills (not just callee-saved regs)
           Validate that our only stack instructions are:
           - saving/restoring callee-saved regs
           - up to 2 instructions using one spilled pseudo
        """
    
        def test(self):

            def validate(parsed_asm, *, program_path: Path):

                _, spill_instructions = self.find_spills(parsed_asm)
                self.assertLessEqual(len(spill_instructions), max_spilled_instructions,
                                     msg=AssemblyTest.build_msg(f"Should only need {max_spilled_instructions} instructions involving spilled pseudo but found {len(spill_instructions)}",
                                     bad_instructions=spill_instructions, full_prog=parsed_asm, program_path=program_path))
                
                spilled_operands = set([op for i in spill_instructions for op in i if isinstance(op, Asm.Memory) ])
                self.assertLessEqual(len(spilled_operands), max_spilled_pseudos, msg=AssemblyTest.build_msg(f"At most {max_spilled_pseudos} pseudoregs should have been spilled, looks like {len(spilled_operands)} were",
                                     bad_instructions=spill_instructions, full_prog=parsed_asm, program_path=program_path))
                
            self.regalloc_test(program_path=program_path, validator=validate, target_fun=target_fun, extra_lib=extra_lib)
        
        return test

def build_test_cases(extra_credit: TestBase.ExtraCredit, int_only: bool, no_coalescing: bool) -> list[Tuple[str, Callable]]:
    # figure out whcih directories are under test
    if int_only:
        subdirs = ["int_only"]
    else:
        subdirs = ["int_only", "all_types"]
    if no_coalescing:
        sub_subdirs = ["no_coalescing"]
    else:
        sub_subdirs = ["no_coalescing", "with_coalescing"]
    
    all_programs: Iterable[Path] = iter([])
    for sub in subdirs:
        for subsub in sub_subdirs:
            more_programs = TestBase.get_programs(TEST_DIR/sub, subsub, extra_credit)
            if all_programs is None:
                all_programs = more_programs
            else:
                all_programs = itertools.chain(all_programs, more_programs)
    
    tests : list[tuple[str, Callable]] = []
    for program in all_programs:
        key = program.relative_to(TEST_DIR).with_suffix("")
        name = f"test_{key}"
        test_method = RegAllocTest.get_test_for_path(program)
        tests.append((name, test_method))

    return tests      