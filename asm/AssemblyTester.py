from curses.ascii import SI, SP, isalnum, isdigit
import io
import itertools
from lib2to3.pgen2 import token
from pickle import POP
import re
import collections
from enum import Enum, auto
from sre_constants import CALL
from typing import NamedTuple, Callable, Iterable, Iterator, NewType, Union, TextIO, Optional


class ParseError(RuntimeError):
    pass


"""IR for assembly programs"""


# Operands
class Immediate(int):
    """Immediate operands like $3"""

    def __str__(self) -> str:
        return f"${super().__str__()}"


class Register(Enum):
    AX = auto()
    BX = auto()
    CX = auto()
    DX = auto()
    DI = auto()
    SI = auto()
    R8 = auto()
    R9 = auto()
    R10 = auto()
    R11 = auto()
    R12 = auto()
    R13 = auto()
    R14 = auto()
    R15 = auto()
    BP = auto()
    SP = auto()
    IP = auto()
    XMM0 = auto()
    XMM1 = auto()
    XMM2 = auto()
    XMM3 = auto()
    XMM4 = auto()
    XMM5 = auto()
    XMM6 = auto()
    XMM7 = auto()
    XMM8 = auto()
    XMM9 = auto()
    XMM10 = auto()
    XMM11 = auto()
    XMM12 = auto()
    XMM13 = auto()
    XMM14 = auto()
    XMM15 = auto()

    def __str__(self) -> str:
        return f"%{self.name}"


class Operator(Enum):
    """these can appear in operands like -4(%rbp) or foo+10(%rbp)"""
    PLUS = auto()
    MINUS = auto()

    def __str__(self) -> str:
        if self == Operator.PLUS:
            return "+"
        if self == Operator.MINUS:
            return "-"
        raise NotImplementedError("what operator is this???")


Expr = list[Union[int, str, Operator]]


class Memory(NamedTuple):
    """memory operands (including RIP-relative, stack, indexed)"""
    disp: Expr
    base: Optional[Register]
    idx: Optional[Register]
    scale: int  # non-optional b/c defaults to 1 if not specified

    def __str__(self) -> str:
        disp_str = "".join(map(str, self.disp))
        return f"{disp_str}({self.base or ''}, {self.idx or ''}, {self.scale or ''})"


# target of jump or call instruction
Target = str

Operand = Union[Memory, Register, Immediate, Target]


# Instructions (including labels)

class Opcode(Enum):
    # data movement/memory manipulation
    MOV = auto()
    PUSH = auto()
    POP = auto()
    LEA = auto()
    # conversions
    MOVS = auto()
    MOVZ = auto()
    CVTTSD2SI = auto()
    CVTSI2SD = auto()
    # binary
    ADD = auto()
    SUB = auto()
    IDIV = auto()
    DIV = auto()
    IMUL = auto()
    AND = auto()
    OR = auto()
    XOR = auto()
    # unary
    SHR = auto()
    NOT = auto()
    NEG = auto()
    CDQ = auto()
    # control flow and conditionals
    JMP = auto()
    JMPCC = auto()
    SETCC = auto()
    CMP = auto()
    CALL = auto()
    RET = auto()

    def __str__(self) -> str:
        return self.name.lower()


class Instruction(NamedTuple):
    mnemonic: Opcode
    operands: list[Operand]

    def __str__(self) -> str:
        str_operands = ", ".join(map(lambda x: str(x), self.operands))
        return f"\t{self.mnemonic} {str_operands}"

# labels that are internal to functions, not marking the start of new functions


class Label(str):
    """w/in assembly function, these are only used to represent labels that are internal to functions
    NB we strip colon when tokenizing this"""

    def __str__(self) -> str:
        return super().__str__() + ":"


AsmItem = Union[Label, Instruction]


class AssemblyFunction(NamedTuple):
    name: str
    instructions: list[AsmItem]


"""Tokens"""


class SymToken(str):
    """Symbols that are _not_ labels"""
    pass


class ConstToken(str):
    """Constants that appear in operands like 4(%rbp), distinct from immediates
    just store as string, don't need actual value
    """
    pass


class Punctuation(Enum):
    COMMA = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    PLUS_SIGN = auto()
    MINUS_SIGN = auto()


Token = Union[Label, Immediate, Register, SymToken, ConstToken, Punctuation]

Statement = list[Token]


"""Tokenizing"""


