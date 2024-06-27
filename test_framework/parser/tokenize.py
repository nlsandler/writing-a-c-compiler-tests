"""Tokenize an assembly file"""
from __future__ import annotations

import io
import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Generator


class TokError(RuntimeError):
    """Found an invalid token"""

    def __init__(self, bad_tok: str) -> None:
        self.bad_tok = bad_tok
        super().__init__()


class TokType(Enum):
    # literals
    COMMA = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    PLUS_SIGN = auto()
    MINUS_SIGN = auto()
    COLON = auto()
    PERCENT = auto()
    DOLLAR = auto()
    AT = auto()
    STAR = auto()
    # line separators
    SEMICOLON = auto()
    NEWLINE = auto()
    # more complex tokens
    SYMBOL = auto()  # this includes labels, register names, mnemonics, etc
    INT = auto()
    STRING_LITERAL = auto()  # we don't actually track the values of these


@dataclass
class Token:
    tok_type: TokType
    tok_str: str


TOKENS = {
    # we recognize decimal and hexadecimal ints (not octal or binary)
    "INT": r"([0-9]+|0x[0-9a-f]+)\b",
    # a symbol is a letter, digit, '.' or '_' followed by a sequence of alphanumeric, '.','_',
    # and '$' and characters
    # NOTE: we don't permit symbols to start with $ characters;
    # in GAS and llvm-as, you can seemingly define labels starting with $ but not use them since
    # $ in assembly operands triggers something involving absolute addressing
    # NOTE 2: most symbols can't start with digits but some directive arguments (e.g. 8byte_literals) can
    "SYMBOL": r"[\w.][\w.$]*",
    # NOTE: we accept \ followed by any digit as an escape sequence in a string literal
    "STRING_LITERAL": r'''"([^"\\\n]|\\.)*"''',
    # single characters
    "COMMA": r",",
    "OPEN_PAREN": r"\(",
    "CLOSE_PAREN": r"\)",
    "PLUS_SIGN": r"\+",
    "MINUS_SIGN": r"-",
    "COLON": r":",
    "PERCENT": r"%",
    "DOLLAR": r"\$",
    "AT": r"@",
    "STAR": r"\*",
    "SEMICOLON": r";",
    "NEWLINE": r"\n",
    # skip comments and whitespace
    # a comment matches anything from # to the end of the line, not counting the \n character
    "SKIP": r"(#.*)|[ \r\t\f\v]",
    # anything else is an error
    "ERROR": r".",
}

TOKEN_PATTERN = re.compile(
    "|".join(f"(?P<{tok_type}>{pattern})" for tok_type, pattern in TOKENS.items()),
    flags=re.IGNORECASE,
)


def tokenize(input_file: io.TextIOBase) -> Generator[Token, None, None]:
    """Convert file object to token generator
    Also perform preprocessing: remove extra whitespace and comments
    Adapted from https://docs.python.org/3/library/re.html#writing-a-tokenizer

    NOTE #1: does not support for non-ASCII Unicode characters
    NOTE #2: doesn't lex floats correctly (e.g. will parse .100 as a symbol
    and 100.0 as multiple tokens) This is okay because these contents only appear in directives,
    which we don't care about
    """

    # TODO support /* */ comments?

    for line in input_file:
        for recognized_tok in re.finditer(TOKEN_PATTERN, line):
            tok_type = recognized_tok.lastgroup  # group name
            tok_value = recognized_tok.group()
            if tok_type is None:
                raise TokError(
                    "Internal error: didn't match any token regex, including error.\n"
                    f"Bad line: {line}"
                )
            if tok_type == "ERROR":
                raise TokError(tok_value)
            if tok_type == "SKIP":
                # don't yield a token for whitespace or comments
                continue
            yield Token(TokType[tok_type], tok_value)
