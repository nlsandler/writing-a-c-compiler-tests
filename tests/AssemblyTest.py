from __future__ import annotations

import sys
from . import TestBase
from . import AssemblyParser
from .AssemblyParser import Register
from pathlib import Path
import subprocess


class OptimizationTest(TestBase.TestChapter):


    CALLEE_SAVED = [ Register.BX, Register.R12, Register.R13, Register.R14, Register.R15 ]
    def get_target_functions(self, asm_file, *, target_fun: str) -> AssemblyParser.AssemblyFunction:
        if sys.platform == "darwin":
            target_fun = "_" + target_fun
        asm = AssemblyParser.parse(asm_file)
        target_asm = next(f for f in asm if f.name == target_fun)
        return target_asm

    def validate_assembly(self, parsed_asm: AssemblyParser.AssemblyFunction, *, program_path: Path):
        raise NotImplementedError("This is supposed to be subclassed")

    def optimization_test(self, program_path: Path, validator=None):
        """Make sure compiled program has correct results, then inspect its assembly code"""

        # now compile to assembly
        # note: don't need to add --fold-constants b/c it's already in cc_opt
        try:
            self.invoke_compiler(program_path, cc_opt="-s").check_returncode()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(e.stderr) from e
        asm = program_path.with_suffix(".s")

        # compile the assembly code with GCC, run it, and make sure it gives expected result
        actual_result = self.gcc_compile_and_run(asm)
        self.validate_runs(program_path, actual_result)

        # make sure we actually performed the optimization
        parsed_asm = self.get_target_functions(asm, target_fun="target")

        # validate_assembly is baseline assembly validation but we can override it for specific programs
        if not validator:
            validator = self.validate_assembly
        validator(parsed_asm, program_path=program_path)


def build_msg(msg, *, bad_instructions=None, full_prog=None, program_path=None):
    msg_lines = [msg]
    if bad_instructions:
        printed_instructions = [str(i) for i in bad_instructions]
        msg_lines.append("Bad instructions:")
        msg_lines.extend(printed_instructions)
    if full_prog:
        msg_lines.extend(["Complete program:", str(full_prog)])
    if program_path:
        msg_lines.append(f"Program: {program_path}")
    return '\n'.join(msg_lines)
