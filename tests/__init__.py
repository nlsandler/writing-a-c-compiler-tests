from __future__ import annotations

from . import TestBase, Chapter21
from typing import Type
from pathlib import Path
from unittest import TestCase

def build_test_class(chapter: int, compiler: Path, options: list[str], stage: str, extra_credit: TestBase.ExtraCredit, skip_invalid: bool) -> Type[TestCase]:
    test_dir = Path(__file__).parent.parent.joinpath(
        f"chapter{chapter}").resolve()

    testclass_name = f"TestChapter{chapter}"

    testclass_attrs = {"test_dir": test_dir,
                       "cc": compiler,
                       "options": options,
                       "exit_stage": None if stage == "run" else stage}

    if not skip_invalid:
        invalid_tests = TestBase.make_invalid_tests(test_dir, stage, extra_credit)

        for (test_name, test_cls) in invalid_tests:
            testclass_attrs[test_name] = test_cls
    
    valid_tests = TestBase.make_valid_tests(test_dir, stage, extra_credit)
    for (test_name, test_cls) in valid_tests:
        testclass_attrs[test_name] = test_cls
    
    return type(testclass_name, (TestBase.TestChapter,), testclass_attrs)

def build_chapter_21_test_class(compiler: Path, options: list[str], extra_credit: TestBase.ExtraCredit, int_only: bool, no_coalescing: bool) -> Type[TestCase]:
    
    testclass_attrs = {"test_dir": Chapter21.TEST_DIR,
                        "cc": compiler,
                        "options": options,
                        "exit_stage": None}

    tests = Chapter21.build_test_cases(extra_credit, int_only, no_coalescing)
    for (test_name, test_cls) in tests:
        testclass_attrs[test_name] = test_cls

    return type("TestChapter21", (Chapter21.RegAllocTest,), testclass_attrs)