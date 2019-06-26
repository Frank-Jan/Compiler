#Ooms Mathias

.data
tekst:  .asciiz "Geef het eerste getal: " 
tekst2:  .asciiz "Geef het tweede getal: " 
nl:     .asciiz "\n"
spatie: .asciiz " "
.text

main:
#asking for information:
#------------------------------------------------------------------
	#printing some text
	la $a0, tekst # load adress from tekst in $a0
	li $v0, 4 # print string
	syscall
	
	#to give in an integer
	li $v0, 5 # reads an integer
	syscall
	move $t0, $v0 # saving the integer
	
	#printing some text
	la $a0, tekst2 # load adress from tekst in $a0
	li $v0, 4 # print string
	syscall
	
	#to give in an integer
	li $v0, 5 # reads an integer
	syscall
	move $t1, $v0 # saving the integer
	
#------------------------------------------------------------------

	bgt $t0, $t1, pre_gcd # to jump over the switch integers
	#switching integers
	move $t8, $t0
	move $t0, $t1
	move $t1, $t8
	
pre_gcd:
	move $a0, $t0 # Put procedure arguments
	move $a1, $t1 # Put procedure arguments
	
	jal gcd # Call procedure
	
	move $t5, $v0 # Get procedure result
	
	#printing returnvalue
	la $a0, ($t5) #the adress of $t5 in $a0
	li $v0, 1  #print the integer in $a0
	syscall
	
	j exit	
	
gcd:
	sw $fp, 0($sp)	# push old frame pointer (dynamic link)
	move $fp, $sp	# frame	pointer now points to the top of the stack
	subu $sp, $sp, 16 # allocate 20 bytes on the stack
	sw $ra, -4($fp)	# store the value of the return address
	# save locally used registers
	sw $s0, -8($fp)	# first integer
	sw $s1, -12($fp) # second integer
	
	move $s0, $a0 # $s0 = first number to be added	
	move $s1, $a1 # $s1 = second number to be added
	
	beqz $s1, special # second number equals to zero
	
	jal remainder
	move $a1, $v0 # Get procedure result
	move $a0, $s1 # greatest number putting on the first place
	
	jal gcd

	lw $s1, -12($fp) # reset saved register $s1
	lw $s0, -8($fp)	# reset saved register $s0
	lw $ra, -4($fp) # get return address from frame
	move $sp, $fp # get old frame pointer from current frame
	lw $fp, ($sp) # restore old frame pointer
	jr $ra
	
special:
	move $v0, $s0 # place result in return value location

	jr $ra

remainder:
	#from frame-example.asm (http://msdl.cs.mcgill.ca/people/hv/teaching/ComputerSystemsArchitecture/)
	
	sw $fp, 0($sp)	# push old frame pointer (dynamic link)
	move $fp, $sp	# frame	pointer now points to the top of the stack
	subu $sp, $sp, 16 # allocate 20 bytes on the stack
	sw $ra, -4($fp)	# store the value of the return address
	# save locally used registers
	sw $s0, -8($fp)	# first integer
	sw $s1, -12($fp) # second integer

	move $s0, $a0 # $s0 = first number to be added	
	move $s1, $a1 # $s1 = second number to be added
	
	rem $t3, $s0, $s1 # calculating remainder
	
	move $v0, $t3 # place result in return value location

	lw	$s0, -8($fp)	# reset saved register $s0
	lw	$ra, -4($fp)    # get return address from frame
	move	$sp, $fp        # get old frame pointer from current fra
	lw	$fp, ($sp)	# restore old frame pointer
	jr	$ra

exit:
	li $v0, 10
	syscall