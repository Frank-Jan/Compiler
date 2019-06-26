#Ooms Mathias

.data
tekst:  .asciiz "Geef de limiet in voor de getallen van Fibonnaci: " 
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
	move $s0, $v0 # saving the integer
	
	li $t1, 1 #startvalue
	
	beq $s0, $t0, exit #special case 0
	
	#printing startvalue 0
	la $a0, ($t0) #the adress of $t0 in $a0
	li $v0, 1  #print the integer in $a0
	syscall
	
	#printing spatie
	la $a0, spatie # load adress from tekst in $a0
	li $v0, 4 # print string
	syscall
	
	beq $s0, $t1, exit #special case 1
	
	#printing startvalue 1
	la $a0, ($t1) #the adress of $t1 in $a0
	li $v0, 1  #print the integer in $a0
	syscall
	
	addi $sp, $sp, -4 #stack pointer needs to move 4 bytes (1 value)
	addi $s1,$s1,1 #because the first integer is already printed
	j main1

main1:
	addi $s1,$s1, 1 #counter to stop 
	bne $s1, $s0, fibonnaci #to stop when limit is reached
	j exit
	
fibonnaci:
	
	#add the 2 values
	add $t2, $t1, $t0
	
	#printing spatie
	la $a0, spatie # load adress from tekst in $a0
	li $v0, 4 # print string
	syscall
	
	#printing sum
	la $a0, ($t2) #the adress of $t2 in $a0
	li $v0, 1  #print the integer in $a0
	syscall
	
	#pushing the sum on the stack
	sw $t2, 0($sp) #store the value of $t0 in 8 bytes "lower" than the stackpointer
	
	lw $t0, 0($sp) #to overwrite the value from the register with the value from the stack
	
	addi $s1,$s1, 1 #counter to stop 
	beq $s1, $s0, exit #to stop when limit is reached
	
	#add the 2 values
	add $t2, $t1, $t0
	
	#printing spatie
	la $a0, spatie # load adress from tekst in $a0
	li $v0, 4 # print string
	syscall
	
	#printing sum
	la $a0, ($t2) #the adress of $t2 in $a0
	li $v0, 1  #print the integer in $a0
	syscall
	
	#pushing the sum on the stack
	sw $t2, 0($sp) #store the value of $t0 in 8 bytes "lower" than the stackpointer

	#now $t1 is overwriten
	lw $t1, 0($sp) #to overwrite the value from the register with the value from the stack
	
	j main1 #recursion
	
exit:
        # to prevent memoryleaks
	addi $sp, $sp, 4 # to put the sp back on it's place
	
	li $v0, 10
	syscall
