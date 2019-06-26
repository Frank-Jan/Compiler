.data
nl: .asciiz "\n"
.text

main:
	li $t0, 1
	j for_loop # jumps to for loop
	
for_loop:
	la $a0, ($t0) #the adress of $t0 in $a0
	li $v0, 1  #print the integer in $a0
	syscall
	
	la $a0, nl # load adress from nl in $a1
	li $v0, 4 # print string
	syscall # works only with $v0
	
	add $t0, $t0, 1 # adds 1 to itself, !!!sequence!!!
	beq $t0, 11, exit #exit when $t0 == 10
	j for_loop # jumps back to for_loop
	
exit:
	li $v0, 10
	syscall