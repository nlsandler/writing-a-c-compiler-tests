"""Representation of assembly programs"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Union


# Operands ########################
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
    """+,-, and @ operators, which can appear in memory displacement expressions like:
    -4(%rbp)
    foo+10(%rbp)
    bar@GOTPCREL(%rip)
    """

    PLUS = auto()
    MINUS = auto()
    AT = auto()

    def __str__(self) -> str:
        if self == Operator.PLUS:
            return "+"
        if self == Operator.MINUS:
            return "-"
        if self == Operator.AT:
            return "@"
        raise NotImplementedError("what operator is this???")


# Expression representing an offset from some register
# all we do with these is compare them so we don't need a more structured representation here
# use List here for backwards compatibility with Python 3.8
Expr = List[Union[int, str, Operator]]


@dataclass
class Memory:
    """Memory operands (including RIP-relative, stack, indexed)"""

    disp: Optional[Expr] = None
    base: Optional[Register] = None
    idx: Optional[Register] = None
    scale: int = 1  # defaults to 1 if not specified

    def __str__(self) -> str:
        disp_str = "".join(map(str, self.disp or []))
        if (not self.idx) and self.scale == 1:
            return f"{disp_str}({self.base or ''})"
        return f"{disp_str}({self.base or ''}, {self.idx or ''}, {self.scale or ''})"


# type alias for target of jump or call instruction
Target = str

# an operand is a memory address, register, immediate value, or target
Operand = Union[Memory, Register, Immediate, Target]

# Instructions ########################


class Opcode(Enum):
    """All instructions we recognize

    Simplified, e.g. we don't distinguish between different conditional jumps
    consider further simplification, like using the same opcode for all unary computations
    (not, shr, neg, etc)"""

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
    CDQE = auto()  # not used in book, included here to distinguish from cdq
    # control flow and conditionals
    JMP = auto()
    JMPCC = auto()
    SETCC = auto()
    CMP = auto()
    CMOV = auto()
    TEST = auto()
    CALL = auto()
    RET = auto()
    LEAVE = auto()
    UNKNOWN = auto()

    def __str__(self) -> str:
        return self.name.lower()


@dataclass
class Instruction:
    """An assembly instruction consists of an opcode and a list of operands"""

    opcode: Opcode
    operands: list[Operand]

    def __str__(self) -> str:
        str_operands = ", ".join(map(str, self.operands))
        return f"\t{self.opcode} {str_operands}"


class Label(str):
    """A label within an assembly function"""

    def __str__(self) -> str:
        return super().__str__() + ":"


AsmItem = Union[Label, Instruction]


@dataclass
class AssemblyFunction:
    """An assembly function consists of a name and a list of instructions and internal labels"""

    name: Label
    instructions: list[AsmItem]

    def __str__(self) -> str:
        return f"{self.name}\n" + "\n".join(map(str, self.instructions))
