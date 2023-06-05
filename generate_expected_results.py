#!/usr/bin/env python3
"""A utility script that runs every test program with the system compiler and records its return code and output"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
from pathlib import Path
from typing import Any, Iterable, List

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

    # --since-commit SHA tells us to only compile tests
    # that have changed since that commit
    # --all tells us to regenerate all expected results
    # by default just do the ones that have changed since last commit

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--since_commit", default=None)
    group.add_argument("--all", action="store_true")

    args = parser.parse_args()

    all_valid_progs = itertools.chain(
        ROOT_DIR.glob("chapter*/valid/**/*.c"),
        ROOT_DIR.glob("chapter19/**/*.c"),
        ROOT_DIR.glob("chapter20/all_types/**/*.c"),
        ROOT_DIR.glob("chapter20/int_only/**/*.c"),
    )

    if args.all:
        progs: Iterable[Path] = all_valid_progs
    else:
        baseline = args.since_commit or "HEAD"
        list_changed_files = subprocess.run(
            f"git diff {baseline} --name-only -- chapter*",
            shell=True,
            text=True,
            check=True,
            capture_output=True,
        )
        # also get untracked files
        list_new_files = subprocess.run(
            "git ls-files -o -- chapter*",
            shell=True,
            text=True,
            check=True,
            capture_output=True,
        )
        changed_files = (
            list_changed_files.stdout.split() + list_new_files.stdout.split()
        )
        # include each file from all_valid progs if:
        # - it changed
        # - it's a client and the library changed, or vice versa
        # - it uses a library/wrapper that changed
        # - a .h file in the same directory changed (use this as hacky shorthand for whether header for this particular file changed)
        progs = []
        for p in all_valid_progs:
            rel_path = p.relative_to(ROOT_DIR)
            if (
                str(rel_path) in changed_files
                or str(rel_path).replace(".c", "_client.c") in changed_files
                or str(rel_path).replace("_client.c", ".c") in changed_files
                or any(lib in changed_files for lib in lookup_libs(p))
                or any(
                    h
                    for h in changed_files
                    if Path(h).suffix == ".h" and Path(h).parent == rel_path.parent
                )
            ):
                progs.append(p)

        # load the json file from that commit ot use as baseline
        subprocess.run(
            f"git show {baseline}:expected_results.json > expected_results_orig.json",
            shell=True,
            text=True,
            check=True,
        )
        with open("expected_results_orig.json", "r", encoding="utf-8") as f:
            results.update(json.load(f))
        (ROOT_DIR / "expected_results_orig.json").unlink()

    # iterate over all valid programs
    for prog in progs:
        print(prog)
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
    try:
        main()
    except subprocess.CalledProcessError as err:
        print(err.cmd)
        print(err.stderr)
        print(err.stdout)
