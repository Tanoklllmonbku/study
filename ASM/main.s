	.file	"main.cpp"
	.text
	.p2align 4,,15
	.def	___tcf_0;	.scl	3;	.type	32;	.endef
___tcf_0:
LFB1942:
	.cfi_startproc
	movl	$__ZStL8__ioinit, %ecx
	jmp	__ZNSt8ios_base4InitD1Ev
	.cfi_endproc
LFE1942:
	.p2align 4,,15
	.globl	__Z12ArrayReverseiPi
	.def	__Z12ArrayReverseiPi;	.scl	2;	.type	32;	.endef
__Z12ArrayReverseiPi:
LFB1510:
	.cfi_startproc
	pushl	%esi
	.cfi_def_cfa_offset 8
	.cfi_offset 6, -8
	pushl	%ebx
	.cfi_def_cfa_offset 12
	.cfi_offset 3, -12
	movl	12(%esp), %edx
	movl	%edx, %ecx
	shrl	$31, %ecx
	addl	%edx, %ecx
	sarl	%ecx
	testl	%ecx, %ecx
	jle	L2
	movl	16(%esp), %eax
	leal	-4(%eax,%edx,4), %edx
	leal	(%eax,%ecx,4), %ebx
	.p2align 4,,10
L5:
	movl	(%edx), %esi
	movl	(%eax), %ecx
	addl	$4, %eax
	subl	$4, %edx
	movl	%esi, -4(%eax)
	movl	%ecx, 4(%edx)
	cmpl	%eax, %ebx
	jne	L5
L2:
	popl	%ebx
	.cfi_restore 3
	.cfi_def_cfa_offset 8
	popl	%esi
	.cfi_restore 6
	.cfi_def_cfa_offset 4
	ret
	.cfi_endproc
LFE1510:
	.section .rdata,"dr"
LC0:
	.ascii ".\12\0"
LC1:
	.ascii ", \0"
	.text
	.p2align 4,,15
	.globl	__Z9ArrayReadiPKi
	.def	__Z9ArrayReadiPKi;	.scl	2;	.type	32;	.endef
__Z9ArrayReadiPKi:
LFB1511:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	pushl	%edi
	.cfi_def_cfa_offset 12
	.cfi_offset 7, -12
	pushl	%esi
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	pushl	%ebx
	.cfi_def_cfa_offset 20
	.cfi_offset 3, -20
	xorl	%ebx, %ebx
	subl	$28, %esp
	.cfi_def_cfa_offset 48
	movl	48(%esp), %edi
	movl	52(%esp), %ebp
	cmpl	$1, %edi
	leal	-1(%edi), %esi
	jle	L10
	.p2align 4,,10
L12:
	movl	0(%ebp,%ebx,4), %eax
	movl	$__ZSt4cout, %ecx
	addl	$1, %ebx
	movl	%eax, (%esp)
	call	__ZNSolsEi
	.cfi_def_cfa_offset 44
	subl	$4, %esp
	.cfi_def_cfa_offset 48
	movl	$2, 8(%esp)
	movl	$LC1, 4(%esp)
	movl	%eax, (%esp)
	call	__ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_i
	cmpl	%ebx, %esi
	jne	L12
L10:
	movl	-4(%ebp,%edi,4), %eax
	movl	$__ZSt4cout, %ecx
	movl	%eax, (%esp)
	call	__ZNSolsEi
	.cfi_def_cfa_offset 44
	subl	$4, %esp
	.cfi_def_cfa_offset 48
	movl	$2, 8(%esp)
	movl	$LC0, 4(%esp)
	movl	%eax, (%esp)
	call	__ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_i
	addl	$28, %esp
	.cfi_def_cfa_offset 20
	popl	%ebx
	.cfi_restore 3
	.cfi_def_cfa_offset 16
	popl	%esi
	.cfi_restore 6
	.cfi_def_cfa_offset 12
	popl	%edi
	.cfi_restore 7
	.cfi_def_cfa_offset 8
	popl	%ebp
	.cfi_restore 5
	.cfi_def_cfa_offset 4
	ret
	.cfi_endproc
LFE1511:
	.def	___main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
LC2:
	.ascii "Array: \12\0"
