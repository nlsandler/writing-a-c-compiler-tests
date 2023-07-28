    .bss
    .align 12 # 2^12 = 4096
    .zero 4084
    .globl _on_page_boundary
_on_page_boundary:
    .zero 10
