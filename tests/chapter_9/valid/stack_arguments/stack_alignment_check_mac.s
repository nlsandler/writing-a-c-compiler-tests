    .text
    .globl _even_arguments
_even_arguments:
    stp     x29, x30, [sp, #-16]!   // Push frame pointer and link register
    mov     x29, sp

    // Validate arguments 1–8
    mov     w9, #1
    cmp     w0, w9
    b.ne    Lfail_even_arguments

    mov     w9, #2
    cmp     w1, w9
    b.ne    Lfail_even_arguments

    mov     w9, #3
    cmp     w2, w9
    b.ne    Lfail_even_arguments

    mov     w9, #4
    cmp     w3, w9
    b.ne    Lfail_even_arguments

    mov     w9, #5
    cmp     w4, w9
    b.ne    Lfail_even_arguments

    mov     w9, #6
    cmp     w5, w9
    b.ne    Lfail_even_arguments

    mov     w9, #7
    cmp     w6, w9
    b.ne    Lfail_even_arguments

    mov     w9, #8
    cmp     w7, w9
    b.ne    Lfail_even_arguments

    // Check stack alignment
    mov     x9, sp
    and     x9, x9, #15             // x9 = sp % 16
    cbnz    x9, Lfail_even_arguments

    mov     w0, #1                  // return 1
    ldp     x29, x30, [sp], #16
    ret

Lfail_even_arguments:
    mov     w0, #-1
    bl      _exit
    ldp     x29, x30, [sp], #16
    ret

.globl _odd_arguments
_odd_arguments:
    stp     x29, x30, [sp, #-16]!
    mov     x29, sp

    // Validate arguments 1–8
    mov     w9, #1
    cmp     w0, w9
    b.ne    Lfail_odd_arguments

    mov     w9, #2
    cmp     w1, w9
    b.ne    Lfail_odd_arguments

    mov     w9, #3
    cmp     w2, w9
    b.ne    Lfail_odd_arguments

    mov     w9, #4
    cmp     w3, w9
    b.ne    Lfail_odd_arguments

    mov     w9, #5
    cmp     w4, w9
    b.ne    Lfail_odd_arguments

    mov     w9, #6
    cmp     w5, w9
    b.ne    Lfail_odd_arguments

    mov     w9, #7
    cmp     w6, w9
    b.ne    Lfail_odd_arguments

    mov     w9, #8
    cmp     w7, w9
    b.ne    Lfail_odd_arguments

    ldr     w9, [x29, #16]
    cmp     w9, #9
    b.ne    Lfail_odd_arguments
    
    // Check stack alignment
    mov     x9, sp
    and     x9, x9, #15
    cbnz    x9, Lfail_odd_arguments

    mov     w0, #1
    ldp     x29, x30, [sp], #16
    ret

Lfail_odd_arguments:
    mov     w0, #-2
    bl      _exit
    ldp     x29, x30, [sp], #16
    ret
