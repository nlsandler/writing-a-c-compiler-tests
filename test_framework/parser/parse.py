# could we abuse python.tokenize here?
"""Parser for assembly programs.

Limitations:
1. This is only used to parse programs that we've already assembled and linked successfully,
so it's not intended to handle invalid programs gracefully.

2. This is only guaranteed to handle the subset of assembly we use in the book.
  I've included some support for other common assembly instructions but you shouldn't rely on it.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Generator, List, Optional, Union

from . import asm, tokenize
from .asm import Expr, Immediate, Opcode, Operand, Operator, Register
from .tokenize import Token, TokType


class ParseError(RuntimeError):
    """We encountered nvalid assembly (or, more likely, valid assembly that don't support)"""


# regex to identify function names (and global variables, though we don't care about those)
# as opposed to internal labels
C_IDENT_PATTERN = r"[_A-Za-z][_A-Za-z0-9]*"
C_IDENTIFIER = re.compile(C_IDENT_PATTERN)
# On macOS, identifiers from the original program must start with underscores
MANGLED_C_IDENTIFIER = re.compile(r"_" + C_IDENT_PATTERN)


def is_valid_c_identifier(lbl: str) -> bool:
    """Could this symbol name be a function or variable name from the original source program?"""
    regex = C_IDENTIFIER
    if sys.platform == "darwin":
        regex = MANGLED_C_IDENTIFIER

    return re.fullmatch(regex, lbl) is not None


def expect_next(*, toks: List[Token], expected: TokType) -> None:
    """Consume next token and fail if it isn't what we expect"""
    next_tok = toks.pop(0)
    if next_tok.tok_type != expected:
        raise ParseError(
            f"Expected {expected} but found {next_tok}. Remaining tokens: {toks}"
        )


def parse_opcode(tok: str) -> tuple[Opcode, Optional[int]]:
    """Parse an instruction mnemonic; return opcode and inferred size
    Inferred size is used to normalize immediate values later on;
    it's None if we can't infer the size or if this is a floating-point instruction
    """
    if not tok.isalnum():
        raise ParseError(f"Bad mnemonic: {tok}")

    # deal w/ special cases
    # Sign-extension from RAX to RDX is cqo in Intel syntax, cdq in AT&T syntax
    # but assemblers accept Intel mnemonics even when using AT&T syntax
    # (and we use the intenl mnemonics in the book)
    if tok in ["cqo", "cqto"]:
        return Opcode.CDQ, 8

    # Sign-extend EAX to EDX: cdq is Intel menmonic, cltd is AT&T mnemonic
    if tok in ["cdq", "cltd"]:
        return Opcode.CDQ, 4

    # sign-extend EAX to RAX: clt/cltq is AT&T syntax, cdqe is Intel syntax
    if tok in ["clt", "cltq", "cdqe"]:
        return Opcode.CDQE, 4

    # overlapping prefixes
    if tok.startswith("movsd"):
        return Opcode.MOV, None

    if tok.startswith("movs"):
        size = None
        if tok[-2] == "b":
            size = 1
        elif tok[-2] == "l":
            size = 4
        return Opcode.MOVS, size

    if tok.startswith("movz"):
        size = None
        if tok[-2] == "b":
            size = 1
        elif tok[-2] == "l":
            size = 4
        return Opcode.MOVZ, size

    # comisd and ucomisd are floating-point cmp
    if tok.startswith("comi") or tok.startswith("ucomi"):
        return Opcode.CMP, None

    if tok.startswith("pxor"):
        return Opcode.XOR, None

    # for our purposes, okay to treat mul and imul as equivalent
    if tok.startswith("mul"):
        return Opcode.IMUL, None

    # conditional instructions; don't distinguish between different conditions
    if tok.startswith("set"):
        return Opcode.SETCC, 1

    condition_codes = [
        "e",
        "g",
        "ge",
        "l",
        "le",
        "b",
        "be",
        "a",
        "ae",
        "p",
        "po",
        "pe",
        "s",
        "c",
        "z",
    ]
    negated_condition_codes = ["n" + cc for cc in condition_codes]
    all_condition_codes = condition_codes + negated_condition_codes
    if tok[0] == "j" and tok[1:] in all_condition_codes:
        return Opcode.JMPCC, None

    # otherwise just look it up by string representation of opcode
    for opcode in Opcode:
        op = str(opcode)
        if tok.startswith(op):
            suffix = tok[len(op) :]
            size = None
            if suffix == "b":
                size = 1
            elif suffix == "l":
                size = 4
            elif suffix == "q":
                size = 8

            if opcode in [Opcode.POP, Opcode.PUSH, Opcode.LEA]:
                size = 8
            return opcode, size

    # we don't recognize this opcode, but allow parsing to continue
    return Opcode.UNKNOWN, None


# parsing register names

REG_ALIASES = {
    "rax": (Register.AX, 8),
    "eax": (Register.AX, 4),
    "al": (Register.AX, 1),
    "rbx": (Register.BX, 8),
    "ebx": (Register.BX, 4),
    "bl": (Register.BX, 1),
    "rcx": (Register.CX, 8),
    "ecx": (Register.CX, 4),
    "cl": (Register.CX, 1),
    "rdx": (Register.DX, 8),
    "edx": (Register.DX, 4),
    "dl": (Register.DX, 1),
    "rdi": (Register.DI, 8),
    "edi": (Register.DI, 4),
    "dil": (Register.DI, 1),
    "rsi": (Register.SI, 8),
    "esi": (Register.SI, 4),
    "sil": (Register.SI, 1),
    "r8": (Register.R8, 8),
    "r8d": (Register.R8, 4),
    "r8b": (Register.R8, 1),
    "r9": (Register.R9, 8),
    "r9d": (Register.R9, 4),
    "r9b": (Register.R9, 1),
    "r10": (Register.R10, 8),
    "r10d": (Register.R10, 4),
    "r10b": (Register.R10, 1),
    "r11": (Register.R11, 8),
    "r11d": (Register.R11, 4),
    "r11b": (Register.R11, 1),
    "r12": (Register.R12, 8),
    "r12d": (Register.R12, 4),
    "r12b": (Register.R12, 1),
    "r13": (Register.R13, 8),
    "r13d": (Register.R13, 4),
    "r13b": (Register.R13, 1),
    "r14": (Register.R14, 8),
    "r14d": (Register.R14, 4),
    "r14b": (Register.R14, 1),
    "r15": (Register.R15, 8),
    "r15d": (Register.R15, 4),
    "r15b": (Register.R15, 1),
    "rsp": (Register.SP, 8),
    "rbp": (Register.BP, 8),
    "rip": (Register.IP, None),
    "xmm0": (Register.XMM0, None),
    "xmm1": (Register.XMM1, None),
    "xmm2": (Register.XMM2, None),
    "xmm3": (Register.XMM3, None),
    "xmm4": (Register.XMM4, None),
    "xmm5": (Register.XMM5, None),
    "xmm6": (Register.XMM6, None),
    "xmm7": (Register.XMM7, None),
    "xmm8": (Register.XMM8, None),
    "xmm9": (Register.XMM9, None),
    "xmm10": (Register.XMM10, None),
    "xmm11": (Register.XMM11, None),
    "xmm12": (Register.XMM12, None),
    "xmm13": (Register.XMM13, None),
    "xmm14": (Register.XMM14, None),
    "xmm15": (Register.XMM15, None),
}


def parse_register(toks: list[Token]) -> tuple[Register, Optional[int]]:
    """Parse register and infer its size in bytes

    <reg> ::= "%" <reg-alias>
    <reg-alias> ::= "rax" | "eax" | etc.
    """

    expect_next(toks=toks, expected=TokType.PERCENT)
    reg_name = toks.pop(0).tok_str
    try:
        return REG_ALIASES[reg_name]
    except KeyError:
        raise ParseError(f"expected register name after % but found {reg_name}")


def parse_immediate(toks: list[Token]) -> Immediate:
    """Parse an immediate value

    NOTE this won't correctly normalize signed/unsigned representations of same value
    e.g. -1 and 255 are the same in one-byte instructions but we won't parse them
    to the same Immediate operand here; we normalize them later in fix_immediate

    <immediate> ::= "$" [ "+" | "-" ] <int>
    <int> ::= ? decimal or hexadecimal integer ?
    """
    expect_next(toks=toks, expected=TokType.DOLLAR)

    next_tok = toks.pop(0)
    tok_type = next_tok.tok_type

    if tok_type == TokType.INT:
        val = int(next_tok.tok_str, base=0)
        return Immediate(val)
    elif tok_type in [TokType.PLUS_SIGN, TokType.MINUS_SIGN]:
        # next tok should val
        num_tok = toks.pop(0)
        if num_tok.tok_type != TokType.INT:
            raise ParseError(f"bad immediate value: ${next_tok}{num_tok.tok_str}")
        val = int(num_tok.tok_str, base=0)
        if tok_type == TokType.MINUS_SIGN:
            return Immediate(-val)
        return Immediate(val)
    else:
        raise ParseError(f"Bad immediate value: ${next_tok}")


def parse_expr(toks: list[Token]) -> Expr:
    """Parse an expression (used as displacement in memory operand)
    NOTE: we don't normalize these, so +10(%rbp) and 10(%rbp) will NOT compare equal

    <expr> ::= { <symbol> | <int> | "+" | "-" }+
    """
    expr: Expr = []
    while True:
        next_tok: Token = toks.pop(0)
        tok_typ = next_tok.tok_type
        if tok_typ == TokType.SYMBOL:
            expr.append(next_tok.tok_str)
        elif tok_typ == TokType.INT:
            expr.append(int(next_tok.tok_str, base=0))
        elif tok_typ == TokType.PLUS_SIGN:
            expr.append(Operator.PLUS)
        elif tok_typ == TokType.MINUS_SIGN:
            expr.append(Operator.MINUS)
        elif tok_typ == TokType.AT:
            expr.append(Operator.AT)
        else:
            # we didn't consume this so put it back on the list
            toks.insert(0, next_tok)
            break  # we're done
    return expr


def parse_memory_operand(toks: List[Token]) -> tuple[Operand, Optional[int]]:
    """
    Parse memory operand

    <memory-operand> ::= [ <expr> ] "(" <guts> ")"
    <guts> ::= <reg> [ "," <idx-and-or-scale> ] // base, with or without other stuff
            | "," <idx-and-or-scale> // no base

    <idx-and-or-scale> ::= <int> | <reg> [ "," [ <int> ]]
    """

    disp: Optional[Expr] = None
    base: Optional[Register] = None
    idx: Optional[Register] = None
    scale = 1

    # first get displacement if there is one
    if toks[0].tok_type != TokType.OPEN_PAREN:
        # next_tok is part of displacement
        disp = parse_expr(toks)
    expect_next(toks=toks, expected=TokType.OPEN_PAREN)

    # optional base
    if toks[0].tok_type == TokType.PERCENT:
        base, _ = parse_register(toks)

    # base register must be followed by close paren or comma
    next_tok = toks.pop(0)
    if next_tok.tok_type == TokType.CLOSE_PAREN:
        # we're done, no index or scale
        return asm.Memory(disp=disp, base=base), None
    # otherwise next token must be comma
    if next_tok.tok_type != TokType.COMMA:
        raise ParseError(
            "Unexpected token after base register in memory operand: " + str(toks)
        )

    # now parse index and scale
    next_tok_type = toks[0].tok_type
    if next_tok_type == TokType.INT:
        # it's a scale
        scale = int(toks.pop(0).tok_str, base=0)
    else:
        # it's an index register, possibly followed by scale
        idx, _ = parse_register(toks)

        # if there's a comma, consume it and check for scale
        if toks[0].tok_type == TokType.COMMA:
            toks.pop(0)
            if toks[0].tok_type == TokType.INT:  # type: ignore[comparison-overlap]
                scale = int(toks.pop(0).tok_str, base=0)

    expect_next(toks=toks, expected=TokType.CLOSE_PAREN)

    return asm.Memory(disp, base, idx, scale), None


def fix_immediate(op: Operand, size: Optional[int]) -> Operand:
    """Normalize immediate values to signed representation"""
    if isinstance(op, Immediate):
        if size is None:
            raise ParseError(
                "Can't interpret immediate b/c instruction size is ambigous"
            )
        if op < 0:
            return op

        as_bytes = op.to_bytes(length=size, byteorder="little", signed=False)
        from_bytes = int.from_bytes(as_bytes, byteorder="little", signed=True)
        return Immediate(from_bytes)

    # not an immediate so we don't need to change it
    return op


def parse_operand(toks: List[Token]) -> tuple[Operand, Optional[int]]:
    """Parse the next operand in list of tokens
    <operand> ::= <reg> | <immediate> | <symbol>["@" <symbol>]
    """
    start_tok_type = toks[0].tok_type

    if start_tok_type == TokType.PERCENT:
        return parse_register(toks)
    if start_tok_type == TokType.DOLLAR:
        return parse_immediate(toks), None
    if len(toks) == 1 and start_tok_type == TokType.SYMBOL:
        # it's a jump target or function name
        target = toks.pop(0).tok_str
        return (target, None)
    if start_tok_type == TokType.STAR:
        # jump targets like *%rax (not supported in the book)
        # HACK just return the register itself as an operand,
        # since we don't analyze jump targets aside from functino names
        toks.pop(0)
        return parse_register(toks)
    if (
        len(toks) == 3
        and start_tok_type == TokType.SYMBOL
        and toks[1].tok_type == TokType.AT
        and toks[2].tok_type == TokType.SYMBOL
    ):
        # it's a function name with a relocation, e.g. foo@PLT
        target = f"{toks[0].tok_str}@{toks[2].tok_str}"
        # consume all tokens from list
        toks.clear()
        return (target, None)

    # it must be a memory operand
    return parse_memory_operand(toks)


# deal with directives
# we just care about whether these move us in or out of the text section


class Directive:
    """Any directive"""


class EnterTextSection(Directive):
    """Directive that makes text section the current section"""


class LeaveTextSection(Directive):
    """Directive that makes any section other than text section the current section"""


# standalone section directives recognized by GNU or LLVM assembler (or both)

NON_TEXT_SECTIONS = [
    ".bss",
    ".data",
    ".cstring",
    ".rodata",
    ".literal4"  # we don't use this but you would if you implemented 'float'
    ".literal8",
    ".literal16",
    ".cstring",
]


def parse_directive(tok_list: List[Token]) -> Directive:
    """Parse a directive and figure out whether it enters the text section, exits it, or neither

    NOTE: unlike earlier parse_* statements, we don't need to consume these tokens.
    tok_list represents a single line of assembly and once we've identified the kind of directive
    we can just discard the rest of the line

    <directive> ::= <text-section> | <non-text-section> | <other-section>
    <text-section> ::= ".text"
                     | ".section" "__TEXT" "," "__text"
                     | ".section" ".text"
    <non-text-section> ::= ".section" <non-text-section name> | ".bss" | ".data" | etc.
    <other-section> ::= <non-section directive> { <any-token> }+
    <non-text-section-name> ::= ? anything other than .text or __TEXT,__text ?
    <non-section-directve> ::= ? any symbol starting with "." other than ".section", ".text", ".bss", etc ?
    """
    if tok_list[0].tok_str == ".text":
        return EnterTextSection()
    if tok_list[0].tok_str in NON_TEXT_SECTIONS:
        return LeaveTextSection()

    # we don't support the GNU assembler stack manipulation pseudo-ops
    if tok_list[0].tok_str in [".popsection", ".pushsection", ".previous"]:
        raise ParseError(f"{tok_list[0].tok_str} not supported")

    if tok_list[0].tok_str == ".section":
        if tok_list[1].tok_type != TokType.SYMBOL:
            raise ParseError(
                f"Expected section name after section directive, found {tok_list[1].tok_str}"
            )

        section_name = tok_list[1].tok_str
        if section_name == ".text":
            return EnterTextSection()

        # on macOS text section name is __TEXT,__text
        # note that other sections in __TEXT are NOT the text section
        # e.g. __TEXT,__cstring
        if section_name == "__TEXT" and tok_list[3].tok_str == "__text":
            return EnterTextSection()

        # otherwise this specifies some non-text section
        return LeaveTextSection()

    # as far as we can tell, it's not a section directive
    return Directive()


def parse_statement(
    tokens: Generator[Token, None, None]
) -> Union[asm.AsmItem, Directive]:
    """Parse the next instruction, label or directive

    Grammar:
    <statement> ::= <label> | <instruction> | <directive>
    <label> ::= <symbol> ":"
    <instruction> ::= <non-directive-symbol> [ <operand> {"," <operand> }] <statement-break>
    <statement-break> ::= "\n" | ";"
    <non-directive-symbol> ::= ? any symbol not starting with "." ?
    """

    # skip empty lines
    # # this will raise StopIteration if we run out of tokens
    first_token = next(tokens)
    while first_token.tok_type in [TokType.SEMICOLON, TokType.NEWLINE]:
        first_token = next(tokens)

    # labels, instructions and directives all start with symbol token
    if first_token.tok_type != TokType.SYMBOL:
        raise ParseError(
            f"Expected label, directive, or instruction but found {first_token.tok_str}"
        )

    # from here on, we use newline as default if tokens is exhausted
    # so we don't raise StopIteration
    nl = Token(TokType.NEWLINE, "\n")
    cur_token = next(tokens, nl)
    if cur_token.tok_type == TokType.COLON:
        # it's a label
        # note: if label is on its own line this won't consume the newline, which is fine
        return asm.Label(first_token.tok_str)

    # it's a directive or instruction, collect all tokens until end of line
    cur_line = [first_token]
    while cur_token.tok_type not in [TokType.SEMICOLON, TokType.NEWLINE]:
        cur_line.append(cur_token)
        cur_token = next(tokens, nl)

    if cur_line[0].tok_str.startswith("."):
        # it's a directive - figure out whether it's text directive,
        # another section direcive, or some other directive we don't care about
        # NOTE: we would treat floating-point values like .100 as directives
        # except that we should never see one at the start of a line
        return parse_directive(cur_line)

    # it's an instruction
    opcode_tok = cur_line.pop(0)
    opcode, size = parse_opcode(opcode_tok.tok_str)

    # now parse operands
    operands = []

    while cur_line:
        next_operand, maybe_size = parse_operand(cur_line)
        operands.append(next_operand)
        if maybe_size and not size:
            size = maybe_size
        # expect either comma followed by another operand, or end of list
        if cur_line:
            expect_next(toks=cur_line, expected=TokType.COMMA)
            if not tokens:
                raise ParseError("Expected another operand after comma")

    if size is not None:
        # if we could infer a size, use it to normalize any immediate values
        operands = [fix_immediate(op, size) for op in operands]
    return asm.Instruction(opcode, operands)


def parse_file(filename: Path) -> dict[str, asm.AssemblyFunction]:
    """Parse an assembly file"""

    asm_functions: dict[str, asm.AssemblyFunction] = {}

    def remove_prefix(s: str, prefix: str) -> str:
        """Backcompat-proof version of str.removeprefix"""
        if sys.version_info >= (3, 9):
            s.removeprefix(prefix)
        if s.startswith(prefix):
            return s[len(prefix) :]
        return s

    def add_fun(f: asm.AssemblyFunction) -> None:
        if sys.platform == "darwin":
            key = remove_prefix(f.name, "_")
        else:
            key = f.name
        asm_functions[key] = f

    with open(filename, "r", encoding="utf-8") as f:
        tokens = tokenize.tokenize(f)

        # add labels and assembly instructions to current assembly function
        # skip directives and labels outside of text section
        current_function: Optional[asm.AssemblyFunction] = None
        in_text_section = True

        while True:
            try:
                asm_item = parse_statement(tokens)

                if in_text_section:
                    # use directives to track current section but don't add them to parsed function
                    if isinstance(asm_item, Directive):
                        if isinstance(asm_item, LeaveTextSection):
                            # leaving the text section finishes the current function
                            if current_function:
                                add_fun(current_function)

                            in_text_section = False
                        # skip to next statement
                        continue

                    if isinstance(asm_item, asm.Label) and is_valid_c_identifier(
                        asm_item
                    ):
                        # we've found start of a new function
                        # NOTE: this assumes that we're not using internal labels
                        # that could be C function names (which we shouldn't be doing,
                        # since it's a potential naming conflict)
                        if current_function:
                            add_fun(current_function)
                        current_function = asm.AssemblyFunction(
                            name=asm_item, instructions=[]
                        )

                    elif current_function is None:
                        if isinstance(asm_item, asm.Instruction):
                            raise ParseError(
                                f"instruction found outside of function: {asm_item}"
                            )
                        # if it's a label, fine to be outside a function;
                        # it's just a static variable or something
                    else:
                        # add instruction to current function
                        current_function.instructions.append(asm_item)

                elif isinstance(asm_item, EnterTextSection):
                    in_text_section = True

                # if we're not in the text section and current statement doesn't put us back
                # in the text section, just ignore it

            except StopIteration:
                break  # end of file

    # we're done, append last function
    if current_function:
        add_fun(current_function)

    return asm_functions
