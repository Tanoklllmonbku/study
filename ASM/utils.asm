section .text

; --- print_str(строка) ---
global _print_str
extern _printf

_print_str:
    push ebp
    mov ebp, esp
    
    push dword [ebp + 8]  ; Передаем строку
    call _printf
    add esp, 4
    
    pop ebp
    ret

; --- sum_numbers(a, b) ---
global _sum_numbers

_sum_numbers:
    push ebp
    mov ebp, esp
    
    mov eax, [ebp + 8]    ; a
    add eax, [ebp + 12]   ; +b
    
    pop ebp
    ret