#!/usr/bin/env python3
"""A utility script that runs every test program with the system compiler and records its return code and output"""

from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Any, List

# NOTE: basic loads EXPECTED_RESULTS from a file so this whole script will fail
# if expected_results.json doesn't already exist
from tests import basic, regalloc
from tests.basic import ROOT_DIR

results: dict[str, dict[str, Any]] = {}


def lookup_libs(prog: Path) -> List[Path]:
    """Look up extra library we need to link against for regalloc tests"""
    test_info = regalloc.REGALLOC_TESTS.get(prog.name)
    if test_info is None:
        return []
    if test_info.extra_lib is None:
        # this uses the wrapper script b/c test inspects assembly
        # but doesn't use other library
        return [regalloc.WRAPPER_SCRIPT]
    # uses wrapper script and other library
    return [
        regalloc.WRAPPER_SCRIPT,
        ROOT_DIR / "chapter20/libraries" / test_info.extra_lib,
    ]


def main() -> None:
    """Run all valid test programs and record results as JSON"""
    all_valid_progs = itertools.chain(
        ROOT_DIR.glob("chapter*/valid/**/*.c"),
        ROOT_DIR.glob("chapter19/**/*.c"),
        ROOT_DIR.glob("chapter20/all_types/**/*.c"),
        ROOT_DIR.glob("chapter20/int_only/**/*.c"),
    )

    # iterate over all valid programs
    for prog in all_valid_progs:
        source_files = [prog]
        if "libraries" in prog.parts:
            if prog.name.endswith("_client.c"):
                # if this is the client, don't compile here,
                # we'll compile it when we get to the library
                continue

            # compile client and library together
            client = prog.parent.joinpath(prog.name.replace(".c", "_client.c"))
            source_files.append(client)

        if "chapter20" in prog.parts:
            # we may need to include wrapper script and other library files
            extra_libs = lookup_libs(prog)
            source_files.extend(extra_libs)

        # compile and run the program
        try:
            result = basic.gcc_compile_and_run(*source_files)

            # record the result

            result_dict: dict[str, Any] = {"return_code": result.returncode}
            if result.stdout:
                result_dict["stdout"] = result.stdout

            key = str(prog.relative_to(ROOT_DIR))
            results[key] = result_dict
        finally:

            # delete executable
            exe = source_files[0].with_suffix("")
            Path.unlink(exe)

    with open("expected_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f)


if __name__ == "__main__":
    main()
