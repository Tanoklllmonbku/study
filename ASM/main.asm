global _main
extern _print_str, _sum_numbers, _printf, _getch

section .data
    hello db "Hello from main!", 10, 0
    sum_msg db "5 + 3 = %d", 10, 0

section .text
_main:
    push hello
    call _print_str
    add esp, 4

    push 3
    push 5
    call _sum_numbers
    add esp, 8

    push eax
    push sum_msg
    call _printf
    add esp, 8

    call _getch
    mov eax, 0  ; Возвращаем 0
    ret