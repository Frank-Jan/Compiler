# Ooms Mathias

.text

main:
	# loading the values 
	li $t1, 12
	li $t2, 66
	li $t3, 48
	li $t4, 97
	
	# pushing 12 and 66 on the stack
	addi $sp, $sp, -8 #stack pointer needs to move 8 bytes (2 values)
	sw $t1, 4($sp) #store the value of $t1 in 4 bytes "lower" than the stackpointer
	sw $t2, 0($sp) #store the value of $t2 on the place where the stackpointer "points"
	
	#pop the stackpointer 4 bytes lower, the previous value is unreachable
	addi $sp, $sp, 4
	
	#pushing 48 on the stack
	addi $sp, $sp, -4 #stack pointer needs to move 4 bytes (1 value)	       
	sw $t3, 0($sp) #store the value of $t3 on the place where the stackpointer "points"
	
	#pop the stackpointer 4 bytes lower, the previous value is unreachable
	addi $sp, $sp, 4
	
	#pushing 97 on the stack
	addi $sp, $sp, -4 #stack pointer needs to move 4 bytes (1 value)	       
	sw $t4, 0($sp) #store the value of $t4 on the place where the stackpointer "points"
	
	#pop the stackpointer 8 bytes lower, the previous 2 values are unreachable
	addi $sp, $sp, 8
	
	#jump to exit
	j exit

exit:
	li   $v0, 10 		# system call for exit
	syscall      		# exit (back to operating system)
	
