.data
	endline: .asciiz "\n"

.text 
main:
	li $s0, 2 #load 2 in $s0
	li $s1, 3 #load 2 in $s1
	
	move $a0, $s0 #move the val 2 from $s0 to $a0(2)
	move $a1, $s1 #move the val 3 from $s1 to $a1(3)
	
	#solution:
	# pushing 2 and 3 on the stack
	addi $sp, $sp, -8 #stack pointer needs to move 8 bytes (2 values)
	sw $s0, 4($sp) #store the value of $s0 in 4 bytes "lower" than the stackpointer
	sw $s1, 0($sp) #store the value of $s1 on the place where the stackpointer "points"
	
	jal sum_add_one #jump and link to the function sum_add_one
			#$ra contains this adress
	
	move $a0, $v0 #move the val 6 from $v0 to $a0(6)
	li $v0, 1 #print the integer (6) in $v0
	syscall # the first sum is correctly calculated
	
	li $v0, 4 #print a string
	la $a0, endline #load the adress of "endline" in $a0
	syscall # prints the "endline"
	
	#solution:
	lw $s0, ($sp) #load the val where the $sp points to in $s0
	addi $sp, $sp, 4 #stack pointer needs to move 4 bytes (1 value)
	lw $s1, ($sp) #load the val where the $sp points to in $s1
	addi $sp, $sp, 4 #stack pointer needs to move 4 bytes (1 value)
	
	#here's the mistake made, he changed in his previous calculation the registers $s0 and $s1,
	#so the values aren't 2 and 3, but 1 and 2
	add $s2, $s0, $s1 #add the vals from $s0 (1) and $s1 (2) in $s2 (3)
	move $a0, $s2 #move the val 3 from $s2 to $a0(3)
	li $v0, 1 #print the integer in $a0
	syscall #prints
	
	li $v0, 10 #system call for exit
	syscall #system call for exit
	
sum_add_one:
	li $s0, 1 #load the val 1 in $s0 (the val 2 in $s0 is gone)
	move $s1, $a0 #move the val 2 from $a0 to $s1
	move $s2, $a1 #move the val 3 from $a1 to $s2
	add $t0, $s0, $s1 #add the vals from $s0 (1) and $s1 (2) in $t0 (3)
	add $s2, $t0, $s2 #add the vals from $t0 (3) and $s2 (3) in $s2 (6)
	move $v0, $s2 #move the val 3 from $s2(6) to $v0(6)
	
	
	jr $ra #jumps back to the adress in $r0 
