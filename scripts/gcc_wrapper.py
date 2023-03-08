#!/usr/bin/env python3
"""A wrapper around GCC that lets us test it with the test suite"""

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str, help="Input file")
    # recognize options that tell us to stop at an intermediate stage,
    # but don't need to distinguish between these
    parser.add_argument(
        "--lex",
        "--parse",
        "--validate",
        "--tacky",
        "--codegen",
        action="store_true",
        dest="intermediate",
    )
    parser.add_argument("-l")
    parser.add_argument("-c", action="store_true")
    parser.add_argument("-S", "-s", action="store_true")

    # accept optimization options but ignore them
    parser.add_argument(
        "--fold-constants",
        "--propagate-copies",
        "--eliminate-unreachable-code",
        "--eliminate-dead-stores",
        "--optimize",
        action="store_true",
    )

    # to actually enable optimizations, pass through -O option (./test_compiler <whatever> -- -O)
    parser.add_argument("-O", action="store_true")
    args = parser.parse_args()

    # construct arguments to GCC
    infile: str = args.src
    # treat warnings as errors so we catch all invalid test cases
    gcc_args = [
        "gcc",
        infile,
        "-pedantic",
        "-Werror",
        "-Wno-literal-conversion",
        "-Wno-constant-conversion",
        "-Wno-constant-logical-operand",
        "-Wno-division-by-zero",
        "-Wno-incompatible-library-redeclaration",
        "-Wno-pointer-to-int-cast",
        "-Wno-int-to-pointer-cast",
        "-Wno-literal-range",
        "-Wno-dangling-else",
        "-Wno-newline-eof",
        "-Wno-unused-value",
        "-fcf-protection=none",
    ]

    if args.l:
        gcc_args.extend(["-l", args.l])
    if args.O:
        gcc_args.append("-O")
    if args.intermediate or args.S:
        gcc_args.append("-S")
    elif args.c:
        gcc_args.append("-c")
    else:
        # use expected naming convention for output
        outfile = str(Path(infile).with_suffix(""))
        gcc_args.extend(["-o", outfile])

    cwd = Path(infile).parent
    compile_result = subprocess.run(gcc_args, check=False, cwd=cwd, text=True)

    # if it failed, exit with non-zero code
    if compile_result.returncode != 0:
        sys.exit(compile_result.returncode)

    # it succeeded - if we were only supposed to run up to an intermediate stage, delete assembly
    if args.intermediate:
        asm = Path(infile).with_suffix(".s")
        asm.unlink()
    return


if __name__ == "__main__":
    main()
