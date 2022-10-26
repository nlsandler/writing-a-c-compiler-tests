import itertools
import re
import collections
from enum import Enum, auto
from typing import NamedTuple, Callable, Iterable, Iterator, NewType, Union, Optional


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
        if (not self.idx) and self.scale == 1:
            return f"{disp_str}({self.base or ''})"
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
    name: Label
    instructions: list[AsmItem]

    def __str__(self) -> str:
        return f"{self.name}\n" + "\n".join(map(str, self.instructions))


"""Tokens"""


class Punctuation(Enum):
    COMMA = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    PLUS_SIGN = auto()
    MINUS_SIGN = auto()
    COLON = auto()
    PERCENT = auto()
    DOLLAR = auto()


Token = Union[str, int, Punctuation]


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


"""
problem: distinguishing between constants and other symbols
can't just rely on starting digit b/c both can start w/ .
recognzing ints, floating-point values, and hex values would be a pain
.1000 is a constant but .100f is not

possible solutions:
1. use re to get a "word" (all allowable characters in symbol), try to parse as float, treat as constant if it fails
2. only treat integers as constants. if it starts with a digit, parse as an int. this is fine for instructions even if it wouldn't work for compiler directives
    this also means we'll accept floats as labels but that's impossible in a valid program so it's fine


"""

# a symbol is a sequence of alphanumeric characters, $, _, and .
# starting with a non-$ token
# this also matches ints, so lex with INT_PATTERN first!
# note that this may include some floats (e.g. .100), which is fine b/c we don't need to parse them
SYMBOL_PATTERN = re.compile(r"[\w._][\w.$]*")


INT_PATTERN = re.compile(r"(0b|0x)?[0-9a-f]+", flags=re.IGNORECASE)


def tokenize(line: str) -> collections.deque[Token]:
    toks: collections.deque[Token] = collections.deque()
    remaining = line.lstrip()
    while remaining:
        # comments
        if remaining[0] == '#':
            return toks

        # HACK: don't bother parsing string literals
        if remaining[0] == '"':
            return toks

        # integer constants
        # this may consume the first part of a float;
        # this is fine b/c floats only appear in compiler directives, which we ignore
        const_match = re.match(INT_PATTERN, remaining)
        if const_match:
            const_tok = const_match.group(0)
            try:
                toks.append(int(const_tok, base=0))
                remaining = remaining[const_match.end(0):].lstrip()
                continue

            except ValueError:
                # may be an identifier
                pass

        # identifiers
        symbol_match = re.match(SYMBOL_PATTERN, remaining)
        if symbol_match:
            toks.append(symbol_match.group(0))
            remaining = remaining[symbol_match.end(0):].lstrip()
            continue

        # punctuation
        next_char, remaining = remaining[0], remaining[1:].lstrip()
        if next_char == ',':
            toks.append(Punctuation.COMMA)
        elif next_char == '(':
            toks.append(Punctuation.OPEN_PAREN)
        elif next_char == ')':
            toks.append(Punctuation.CLOSE_PAREN)
        elif next_char == '+':
            toks.append(Punctuation.PLUS_SIGN)
        elif next_char == '-':
            toks.append(Punctuation.MINUS_SIGN)
        elif next_char == '%':
            toks.append(Punctuation.PERCENT)
        elif next_char == ':':
            toks.append(Punctuation.COLON)
        elif next_char == '$':
            toks.append(Punctuation.DOLLAR)
        else:
            raise ParseError(f"Unknown token: {next_char}")

    return toks


"""Parsing"""


def sym_to_instr(t: Token) -> Opcode:
    """Parse an instruction mnemonic"""
    if not (isinstance(t, str) and t.isalnum()):
        raise ParseError(f"Bad mnemonic: {t}")

    # deal w/ special cases
    if t == "cqo" or t.startswith("clt"):
        return Opcode.CDQ

    if t.startswith("set"):
        return Opcode.SETCC

    # movs/movz are also prefixes of mov
    if t.startswith("movs"):
        return Opcode.MOVS

    if t.startswith("movz"):
        return Opcode.MOVZ

    if t.startswith("comi"):
        return Opcode.CMP

    if t.startswith("mul"):
        return Opcode.IMUL

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
        raise ParseError(
            f"Expected {expected} but found {next_tok}. Remaining tokens: {toks}")


def parse_expr(toks: collections.deque[Token]) -> Expr:
    expr: Expr = []
    while True:
        next_tok = toks.popleft()
        if isinstance(next_tok, str) or isinstance(next_tok, int):
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


def parse_register(toks: collections.deque[Token]) -> Register:
    expect_next(toks=toks, expected=Punctuation.PERCENT)
    reg_name = toks.popleft()
    if not isinstance(reg_name, str):
        raise ParseError(
            f"Expected register name after %, found {reg_name}")
    return lookup_reg(reg_name)


