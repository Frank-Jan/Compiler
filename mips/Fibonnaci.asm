#Ooms Mathias


.data
tekst:  .asciiz "Geef de limiet in voor de getallen van Fibonnaci (nul mag niet): " 
nl:     .asciiz "\n"
spatie: .asciiz " "
.text

main:
	#printing some text
	la $a0, tekst # load adress from tekst in $a0
	li $v0, 4 # print string
	syscall
	
	#to give in an integer
	li $v0, 5 # reads an integer
	syscall
	move $t0, $v0 # saving the integer
	
	#startvalues for fibonnaci
	li $t1, 0 
	li $t2, 1 
	
	move $a0, $t0 # Put procedure arguments (number of numbers)
	move $a1, $t1 # Put procedure arguments (first number)
	move $a2, $t2 # Put procedure arguments (second number)
		
	jal fibonnaci #fibonnaci function
	
	j exit
	
fibonnaci:
	#from frame-example.asm (http://msdl.cs.mcgill.ca/people/hv/teaching/ComputerSystemsArchitecture/)
	
	sw $fp, 0($sp)	# push old frame pointer (dynamic link)
	move $fp, $sp	# frame	pointer now points to the top of the stack
	subu $sp, $sp, 20 # allocate 24 bytes on the stack
	sw $ra, -4($fp)	# store the value of the return address
	# save locally used registers
	sw $s0, -8($fp)	# for number of numbers
	sw $s1, -12($fp) # first integer
	sw $s2, -16($fp) # second integer

	move $s0, $a0 # $s0 = number of integers 	
	move $s1, $a1 # $s1 = first number to be added
	move $s2, $a2 # $s2 = second number to be added
	
	beq $t4, 0, special # $t4 serves as boolean
	
#calculating fibonnaci
#------------------------------------------------------------------------------	
	
	add $t3, $s1, $s2  # $t3 is the next number
	move $s1, $s2  # the first number becomes the second one
	move $s2, $t3  # the second number becomes the next number
	
	#printing number
	la $a0, ($s2) #the adress of $s2 in $a0
	li $v0, 1  #print the integer in $a0
	syscall
	
	#printing spatie
	la $a0, spatie # load adress from tekst in $a0
	li $v0, 4 # print string
	syscall

	addi $s0, $s0, -1 # 1 integer is printed, so now substract

#------------------------------------------------------------------------------	

	#looking if we need to do fibonacci all over again
	bnez $s0, prep_fib #jump to function for preparing another fibonnaci call

	lw $s2, -16($fp) # reset saved register $s2
	lw $s1, -12($fp) # reset saved register $s1
	lw $s0, -8($fp)	# reset saved register $s0
	lw $ra, -4($fp) # get return address from frame
	move $sp, $fp # get old frame pointer from current frame
	lw $fp, ($sp) # restore old frame pointer
	jr $ra

special:
# printing the first 1/2 integers and stop when neccessary 	

	#printing startvalue 0
	la $a0, ($s1) #the adress of $t0 in $a0
	li $v0, 1  #print the integer in $a0
	syscall
	
	#printing spatie
	la $a0, spatie # load adress from tekst in $a0
	li $v0, 4 # print string
	syscall
	
	addi $s0, $s0, -1 # 1 integer is printed, so now substract
	beqz $s0, exit # when $s0 is zero exit
		
	#printing startvalue 1
	la $a0, ($s2) #the adress of $t0 in $a0
	li $v0, 1  #print the integer in $a0
	syscall
	
	#printing spatie
	la $a0, spatie # load adress from tekst in $a0
	li $v0, 4 # print string
	syscall
	
	addi $s0, $s0, -1 # 1 integer is printed, so now substract
	beqz $s0, exit # when $s0 is zero exit
	
	li $t4, 1 #changing boolean
	
	#has to do the following code below, so there is no jump here
	
prep_fib:
	# putting all arguments right for next function call
	move $a0, $s0
	move $a1, $s1
	move $a2, $s2
	
	jal fibonnaci
	j exit
	
exit:
	li $v0, 10
	syscall
