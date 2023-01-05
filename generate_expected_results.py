#!/usr/bin/env python3
"""A utility script that runs every test program with the system compiler and records its return code and output"""

import itertools
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

results : dict[str, dict[str, Any]]= {}

ROOT_DIR = Path(__file__).parent

if sys.platform == 'darwin':
    WRAPPER_SCRIPT = ROOT_DIR.joinpath('chapter21/wrapper_osx.s')
else:
    WRAPPER_SCRIPT = ROOT_DIR.joinpath('chapter21/wrapper_linux.s')

LIBRARIES = {
    "track_arg_registers": "track_arg_registers_lib.c",
    "force_spill": "force_spill_lib.c",
    "spills_and_rewrites": "force_spill_lib.c",
    "spills_rewrites_compare":"force_spill_lib.c",
    "rewrite_large_multiply":"force_spill_lib.c",
    "spill_movz_dst": "force_spill_lib.c",
    "test_spill_metric": "test_spill_metric_lib.c",
    "test_spill_metric_2": "test_spill_metric_2_lib.c",
    "many_pseudos_fewer_conflicts": "many_pseudos_fewer_conflicts_lib.c",
    "track_dbl_arg_registers": "track_dbl_arg_registers_lib.c",
    "test_spilling_dbls": "force_spill_dbl_lib.c",
    "mixed_ints": "force_spill_mixed_int_lib.c",
    "callee_saved_live_at_exit": "callee_saved_live_at_exit_lib.c",
    "funcall_generates_args": "funcall_generates_args_lib.c",
    "george_coalesce": "george_lib.c",
    "coalesce_prevents_spill": "coalesce_prevents_spill_lib.c"
}

all_valid_progs = itertools.chain(ROOT_DIR.glob("chapter*/valid/**/*.c"),
                                  ROOT_DIR.glob("chapter*/valid_extra_credit/**/*.c"),
                                  ROOT_DIR.glob("chapter20/**/*.c"),
                                  ROOT_DIR.glob("chapter21/**/*.c"))

# iterate over all valid programs
for prog in all_valid_progs:
    source_files = [str(prog)]
    if "libraries" in prog.parts:
        if prog.name.endswith("_client.c"):

            # if this is the client, don't compile here, we'll compile it when we get to the library
            continue

        if "chapter21" in prog.parts:
            # these are libraries used by chapter 21 tests, not test programs themselves
            continue

        # compile client and library together
        client = prog.parent.joinpath(prog.name.replace(".c", "_client.c"))
        source_files.append(str(client))

    # compile the program
    # TODO this is copied from TestBase

    try:
        subprocess.run(["gcc"] + source_files + ["-Wno-incompatible-library-redeclaration", "-o", prog.stem],
                        check=True, capture_output=True)
    except subprocess.CalledProcessError as e:


        # if it's a chapter 21 test, may need to compile against wrapper script
        if "chapter21" in prog.parts:
            source_files.append(str(WRAPPER_SCRIPT))
            if prog.stem in LIBRARIES:
                lib_path = ROOT_DIR.joinpath("chapter21/libraries", LIBRARIES[prog.stem])
                source_files.append(str(lib_path))
            try:
                subprocess.run(["gcc"] + source_files + ["-Wno-incompatible-library-redeclaration", "-o", prog.stem],
                                check=True, capture_output=True)
            except subprocess.CalledProcessError as inner_e:
                raise RuntimeError(inner_e.stderr) from inner_e
        else:
            raise RuntimeError(e.stderr) from e


    exe = Path.joinpath(ROOT_DIR, prog.stem)
    # run the program
    try:
        result = subprocess.run([exe], check=False, text=True, capture_output=True)
        if result.stderr:
            raise RuntimeError(result.stderr)
        
        result_dict: dict[str, Any] = {"return_code": result.returncode}
        if result.stdout:
            result_dict["stdout"] = result.stdout
        

        key = str(prog.relative_to(ROOT_DIR))
        results[key] = result_dict
    finally:
        # delete executable
        Path.unlink(exe)


with open("expected_results.json", "w") as f:
    json.dump(results, f)