def lookup_reg(regname: str) -> Register:
    alias_map = {
        "rax": Register.AX,
        "eax": Register.AX,
        "al": Register.AX,
        "rbx": Register.BX,
        "ebx": Register.BX,
        "bl": Register.BX,
        "rcx": Register.CX,
        "ecx": Register.CX,
        "cl": Register.CX,
        "rdx": Register.DX,
        "edx": Register.DX,
        "dl": Register.DX,
        "rdi": Register.DI,
        "edi": Register.DI,
        "dil": Register.DI,
        "rsi": Register.SI,
        "esi": Register.SI,
        "sil": Register.SI,
        "r8": Register.R8,
        "r8d": Register.R8,
        "r8b": Register.R8,
        "r9": Register.R9,
        "r9d": Register.R9,
        "r9b": Register.R9,
        "r10": Register.R10,
        "r10d": Register.R10,
        "r10b": Register.R10,
        "r11": Register.R11,
        "r11d": Register.R11,
        "r11b": Register.R11,
        "r12": Register.R12,
        "r12d": Register.R12,
        "r12b": Register.R12,
        "r13": Register.R13,
        "r13d": Register.R13,
        "r13b": Register.R13,
        "r14": Register.R14,
        "r14d": Register.R14,
        "r14b": Register.R14,
        "r15": Register.R15,
        "r15d": Register.R15,
        "r15b": Register.R15,
        "rsp": Register.SP,
        "rbp": Register.BP,
        "rip": Register.IP,
        "xmm0": Register.XMM0,
        "xmm1": Register.XMM1,
        "xmm2": Register.XMM2,
        "xmm3": Register.XMM3,
        "xmm4": Register.XMM4,
        "xmm5": Register.XMM5,
        "xmm6": Register.XMM6,
        "xmm7": Register.XMM7,
        "xmm8": Register.XMM8,
        "xmm9": Register.XMM9,
        "xmm10": Register.XMM10,
        "xmm11": Register.XMM11,
        "xmm12": Register.XMM12,
        "xmm13": Register.XMM13,
        "xmm14": Register.XMM14,
        "xmm15": Register.XMM15,
        # TODO finish this
    }
    return alias_map[regname]


def take_chars_while(predicate: Callable[[str], bool], chars: collections.deque[str]) -> str:
    result = []
    while predicate(chars[0]):
        result.append(chars.popleft())

    return "".join(result)


def tokenize(line: str) -> list[Token]:
    chars = collections.deque(line)
    toks: list[Token] = []
    while chars:
        next_char = chars.popleft()
        # comment
        if next_char == '#':
            chars.clear()
        # punctuation
        elif next_char == ',':
            toks.append(Punctuation.COMMA)
        elif next_char == '(':
            toks.append(Punctuation.OPEN_PAREN)
        elif next_char == ')':
            toks.append(Punctuation.CLOSE_PAREN)
        elif next_char == '+':
            toks.append(Punctuation.PLUS_SIGN)
        elif next_char == '-':
            toks.append(Punctuation.MINUS_SIGN)
        # whitespace
        elif next_char.isspace():
            # ignore whitespace
            continue
        # constants
        elif next_char.isdigit():
            # it's a constant token
            def is_const_char(c): return c.isalnum() or c in ".+-"
            # next_char is part of token, so put it back
            chars.appendleft(next_char)
            num_tok = take_chars_while(is_const_char, chars)

            toks.append(ConstToken(num_tok))
        # registers
        elif next_char == '%':
            # note: we don't permit space b/t prefix and reg name
            # TODO use takewhile-type function here
            reg_name = take_chars_while(str.isalpha, chars)
            toks.append(lookup_reg(reg_name))
        # labels, symbols, immediates
        else:
            # next_char is part of symbol, so put it back
            chars.appendleft(next_char)
            def is_symbol_char(x): return x.isalnum() or x in "_.$"
            sym = take_chars_while(is_symbol_char, chars)
            # if symbol is immediately followed by colon, it's a label
            if chars[0] == ':':
                chars.popleft()  # consume colon
                toks.append(Label(sym))
            elif sym[0] == '$':
                # probably an immediate
                try:
                    toks.append(Immediate(int(sym[1:])))
                except ValueError:
                    toks.append(SymToken(sym))
            else:
                toks.append(SymToken(sym))

    return toks


"""Parsing"""


def is_directive(t: Token):
    """Check whether the first token in a line is a directive (i.e. a symbol that starts with '.')
    """
    if isinstance(t, SymToken) and t[0] == '.':
        return True
    return False


def is_compiler_directive(statement):
    tok = statement[0]
    return isinstance(tok, SymToken) and tok[0] == '.'


def sym_to_instr(t: Token) -> Opcode:
    """Parse an instruction mnemonic"""
    if not (isinstance(t, SymToken) and t.isalpha()):
        raise ParseError

    # deal w/ special cases for
    if t == "cqo":
        return Opcode.CDQ
    CONDITION_CODES = ["e", "ne", "g", "ge",
                       "l", "le", "b", "be", "a", "ae", "po"]
    if t[0] == "j" and t[1:] in CONDITION_CODES:
        return Opcode.JMPCC

    for opcode in Opcode:
        if t.startswith(str(opcode)):
            return opcode

    raise ParseError(f"Unknown opcode {t}")


