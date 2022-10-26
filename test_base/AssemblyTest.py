import sys
from enum import Enum, unique, auto
from test_base import TestBase
from test_base import AssemblyParser
from test_base.AssemblyParser import Opcode
from typing import Union
from pathlib import Path


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


def is_computation(i: Union[AssemblyParser.Instruction, AssemblyParser.Label]):
    """Check whether this is an acceptable instruction to see in a fully constant-folded function"""
    if isinstance(i, AssemblyParser.Label):
        return False

    if i.mnemonic in NOT_COMPUTE_INSTRUCTIONS:
        return False

    if i.mnemonic == Opcode.SUB and i.operands[1] == AssemblyParser.Register.SP:
        return False

    return True


class OptimizationTest(TestBase.TestChapter):

    def check_returns_constant(self, asm_file, *, target_fun: str, other_funs: set[str]):

        if sys.platform == "darwin":
            target_fun = "_" + target_fun
            other_funs = set("_" + n for n in other_funs)
        other_funs.add(target_fun)
        asm = AssemblyParser.parse(
            asm_file, other_funs)
        target_asm = next(f for f in asm if f.name == target_fun)
        compute_instructions = [
            i for i in target_asm.instructions if is_computation(i)]
        printable_compute_instructions = '\n'.join(
            str(i) for i in compute_instructions)
        self.assertFalse(compute_instructions, msg=f"""
Found the following instructions that should have been constant folded:
    {printable_compute_instructions}
in the assembly function:
    {target_asm}
in file {asm_file}
""")

    def constant_fold_test(self, program_path: Path):
        """Make sure compiled program has correct results, then inspect its assembly code"""

        # first compile and run the program with GCC
        expected_result = self.gcc_compile_and_run(
            program_path, prefix_output=True)

        # now compile to assembly
        # note: don't need to add --fold-constants b/c it's already in cc_opt
        self.invoke_compiler(program_path, cc_opt="-s")
        asm = program_path.with_suffix(".s")

        # compile the assembly code with GCC, run it, and make sure it gives expected result
        actual_result = self.gcc_compile_and_run(asm)
        self.validate_runs(expected_result, actual_result)

        # make sure we actually performed constant folding
        self.check_returns_constant(
            asm, target_fun="target", other_funs=set(["main"]))
