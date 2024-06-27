#!/usr/bin/env python3
"""A utility script that runs every test program with the system compiler and records its return code and output"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

# NOTE: basic loads EXPECTED_RESULTS from a file so this whole script will fail
# if expected_results.json doesn't already exist
from test_framework import basic, regalloc
from test_framework.basic import ROOT_DIR, TEST_DIR

results: dict[str, dict[str, Any]] = {}


def needs_wrapper(prog: Path) -> bool:
    """Check whether we need to link against wrapper script"""
    return prog.name in regalloc.REGALLOC_TESTS


def cleanup_keys() -> None:
    """Remove entries from expected_results.json where the corresponding file doesn't exist."""

    # Note: need to construct a list of keys and iterate over that,
    # rather than iterating over dict directly, b/c dict size can't change during iteration
    all_keys = list(results.keys())
    for k in all_keys:
        full_path = TEST_DIR / k
        if not full_path.exists():
            del results[k]
    return


def main() -> None:
    """Run all valid test programs and record results as JSON"""

    # --since-commit SHA tells us to only compile tests
    # that have changed since that commit
    # --all tells us to regenerate all expected results
    # by default just do the ones that have changed since last commit

    # TODO option to remove entries from expected_result.json for files
    # that no longer exist
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--since-commit", default=None)
    group.add_argument("--all", action="store_true")

    args = parser.parse_args()

    all_valid_progs = itertools.chain(
        TEST_DIR.glob("chapter_*/valid/**/*.c"),
        TEST_DIR.glob("chapter_19/constant_folding/**/*.c"),
        TEST_DIR.glob("chapter_19/unreachable_code_elimination/**/*.c"),
        TEST_DIR.glob("chapter_19/copy_propagation/**/*.c"),
        TEST_DIR.glob("chapter_19/dead_store_elimination/**/*.c"),
        TEST_DIR.glob("chapter_19/whole_pipeline/**/*.c"),
        TEST_DIR.glob("chapter_20/all_types/**/*.c"),
        TEST_DIR.glob("chapter_20/int_only/**/*.c"),
    )

    if args.all:
        progs: Iterable[Path] = all_valid_progs
    else:
        baseline = args.since_commit or "HEAD"
        list_changed_files = subprocess.run(
            f"git diff {baseline} --name-only -- tests/chapter_*",
            shell=True,
            text=True,
            check=True,
            capture_output=True,
        )
        # also get untracked files
        list_new_files = subprocess.run(
            "git ls-files -o -- tests/chapter_*",
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
                or (needs_wrapper(p) and regalloc.WRAPPER_SCRIPT in changed_files)
                or any(lib in changed_files for lib in basic.get_libs(p))
                or any(
                    h
                    for h in changed_files
                    if Path(h).suffix == ".h" and Path(h).parent == rel_path.parent
                )
            ):
                progs.append(p)

        # load the json file from that commit to use as baseline
        subprocess.run(
            f"git show {baseline}:expected_results.json > expected_results_orig.json",
            shell=True,
            text=True,
            check=True,
        )
        with open("expected_results_orig.json", "r", encoding="utf-8") as f:
            results.update(json.load(f))
        Path("expected_results_orig.json").unlink()
        cleanup_keys()

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

        # prog may have some extra dependencies
        source_files.extend(basic.get_libs(prog))

        if "chapter_20" in prog.parts:
            # we may need to include wrapper script too
            if needs_wrapper(prog):
                source_files.append(regalloc.WRAPPER_SCRIPT)

        opts = (
            []
        )  # to help catch behavior that relies on faulty assumptions about initialization
        if any(basic.needs_mathlib(p) for p in source_files):
            opts.append("-lm")

        # compile and run the program
        try:
            result = basic.gcc_compile_and_run(source_files, opts)

            # record the result
            result_dict: dict[str, Any] = {"return_code": result.returncode}
            if result.stdout:
                result_dict["stdout"] = result.stdout

            key = str(prog.relative_to(TEST_DIR))
            results[key] = result_dict
            if result.returncode:
                print(f"Return code for {key} is {result.returncode}", file=sys.stderr)
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
