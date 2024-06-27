#!/usr/bin/env python3

"""Autogenerate several very similar test cases where we create specific interference graphs"""
from pathlib import Path
from string import ascii_lowercase
from typing import Any

from jinja2 import Environment, FileSystemLoader, pass_environment
from jinja2.filters import do_wordwrap


@pass_environment
def comment_wrap(e: Environment, value: str, width: int = 73) -> str:
    # default width is short b/c we usually call this in a context w/ indent of 4
    # and there's no good way to directly track current indent
    lines = [l.strip().removeprefix("//") for l in value.splitlines()]
    oneline = "//" + "".join(lines)
    return (
        do_wordwrap(
            e,
            oneline,
            width=width,
            break_long_words=False,
            wrapstring="\n// ",
        )
        + "\n"
    )


PLATFORM_PROPS = {
    "linux": {
        "local_prefix": ".L",
        "id_prefix": "",
        "plt_suffix": "@PLT",
        "rodata_directives": """\t.section .rodata
\t.align 8""",
        "execstack_note": """\t.section	".note.GNU-stack","",@progbits
""",
    },
    "osx": {
        "local_prefix": "L",
        "id_prefix": "_",
        "plt_suffix": "",
        "rodata_directives": """\t.literal8""",
        "execstack_note": "",
    },
}


def gen_assembly(template_file: Path, output_dir: Path) -> None:
    if not template_file.name.endswith(".s.jinja"):
        exit(f"Expected assembly template, found {template_file}")
    templ = env.get_template(str(template_file))
    basename = template_file.name.removesuffix(".s.jinja")
    for platform in ["linux", "osx"]:
        src = templ.render(PLATFORM_PROPS[platform])
        new_name = f"{basename}_{platform}.s"
        output_path = Path("tests") / output_dir / new_name
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(src)


test_cases = {
    "tests/chapter_11/valid/long_expressions/rewrite_large_multiply_regression.c": {
        "comment": {
            "instr": "imul",
            "extra_desc": " and source operands are immediates value larger than INT32_MAX",
            "other_test": "tests/chapter_11/valid/long_expressions/large_constants.c",
            "operation_desc": "a multiply by a large immediate value",
            "operation_name": "multiply",
        },
        "glob": {"type": "long", "init": "5l"},
        "should_spill": {
            "type": "long",
            "expr": "glob * 4294967307l",
            "val": "21474836535l",
        },
        "one_expr": "glob - 4",
        "thirteen_expr": "glob + 8",
    },
    "tests/chapter_12/valid/explicit_casts/rewrite_movz_regression.c": {
        "comment": {
            "instr": "MovZeroExtend",
            "operation_desc": "a zero extension",
            "operation_name": "zero extend",
        },
        "glob": {"type": "unsigned", "init": "5000u"},
        "should_spill": {"type": "long", "expr": "(long)glob", "val": "5000l"},
        "one_expr": "glob - 4999",
        "thirteen_expr": "glob - 4987u",
    },
    "tests/chapter_16/valid/chars/rewrite_movz_regression.c": {
        "comment": {
            "instr": "movz",
            "operation_desc": "a zero extension",
            "operation_name": "zero extend",
        },
        "glob": {"type": "unsigned char", "init": "5"},
        "should_spill": {"type": "int", "expr": "(int)glob", "val": "5"},
        "one_expr": "glob - 4",
        "thirteen_expr": "8 + glob",
    },
    "tests/chapter_13/valid/explicit_casts/rewrite_cvttsd2si_regression.c": {
        "comment": {
            "instr": "cvttsd2si",
            "operation_desc": "a cvttsd2si",
            "operation_name": "cvttsd2sdi",
        },
        "glob": {"type": "double", "init": "5000."},
        "should_spill": {"type": "long", "expr": "(long)glob", "val": "5000"},
        "one_expr": "glob - 4999",
        "thirteen_expr": "glob - 4987",
    },
}

# TODO better way to track which template corresponds to which final source file
# for now we'll just map assembly templates to output directories
assembly_locations = {
    "stack_alignment_check.s.jinja": "chapter_9/valid/stack_arguments"
}

env = Environment(
    loader=FileSystemLoader("templates"), trim_blocks=True, lstrip_blocks=True
)
env.globals["letters"] = list(ascii_lowercase[0:12])
env.filters["comment_wrap"] = comment_wrap

# pre-chapter 20 tests
for k, v in test_cases.items():
    templ = env.get_template("pre_ch20_spill_var.c.jinja")
    src = templ.render(v)
    with open(k, "w", encoding="utf-8") as f:
        f.write(src)

for template_file, dest_dir in assembly_locations.items():
    gen_assembly(Path(template_file), Path(dest_dir))

# chapter 20 tests

# for templates we use to generate multiple test cases,
# specify each test's destination and variables
configurable_templates: dict[str, dict[str, dict[str, Any]]] = {
    "division_interference.c.jinja": {
        "int_only/no_coalescing/idiv_interference.c": {"instr": "idiv", "u": ""},
        "all_types/no_coalescing/div_interference.c": {
            "instr": "div",
            "u": "unsigned ",
        },
    },
    "force_spill.c.jinja": {
        "int_only/no_coalescing/force_spill.c": {"all_types": False},
        "all_types/no_coalescing/force_spill_mixed_ints.c": {"all_types": True},
    },
}


template_files = Path("templates/chapter_20_templates").iterdir()
for t in template_files:
    if t.suffix != ".jinja":
        exit(f"Found non-template {f} in templates directory")
    relative_path = t.relative_to("templates")
    templ = env.get_template(str(relative_path))
    if t.name in configurable_templates:
        for dest, templ_vars in configurable_templates[t.name].items():
            src = templ.render(templ_vars)
            output_path = Path("tests/chapter_20") / dest
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(src)
    elif str(t).endswith(".s.jinja"):
        gen_assembly(relative_path, Path("chapter_20/libraries"))

    else:
        src = templ.render()
        output_path = Path("tests/chapter_20/int_only/no_coalescing") / t.stem
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(src)