LC3:
	.ascii "Array length: \0"
LC4:
	.ascii "\12\0"
LC5:
	.ascii "Reversed array: \12\0"
LC6:
	.ascii "Press any key for continue...\0"
	.section	.text.startup,"x"
	.p2align 4,,15
	.globl	_main
	.def	_main;	.scl	2;	.type	32;	.endef
_main:
LFB1512:
	.cfi_startproc
	leal	4(%esp), %ecx
	.cfi_def_cfa 1, 0
	andl	$-16, %esp
	pushl	-4(%ecx)
	pushl	%ebp
	.cfi_escape 0x10,0x5,0x2,0x75,0
	movl	%esp, %ebp
	pushl	%ebx
	pushl	%ecx
	.cfi_escape 0xf,0x3,0x75,0x78,0x6
	.cfi_escape 0x10,0x3,0x2,0x75,0x7c
	leal	-28(%ebp), %ebx
	subl	$48, %esp
	call	___main
	movl	$LC2, 4(%esp)
	movl	$__ZSt4cout, (%esp)
	movl	$1, -28(%ebp)
	movl	$2, -24(%ebp)
	movl	$3, -20(%ebp)
	movl	$4, -16(%ebp)
	movl	$5, -12(%ebp)
	call	__ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movl	%ebx, 4(%esp)
	movl	$5, (%esp)
	call	__Z9ArrayReadiPKi
	movl	$LC3, 4(%esp)
	movl	$__ZSt4cout, (%esp)
	call	__ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movl	$__ZSt4cout, %ecx
	movl	$5, (%esp)
	call	__ZNSolsEi
	subl	$4, %esp
	movl	$LC4, 4(%esp)
	movl	%eax, (%esp)
	call	__ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movl	$LC5, 4(%esp)
	movl	$__ZSt4cout, (%esp)
	call	__ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movl	-28(%ebp), %eax
	movl	-12(%ebp), %edx
	movl	%ebx, 4(%esp)
	movl	$5, (%esp)
	movl	%edx, -28(%ebp)
	movl	%eax, -12(%ebp)
	movl	-16(%ebp), %edx
	movl	-24(%ebp), %eax
	movl	%edx, -24(%ebp)
	movl	%eax, -16(%ebp)
	call	__Z9ArrayReadiPKi
	movl	$LC6, 4(%esp)
	movl	$__ZSt4cout, (%esp)
	call	__ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movl	$__ZSt3cin, %ecx
	call	__ZNSi3getEv
	leal	-8(%ebp), %esp
	xorl	%eax, %eax
	popl	%ecx
	.cfi_restore 1
	.cfi_def_cfa 1, 0
	popl	%ebx
	.cfi_restore 3
	popl	%ebp
	.cfi_restore 5
	leal	-4(%ecx), %esp
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE1512:
	.p2align 4,,15
	.def	__GLOBAL__sub_I__Z12ArrayReverseiPi;	.scl	3;	.type	32;	.endef
__GLOBAL__sub_I__Z12ArrayReverseiPi:
LFB1943:
	.cfi_startproc
	subl	$28, %esp
	.cfi_def_cfa_offset 32
	movl	$__ZStL8__ioinit, %ecx
	call	__ZNSt8ios_base4InitC1Ev
	movl	$___tcf_0, (%esp)
	call	_atexit
	addl	$28, %esp
	.cfi_def_cfa_offset 4
	ret
	.cfi_endproc
LFE1943:
	.section	.ctors,"w"
	.align 4
	.long	__GLOBAL__sub_I__Z12ArrayReverseiPi
.lcomm __ZStL8__ioinit,1,1
	.ident	"GCC: (MinGW.org GCC-6.3.0-1) 6.3.0"
	.def	__ZNSt8ios_base4InitD1Ev;	.scl	2;	.type	32;	.endef
	.def	__ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	__ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_i;	.scl	2;	.type	32;	.endef
	.def	__ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	__ZNSi3getEv;	.scl	2;	.type	32;	.endef
	.def	__ZNSt8ios_base4InitC1Ev;	.scl	2;	.type	32;	.endef
	.def	_atexit;	.scl	2;	.type	32;	.endef