def expect_next(*, toks: collections.deque[Token], expected: Token):
    next_tok = toks.popleft()
    if next_tok != expected:
        raise ParseError(f"Expected {expected} but found {next_tok}")

# Operand = Union[Data, Indexed, Memory, Register, Immediate]


def parse_expr(toks: collections.deque[Token]) -> Expr:
    expr: Expr = []
    while True:
        next_tok = toks.popleft()
        if isinstance(next_tok, SymToken) or isinstance(next_tok, ConstToken):
            expr.append(next_tok)
        elif next_tok == Punctuation.PLUS_SIGN:
            expr.append(Operator.PLUS)
        elif next_tok == Punctuation.MINUS_SIGN:
            expr.append(Operator.MINUS)
        else:
            # we didn't consume this so put it back on the queue
            toks.appendleft(next_tok)
            break  # we're done
    return expr


def parse_next_operand(toks: collections.deque[Token]) -> Operand:
    """Convert a list of tokens following an instruction mnemonic into a list of operands
    accept two forms of memory operands: disp(base) and disp(opt_base,index,opt_scale)
    we don't accept special one-comma form e.g. foo(,1)
    """

    next_tok = toks.popleft()
    if isinstance(next_tok, Label):
        # labels (w/ colons) shouldn't appear here
        raise ParseError(
            "Found label while trying to parse operands: " + str(next_tok))
    if isinstance(next_tok, Register) or isinstance(next_tok, Immediate):
        # it's valid as-is
        return next_tok

    if isinstance(next_tok, SymToken) and not toks:
        return next_tok

    # it's a memory operand
    disp: Expr = []
    base: Optional[Register] = None
    idx: Optional[Register] = None
    scale = 1

    # first get displacement
    if next_tok != Punctuation.OPEN_PAREN:
        # next_tok is part of displacement, put it back on deque
        toks.appendleft(next_tok)
        disp = parse_expr(toks)
        expect_next(toks=toks, expected=Punctuation.OPEN_PAREN)

    # now base
    base_tok = toks.popleft()
    if base_tok != Punctuation.COMMA:

        if isinstance(base_tok, Register):
            base = base_tok
        else:
            raise ParseError(
                "base of memory operand must be register: " + str(toks))

        # base register must be followed by close paren or comma
        next_tok = toks.popleft()
        if next_tok == Punctuation.CLOSE_PAREN:
            # we're done, no index or scale
            return Memory(disp=disp, base=base, idx=None, scale=1)
        # otherwise next token must be comma
        if next_tok != Punctuation.COMMA:
            raise ParseError(
                "Unexpected token after base register in memory operand: " + str(toks))

    # index
    index_tok = toks.popleft()
    if isinstance(index_tok, Register):
        idx = index_tok
    else:
        raise ParseError("Index in memory operand isn't a register")

    expect_next(toks=toks, expected=Punctuation.COMMA)

    # scale
    next_tok = toks.popleft()
    if isinstance(next_tok, ConstToken):
        scale = int(next_tok)
        expect_next(toks=toks, expected=Punctuation.CLOSE_PAREN)
    elif next_tok != Punctuation.CLOSE_PAREN:
        raise ParseError(
            "expected scale or close paren at end of memory operand")

    return Memory(disp=disp, base=base, idx=idx, scale=scale)


def stmt_to_instruction(stmt: Statement) -> AsmItem:
    # convert label token to label
    if len(stmt) == 1 and isinstance(stmt[0], Label):
        return stmt[0]

    # convert anything else to instruction
    opcode_tok, operand_toks = stmt[0], stmt[1:]
    mnemonic = sym_to_instr(opcode_tok)

    # convert remaining operands to list of tokens
    operands = []
    if operand_toks:
        op_deque = collections.deque(operand_toks)
        while True:
            operands.append(parse_next_operand(op_deque))
            if not op_deque:
                # we're done
                break

            # expect comma, then repeat
            expect_next(toks=op_deque, expected=Punctuation.COMMA)

    return Instruction(mnemonic, operands)


def parse(filename: str, function_names: set[str]) -> list[AssemblyFunction]:
    asm_functions: list[AssemblyFunction] = []

    with open(filename, encoding='utf-8') as f:
        current_function: Optional[AssemblyFunction] = None

        for line in f:
            tokens = tokenize(line)

            if not tokens or is_compiler_directive(tokens):
                # ignore empty lines and compiler directives
                continue
            if isinstance(tokens[0], Label) and tokens[0] in function_names:
                # we've found start of a new function
                if current_function:
                    asm_functions.append(current_function)
                current_function = AssemblyFunction(
                    name=tokens[0], instructions=[])
                if tokens[1:]:
                    raise NotImplementedError(
                        "Label and other stuff on same line")
            elif current_function is None:
                raise ParseError(
                    f"instruction found outside of function: {tokens}")
            else:
                # add instruction to current function
                current_function.instructions.append(
                    stmt_to_instruction(tokens))

    return asm_functions
