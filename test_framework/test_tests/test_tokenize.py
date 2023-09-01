"""Tests for assembly tokenizer"""

from __future__ import annotations

import io
import unittest
from typing import List

from ..parser import tokenize
from ..parser.tokenize import Token, TokType

newline = Token(TokType.NEWLINE, "\n")


def sym(symbol: str) -> Token:
    """Create a symbol token"""
    return Token(TokType.SYMBOL, symbol)


class TokenizeTestCase(unittest.TestCase):
    """Test the assembly tokenizer"""

    def test_simple(self) -> None:
        """We can tokenize a simple assembly program"""
        asm = io.StringIO(
            r"""
    .globl main
main:
    movl $2, %eax
    ret
"""
        )
        actual_tokens = list(tokenize.tokenize(asm))
        expected_tokens = [
            newline,
            sym(".globl"),
            sym("main"),
            newline,
            sym("main"),
            Token(TokType.COLON, ":"),
            newline,
            sym("movl"),
            Token(TokType.DOLLAR, "$"),
            Token(TokType.INT, "2"),
            Token(TokType.COMMA, ","),
            Token(TokType.PERCENT, "%"),
            sym("eax"),
            newline,
            sym("ret"),
            newline,
        ]
        self.assertListEqual(actual_tokens, expected_tokens)

    def test_oneline(self) -> None:
        """We can tokenize a single line with no trailing newline"""
        asm = io.StringIO(r""".section .rodata; _foo: .quad 100;""")
        actual_tokens = list(tokenize.tokenize(asm))
        expected_tokens = [
            sym(".section"),
            sym(".rodata"),
            Token(TokType.SEMICOLON, ";"),
            sym("_foo"),
            Token(TokType.COLON, ":"),
            sym(".quad"),
            Token(TokType.INT, "100"),
            Token(TokType.SEMICOLON, ";"),
        ]

        self.assertListEqual(actual_tokens, expected_tokens)

    def test_string_literal(self) -> None:
        """We can tokenize string literals"""
        asm = io.StringIO(
            r'''.asciz "Hi, World!\n\tIt's me, a string. Here's an octal escape sequence: \141"'''
        )
        actual_tokens = list(tokenize.tokenize(asm))
        expected_tokens = [
            sym(".asciz"),
            Token(
                TokType.STRING_LITERAL,
                r'''"Hi, World!\n\tIt's me, a string. Here's an octal escape sequence: \141"''',
            ),
        ]

        self.assertListEqual(actual_tokens, expected_tokens)

    def test_invalid(self) -> None:
        """We raise an error when we encounter an invalid token"""
        asm = io.StringIO("=foo")
        with self.assertRaises(tokenize.TokError):
            list(tokenize.tokenize(asm))

        asm = io.StringIO("foo!")
        with self.assertRaises(tokenize.TokError):
            list(tokenize.tokenize(asm))

    def test_tokenize_operands(self) -> None:
        """We can tokenize various assembly operands"""
        asm = io.StringIO(
            r"-4(%rbp) foo+10( %rip ) $0xdeadbeef $ -1248 % xmm14 (%rax, %rdx , 8)"
        )
        actual_tokens = list(tokenize.tokenize(asm))
        expected_tokens = [
            # -4(%rbp)
            Token(TokType.MINUS_SIGN, "-"),
            Token(TokType.INT, "4"),
            Token(TokType.OPEN_PAREN, "("),
            Token(TokType.PERCENT, "%"),
            sym("rbp"),
            Token(TokType.CLOSE_PAREN, ")"),
            # foo+10(%rip)
            sym("foo"),
            Token(TokType.PLUS_SIGN, "+"),
            Token(TokType.INT, "10"),
            Token(TokType.OPEN_PAREN, "("),
            Token(TokType.PERCENT, "%"),
            sym("rip"),
            Token(TokType.CLOSE_PAREN, ")"),
            # $0xdeadbeef
            Token(TokType.DOLLAR, "$"),
            Token(TokType.INT, "0xdeadbeef"),
            # $-1248
            Token(TokType.DOLLAR, "$"),
            Token(TokType.MINUS_SIGN, "-"),
            Token(TokType.INT, "1248"),
            # %xmm14
            Token(TokType.PERCENT, "%"),
            sym("xmm14"),
            # (%rax, %rdx, 8)
            Token(TokType.OPEN_PAREN, "("),
            Token(TokType.PERCENT, "%"),
            sym("rax"),
            Token(TokType.COMMA, ","),
            Token(TokType.PERCENT, "%"),
            sym("rdx"),
            Token(TokType.COMMA, ","),
            Token(TokType.INT, "8"),
            Token(TokType.CLOSE_PAREN, ")"),
        ]
        self.assertListEqual(actual_tokens, expected_tokens)

    def test_tokenize_floats(self) -> None:
        """Make sure we don't choke on floats (although we don't need to lex them correctly)"""
        asm = io.StringIO(r"100. 0x1a.3e35p-10 .346 666.")
        actual_tokens = list(tokenize.tokenize(asm))
        self.assertTrue(actual_tokens)

    def test_tokenize_labels(self) -> None:
        """We can tokenize various labels"""
        asm = io.StringIO(r"foo2 _foo .L.bar .L:bar _main.123 blah@PLT")
        actual_tokens = list(tokenize.tokenize(asm))
        expected_tokens = [
            sym("foo2"),
            sym("_foo"),
            sym(".L.bar"),
            sym(".L"),
            Token(TokType.COLON, ":"),
            sym("bar"),
            sym("_main.123"),
            sym("blah"),
            Token(TokType.AT, "@"),
            sym("PLT"),
        ]
        self.assertListEqual(actual_tokens, expected_tokens)

    def test_ignore_whitespace(self) -> None:
        """We skip whitespace"""
        asm = io.StringIO(" \t ")
        actual_tokens = list(tokenize.tokenize(asm))
        expected_tokens: List[Token] = []
        self.assertListEqual(actual_tokens, expected_tokens)

    def test_ignore_comments(self) -> None:
        """We skip comments"""
        asm = io.StringIO(
            r"""
    .globl main # this is a comment
# here's another comment
main:
    movl $2, %eax
    # movl $1, %eax
    ret
    # comment! 2309!! # #
"""
        )
        actual_tokens = list(tokenize.tokenize(asm))
        expected_tokens = [
            newline,
            sym(".globl"),
            sym("main"),
            newline,
            newline,
            sym("main"),
            Token(TokType.COLON, ":"),
            newline,
            sym("movl"),
            Token(TokType.DOLLAR, "$"),
            Token(TokType.INT, "2"),
            Token(TokType.COMMA, ","),
            Token(TokType.PERCENT, "%"),
            sym("eax"),
            newline,
            newline,
            sym("ret"),
            newline,
            newline,
        ]
        self.assertListEqual(actual_tokens, expected_tokens)
