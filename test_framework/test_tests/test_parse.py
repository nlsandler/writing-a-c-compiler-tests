"""Tests for assembly parser"""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

from ..parser import parse
from ..parser.asm import (
    AssemblyFunction,
    Immediate,
    Instruction,
    Label,
    Memory,
    Opcode,
    Operator,
    Register,
)


class ParseTestCase(unittest.TestCase):
    """Tests for assembly parser"""

    # assembly for the program:
    # .globl main; main: movl $2, %eax; ret
    # we reuse this for several tests
    BASIC_PROGRAM = AssemblyFunction(
        name=Label("main"),
        instructions=[
            Instruction(Opcode.MOV, [Immediate(2), Register.AX]),
            Instruction(Opcode.RET, []),
        ],
    )

    def setUp(self) -> None:
        """Patch sys.platform so tests work the same on alll platforms"""
        self.platform_patcher = patch("sys.platform", new="linux")
        self.platform_patcher.start()

    def tearDown(self) -> None:
        self.platform_patcher.stop()

    def assertExpectedAssembly(
        self, asm_text: str, expected_asm: AssemblyFunction, target_fun: str = "main"
    ) -> None:
        """Shared logic for parsing tests"""
        mockfile = mock_open(read_data=asm_text)
        with patch("builtins.open", mockfile):
            actual_assembly = parse.parse_file(Path("dummy.asm"))[target_fun]
            self.assertEqual(actual_assembly.name, expected_asm.name)
            self.assertListEqual(
                actual_assembly.instructions, expected_asm.instructions
            )

    def test_simple(self) -> None:
        """We can parse a simple assembly program"""
        asm = """
    .globl main
main:
    movl $2, %eax
    ret
"""
        self.assertExpectedAssembly(asm, self.BASIC_PROGRAM)

    def test_semicolon_linesep(self) -> None:
        """Parser correctly handles semicolons used as line separators"""
        asm = """.globl main; main:; movl $2, %eax; ret"""

        self.assertExpectedAssembly(asm, self.BASIC_PROGRAM)

    def test_label_sameline(self) -> None:
        """Label on same line as instruction"""
        asm = """
    .globl main
main: movl $2, %eax
    ret
"""
        self.assertExpectedAssembly(asm, self.BASIC_PROGRAM)

    def test_internal_label(self) -> None:
        """Parse labels that aren't function names"""
        asm = """
    .globl main
main: .L1: .L2: jmp .L1
    jne .L2
    another.lbl: ret
"""
        expected_assembly = AssemblyFunction(
            name=Label("main"),
            instructions=[
                Label(".L1"),
                Label(".L2"),
                Instruction(Opcode.JMP, [".L1"]),
                Instruction(Opcode.JMPCC, [".L2"]),
                Label("another.lbl"),
                Instruction(Opcode.RET, []),
            ],
        )

        self.assertExpectedAssembly(asm, expected_assembly)

    def test_ignore_whitespace(self) -> None:
        """Ignore whitespace"""
        asm = """\tmain :   movl   $\t1 ,% eax; .L   :jmp main
addq $1,-4(  %rbp  )
.section whatever
foo: ret
"""
        expected_assembly = AssemblyFunction(
            name=Label("main"),
            instructions=[
                Instruction(Opcode.MOV, [Immediate(1), Register.AX]),
                Label(".L"),
                Instruction(Opcode.JMP, ["main"]),
                Instruction(
                    Opcode.ADD,
                    [
                        Immediate(1),
                        Memory(disp=[Operator.MINUS, 4], base=Register.BP),
                    ],
                ),
            ],
        )
        self.assertExpectedAssembly(asm, expected_assembly)

    def test_operands(self) -> None:
        """Parse various instruction operands"""
        asm = """
main:
    pushq $-1 # negative immediate
    pushq $ + 55 # positive immediate
    pushq $0x1af4b # hex immediate
    movb $1, %sil # one-byte register
    movq % xmm15, %xmm0 # XMM registers
    pushq foo(%rip) # RIP-relative variable
    pushq var4u+10(%rip) # RIP-relative variable + offset
    pushq foo@GOTPCREL(%rip) # address in GOT (not covered in the book)

    # base w/out index or scale
    lea (%rip), %rax
    lea 10(%r8d), %rax # displacement and base, no index or scale

    # index w/out base or scale
    lea 0xc(,%rax,), %rax # displacment (in hexadecimal)
    lea (,%rax, ), %rax

    # scale w/out base or index
    lea (,1), %rax
    lea -0x10 (,1), %rax

    # base and index w/out scale
    pushq (%rbp, %rax,)
    pushq (%rbp, %rax)

    # index and scale w/ no base
    lea 10(,%rdi,4), %rax

    # base and scale w/ no index
    lea (%rax,1), %rax

    # all three
    pushq (%rbp, %rax, 8)
"""

        expected_assembly = AssemblyFunction(
            name=Label("main"),
            instructions=[
                Instruction(Opcode.PUSH, [Immediate(-1)]),
                Instruction(Opcode.PUSH, [Immediate(55)]),
                Instruction(Opcode.PUSH, [Immediate(0x1AF4B)]),
                Instruction(Opcode.MOV, [Immediate(1), Register.SI]),
                Instruction(Opcode.MOV, [Register.XMM15, Register.XMM0]),
                Instruction(
                    Opcode.PUSH,
                    [Memory(disp=["foo"], base=Register.IP)],
                ),
                Instruction(
                    Opcode.PUSH,
                    [Memory(disp=["var4u", Operator.PLUS, 10], base=Register.IP)],
                ),
                Instruction(
                    Opcode.PUSH,
                    [Memory(disp=["foo", Operator.AT, "GOTPCREL"], base=Register.IP)],
                ),
                Instruction(Opcode.LEA, [Memory(base=Register.IP), Register.AX]),
                Instruction(
                    Opcode.LEA, [Memory(disp=[10], base=Register.R8), Register.AX]
                ),
                Instruction(
                    Opcode.LEA, [Memory(disp=[0xC], idx=Register.AX), Register.AX]
                ),
                Instruction(Opcode.LEA, [Memory(idx=Register.AX), Register.AX]),
                Instruction(Opcode.LEA, [Memory(), Register.AX]),
                Instruction(
                    Opcode.LEA, [Memory(disp=[Operator.MINUS, 0x10]), Register.AX]
                ),
                Instruction(Opcode.PUSH, [Memory(base=Register.BP, idx=Register.AX)]),
                Instruction(Opcode.PUSH, [Memory(base=Register.BP, idx=Register.AX)]),
                Instruction(
                    Opcode.LEA,
                    [Memory(disp=[10], idx=Register.DI, scale=4), Register.AX],
                ),
                Instruction(Opcode.LEA, [Memory(base=Register.AX), Register.AX]),
                Instruction(
                    Opcode.PUSH, [Memory(base=Register.BP, idx=Register.AX, scale=8)]
                ),
            ],
        )

        self.assertExpectedAssembly(asm, expected_assembly)

    def test_targets(self) -> None:
        """Parse various targets of function calls"""
        asm = """
main:
    call _foo12_3
    call f_
    call __
    call f@PLT
"""
        expected_assembly = AssemblyFunction(
            name=Label("main"),
            instructions=[
                Instruction(Opcode.CALL, ["_foo12_3"]),
                Instruction(Opcode.CALL, ["f_"]),
                Instruction(Opcode.CALL, ["__"]),
                Instruction(Opcode.CALL, ["f@PLT"]),
            ],
        )
        self.assertExpectedAssembly(asm, expected_assembly)

    def test_mnemonics(self) -> None:
        """Parse various instruction mnemonics"""
        asm = """
main:
    # various mnemonics (both Intel and AT&T) for sign-extending AX into DX in various sizes
    cqo ; cqto; cltd; cdq
    # sign-extending AX into AX at various sizes
    clt; cltq; cdqe # LLVM assembler recognizes 'clt' but GAS does not
    # condition codes
    setne %al; sete %bl; setg %cl; setge %dl; setpo %dil
    jl X; jle X; ja X; jae X; jb X; jbe X
    # movsx/movz
    movsx %eax, %r12
    movsbl %sil, %r13d
    movslq %r13d, %r14
    movsbq %r8b, %r15
    movsb %sil, %r13d
    movsl %r13d, %r14
    movzbl %sil, %r13d
    movzbq %r8b, %r15
    movzb %sil, %r13d
    # floating-point
    comisd -8(%rbp), %xmm4
    movsd %xmm0, 8(%rbp)
    mulsd %xmm2, %xmm3
    divsd %xmm5, %xmm6
    # mov
    movb $1, -3(%rbp)
    movl $1, %eax
    movq $1, %rax
    mov $1, %eax

    # instructions w/ only quadword suffixes
    push $1; pushq $2
    pop %rax; popq %rbx
    lea (%rax), %rax; leaq (%rax), %rax
    callq f; retq

    # other stuff
    cvttsd2si %xmm7, %rax; cvttsd2siq %xmm8, %rax
    cvtsi2sd %r10, %xmm9; cvtsi2sdl %r11d, %xmm10
    addq $10, -8(%rbp); add $-0x100, %rax
    subl %ebx, %ecx
    idiv %rax; idivq -8(%rbp)
    imul $40, %rax
    cmp %rax, -8(%rbp); cmpl $100, %eax
    xor %eax, %eax; andq $1, %rax; orl foo(%rip), %eax
    shrq -8(%rbp); shr %eax; notl -8(%rbp); neg %rax
"""

        expected_assembly = AssemblyFunction(
            name=Label("main"),
            instructions=[
                # sign extend AX to DX
                Instruction(Opcode.CDQ, []),
                Instruction(Opcode.CDQ, []),
                Instruction(Opcode.CDQ, []),
                Instruction(Opcode.CDQ, []),
                # sign extend w/in AX
                Instruction(Opcode.CDQE, []),
                Instruction(Opcode.CDQE, []),
                Instruction(Opcode.CDQE, []),
                # conditionals
                Instruction(Opcode.SETCC, [Register.AX]),
                Instruction(Opcode.SETCC, [Register.BX]),
                Instruction(Opcode.SETCC, [Register.CX]),
                Instruction(Opcode.SETCC, [Register.DX]),
                Instruction(Opcode.SETCC, [Register.DI]),
                Instruction(Opcode.JMPCC, ["X"]),
                Instruction(Opcode.JMPCC, ["X"]),
                Instruction(Opcode.JMPCC, ["X"]),
                Instruction(Opcode.JMPCC, ["X"]),
                Instruction(Opcode.JMPCC, ["X"]),
                Instruction(Opcode.JMPCC, ["X"]),
                Instruction(Opcode.MOVS, [Register.AX, Register.R12]),
                Instruction(Opcode.MOVS, [Register.SI, Register.R13]),
                Instruction(Opcode.MOVS, [Register.R13, Register.R14]),
                Instruction(Opcode.MOVS, [Register.R8, Register.R15]),
                Instruction(Opcode.MOVS, [Register.SI, Register.R13]),
                Instruction(Opcode.MOVS, [Register.R13, Register.R14]),
                Instruction(Opcode.MOVZ, [Register.SI, Register.R13]),
                Instruction(Opcode.MOVZ, [Register.R8, Register.R15]),
                Instruction(Opcode.MOVZ, [Register.SI, Register.R13]),
                Instruction(
                    Opcode.CMP,
                    [
                        Memory(disp=[Operator.MINUS, 8], base=Register.BP),
                        Register.XMM4,
                    ],
                ),
                Instruction(
                    Opcode.MOV, [Register.XMM0, Memory(disp=[8], base=Register.BP)]
                ),
                Instruction(Opcode.IMUL, [Register.XMM2, Register.XMM3]),
                Instruction(Opcode.DIV, [Register.XMM5, Register.XMM6]),
                Instruction(
                    Opcode.MOV,
                    [Immediate(1), Memory(disp=[Operator.MINUS, 3], base=Register.BP)],
                ),
                Instruction(
                    Opcode.MOV,
                    [Immediate(1), Register.AX],
                ),
                Instruction(
                    Opcode.MOV,
                    [Immediate(1), Register.AX],
                ),
                Instruction(
                    Opcode.MOV,
                    [Immediate(1), Register.AX],
                ),
                Instruction(Opcode.PUSH, [Immediate(1)]),
                Instruction(Opcode.PUSH, [Immediate(2)]),
                Instruction(Opcode.POP, [Register.AX]),
                Instruction(Opcode.POP, [Register.BX]),
                Instruction(Opcode.LEA, [Memory(base=Register.AX), Register.AX]),
                Instruction(Opcode.LEA, [Memory(base=Register.AX), Register.AX]),
                Instruction(Opcode.CALL, ["f"]),
                Instruction(Opcode.RET, []),
                Instruction(Opcode.CVTTSD2SI, [Register.XMM7, Register.AX]),
                Instruction(Opcode.CVTTSD2SI, [Register.XMM8, Register.AX]),
                Instruction(Opcode.CVTSI2SD, [Register.R10, Register.XMM9]),
                Instruction(Opcode.CVTSI2SD, [Register.R11, Register.XMM10]),
                Instruction(
                    Opcode.ADD,
                    [Immediate(10), Memory(disp=[Operator.MINUS, 8], base=Register.BP)],
                ),
                Instruction(Opcode.ADD, [Immediate(-0x100), Register.AX]),
                Instruction(Opcode.SUB, [Register.BX, Register.CX]),
                Instruction(Opcode.IDIV, [Register.AX]),
                Instruction(
                    Opcode.IDIV, [Memory(disp=[Operator.MINUS, 8], base=Register.BP)]
                ),
                Instruction(Opcode.IMUL, [Immediate(40), Register.AX]),
                Instruction(
                    Opcode.CMP,
                    [Register.AX, Memory(disp=[Operator.MINUS, 8], base=Register.BP)],
                ),
                Instruction(Opcode.CMP, [Immediate(100), Register.AX]),
                Instruction(Opcode.XOR, [Register.AX, Register.AX]),
                Instruction(Opcode.AND, [Immediate(1), Register.AX]),
                Instruction(
                    Opcode.OR, [Memory(disp=["foo"], base=Register.IP), Register.AX]
                ),
                Instruction(
                    Opcode.SHR, [Memory(disp=[Operator.MINUS, 8], base=Register.BP)]
                ),
                Instruction(Opcode.SHR, [Register.AX]),
                Instruction(
                    Opcode.NOT, [Memory(disp=[Operator.MINUS, 8], base=Register.BP)]
                ),
                Instruction(Opcode.NEG, [Register.AX]),
            ],
        )
        self.assertExpectedAssembly(asm, expected_assembly)

    def test_multi_function(self) -> None:
        """Given multiple functions (and global variables), extract the right one"""
        asm = """
        .globl foo
foo:
    movl $1, %eax
    ret
bar:
    movq $2, %rax
foobar:
    movq %rdi, %rax
    ret
    .section bss
foof:
    .zero 100
    .text
_foobar:
    movl %r8d, %eax
    ret
        """
        foo_asm = AssemblyFunction(
            name=Label("foo"),
            instructions=[
                Instruction(Opcode.MOV, [Immediate(1), Register.AX]),
                Instruction(Opcode.RET, []),
            ],
        )
        bar_asm = AssemblyFunction(
            name=Label("bar"),
            instructions=[
                Instruction(Opcode.MOV, [Immediate(2), Register.AX]),
            ],
        )
        foobar_asm = AssemblyFunction(
            name=Label("foobar"),
            instructions=[
                Instruction(Opcode.MOV, [Register.DI, Register.AX]),
                Instruction(Opcode.RET, []),
            ],
        )
        _foobar_asm = AssemblyFunction(
            name=Label("_foobar"),
            instructions=[
                Instruction(Opcode.MOV, [Register.R8, Register.AX]),
                Instruction(Opcode.RET, []),
            ],
        )
        for expected in [foo_asm, bar_asm, foobar_asm, _foobar_asm]:
            self.assertExpectedAssembly(asm, expected, target_fun=expected.name)

    def test_directives_and_comments(self) -> None:
        """Ignore directives and comments"""
        asm = """
    .text
    .globl main # here's a comment
main:
    # another comment
    .cfi_startproc
    movl $2, %eax
    ret
    .cfi_endproc
    .section .debug_stuff
.Lsome_info:
    .byte 1
    .byte 2
"""
        self.assertExpectedAssembly(asm, self.BASIC_PROGRAM)

    def test_section_directives(self) -> None:
        """Correctly identify directives to enter or leave text section"""
        asm = """
    .text
foo:
    ret
    .data
.Lsomeconst:
    .string "Hello world"
    .section .rodata
    .section .text
bar:
    ret
    .bss
.Lblah:
    .zero 4
    .text
baz:
    ret
"""
        expected_foo = AssemblyFunction(Label("foo"), [Instruction(Opcode.RET, [])])
        expected_bar = AssemblyFunction(Label("bar"), [Instruction(Opcode.RET, [])])
        expected_baz = AssemblyFunction(Label("baz"), [Instruction(Opcode.RET, [])])
        self.assertExpectedAssembly(asm, expected_foo, target_fun="foo")
        self.assertExpectedAssembly(asm, expected_bar, target_fun="bar")
        self.assertExpectedAssembly(asm, expected_baz, target_fun="baz")

    def test_normalize_operands(self) -> None:
        """Recognize when positive and negative immediates have same value"""
        asm1 = """
main:
        movb $-5, %al
        add $-22, %eax
        subl $-8, -8(%rbp)
        push $-200
        movq $-2147483640, -4(%rax)
"""

        asm2 = """
main:
        movb $251, %al
        add $4294967274, %eax
        subl $4294967288, -8(%rbp)
        pushq $18446744073709551416
        movq $18446744071562067976, -4(%rax)
"""
        mock1 = mock_open(read_data=asm1)
        mock2 = mock_open(read_data=asm2)
        instructions1 = []
        instructions2 = []
        with patch("builtins.open", mock1):
            asm1_parsed = parse.parse_file(Path("dummy.asm"))["main"]
            instructions1 = asm1_parsed.instructions

        with patch("builtins.open", mock2):
            asm2_parsed = parse.parse_file(Path("dummy.asm"))["main"]
            instructions2 = asm2_parsed.instructions

        self.assertListEqual(instructions1, instructions2)

    @patch("sys.platform", new="darwin")
    def test_internal_label_macos(self) -> None:
        """Parse labels that aren't function names according to macOS naming conventions"""
        asm = """
    .globl _main
_main: L1: L2: jmp L1
    jne L2
    # shouldn't recognize another.lbl as a function b/c of '.'
    _another.lbl: ret
"""
        expected_assembly = AssemblyFunction(
            name=Label("_main"),
            instructions=[
                Label("L1"),
                Label("L2"),
                Instruction(Opcode.JMP, ["L1"]),
                Instruction(Opcode.JMPCC, ["L2"]),
                Label("_another.lbl"),
                Instruction(Opcode.RET, []),
            ],
        )

        self.assertExpectedAssembly(asm, expected_assembly)

    @patch("sys.platform", new="darwin")
    def test_multi_function_macos(self) -> None:
        """Parse multiple functions with macos naming conventions and extract the right one"""
        asm = """
        .globl _foo
_foo:
    movl $1, %eax
    ret
_bar:
    movq $2, %rax
_foobar:
    movq %rdi, %rax
    ret
    .cstring
_foof:
    .string "Hello"
    .section __TEXT,__text
__foobar:
    movl %r8d, %eax
    ret
        """
        foo_asm = AssemblyFunction(
            name=Label("_foo"),
            instructions=[
                Instruction(Opcode.MOV, [Immediate(1), Register.AX]),
                Instruction(Opcode.RET, []),
            ],
        )
        bar_asm = AssemblyFunction(
            name=Label("_bar"),
            instructions=[
                Instruction(Opcode.MOV, [Immediate(2), Register.AX]),
            ],
        )
        foobar_asm = AssemblyFunction(
            name=Label("_foobar"),
            instructions=[
                Instruction(Opcode.MOV, [Register.DI, Register.AX]),
                Instruction(Opcode.RET, []),
            ],
        )
        _foobar_asm = AssemblyFunction(
            name=Label("__foobar"),
            instructions=[
                Instruction(Opcode.MOV, [Register.R8, Register.AX]),
                Instruction(Opcode.RET, []),
            ],
        )
        for expected in [foo_asm, bar_asm, foobar_asm, _foobar_asm]:
            self.assertExpectedAssembly(asm, expected, target_fun=expected.name[1:])
