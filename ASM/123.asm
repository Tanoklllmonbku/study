global _main
extern _printf, _getch

section .data
    hello db 'Hello, World!', 10, 0

section .text
_main:
    push hello
    call _printf
    add esp, 4

    call _getch       ; Ожидает нажатия любой клавиши
    ret