def parse_immediate(toks: collections.deque[Token]) -> Immediate:
    expect_next(toks=toks, expected=Punctuation.DOLLAR)
    # next token may be punctuation or operator
    next_tok = toks.popleft()
    if isinstance(next_tok, int):
        return Immediate(next_tok)
    elif next_tok in [Punctuation.PLUS_SIGN, Punctuation.MINUS_SIGN]:
        # following tok is punctuation
        imm_val = toks.popleft()
        if not isinstance(imm_val, int):
            raise ParseError(f"bad immediate value: ${next_tok}{imm_val}")
        if next_tok == Punctuation.MINUS_SIGN:
            return Immediate(-imm_val)
        return Immediate(imm_val)
    else:
        raise ParseError(f"Bad immediate value: ${next_tok}")


def parse_next_operand(toks: collections.deque[Token]) -> Operand:
    """Convert a list of tokens following an instruction mnemonic into a list of operands
    accept two forms of memory operands: disp(base) and disp(opt_base,index,opt_scale)
    we don't accept special one-comma form e.g. foo(,1)
    """

    if toks[0] == Punctuation.PERCENT:
        # it's a register
        return parse_register(toks)

    if toks[0] == Punctuation.DOLLAR:
        # it's an immediate, may have + or - sign
        return parse_immediate(toks)

    if isinstance(toks[0], str) and len(toks) == 1:
        # identifier not followed by anything else
        # is a call or jump target
        return toks.popleft()

    # it's a memory operand
    disp: Expr = []
    base: Optional[Register] = None
    idx: Optional[Register] = None
    scale = 1

    # first get displacement
    if toks[0] != Punctuation.OPEN_PAREN:
        # next_tok is part of displacement
        disp = parse_expr(toks)
    expect_next(toks=toks, expected=Punctuation.OPEN_PAREN)

    # optional base
    if toks[0] == Punctuation.PERCENT:
        base = parse_register(toks)

    # base register must be followed by close paren or comma
    next_tok = toks.popleft()
    if next_tok == Punctuation.CLOSE_PAREN:
        # we're done, no index or scale
        return Memory(disp=disp, base=base, idx=None, scale=1)
    # otherwise next token must be comma
    if next_tok != Punctuation.COMMA:
        raise ParseError(
            "Unexpected token after base register in memory operand: " + str(toks))

    #  optional index
    if toks[0] == Punctuation.PERCENT:
        idx = parse_register(toks)

    expect_next(toks=toks, expected=Punctuation.COMMA)

    # scale
    next_tok = toks.popleft()
    if isinstance(next_tok, int):
        expect_next(toks=toks, expected=Punctuation.CLOSE_PAREN)
    elif next_tok != Punctuation.CLOSE_PAREN:
        raise ParseError(
            "expected scale or close paren at end of memory operand")

    return Memory(disp=disp, base=base, idx=idx, scale=scale)


def parse_statement(line: str) -> Union[Label, Instruction, None]:
    """Return a label or instruction, or None if this is a compiler directive"""
    tokens = tokenize(line)
    if not tokens:
        # empty line
        return None

    label_or_mnemonic = tokens.popleft()
    if not isinstance(label_or_mnemonic, str):
        raise ParseError(
            f"Statement must start with an identifier but found {label_or_mnemonic}")

    if tokens and tokens[0] == Punctuation.COLON:
        # it's a label
        if len(tokens) > 1:
            raise ParseError(
                "We don't allow other stuff on the same line as labels")
        return Label(label_or_mnemonic)
    if label_or_mnemonic.startswith("."):
        # it's a compiler directive
        # note that identifiers starting with periods can be labels (or operands referring to labels)
        return None

    # it's an instruction
    mnemonic = sym_to_instr(label_or_mnemonic)
    # convert remaining operands to list of tokens
    operands = []

    while tokens:
        operands.append(parse_next_operand(tokens))
        # expect either comma followed by another operand, or end of list
        if tokens:
            expect_next(toks=tokens, expected=Punctuation.COMMA)
            if not tokens:
                raise ParseError("Expected another operand after comma")

    return Instruction(mnemonic, operands)


def parse(filename: str, function_names: set[str]) -> list[AssemblyFunction]:
    asm_functions: list[AssemblyFunction] = []
    with open(filename, encoding='utf-8') as f:
        current_function: Optional[AssemblyFunction] = None

        # assume one statement per line; assume labels are on their own line
        for line in f:
            label_or_instruction = parse_statement(line)
            if not label_or_instruction:
                # it was a compiler directive
                continue

            if isinstance(label_or_instruction, Label) and label_or_instruction.startswith("_"):
                # for now use _ as marker that something is a function,
                # eventually check set of function names

                #   tokens[0] in function_names:
                # we've found start of a new function
                if current_function:
                    asm_functions.append(current_function)
                current_function = AssemblyFunction(
                    name=label_or_instruction, instructions=[])

            elif current_function is None:
                if isinstance(label_or_instruction, Instruction):
                    raise ParseError(
                        f"instruction found outside of function: {label_or_instruction}")
                # if it's a label, fine to be outside a function
            else:
                # add instruction to current function
                current_function.instructions.append(label_or_instruction)

        # we're done, append last function
        if current_function:
            asm_functions.append(current_function)

    return asm_functions


if __name__ == "__main__":
    asm = parse("asm/static_vars_at_exit.s", set())
    for assembly_fun in asm:
        print(assembly_fun)
