#Mathias Ooms

.data
tekst:  .asciiz "Geef een integer van hoeveel integers je wilt ingeven: " 
tekst1: .asciiz "Geef een getal in: "
nl:     .asciiz "\n"
spatie: .asciiz " "
.text

main:
	la $a0, tekst # load adress from tekst in $a0
	li $v0, 4 # print string
	syscall
	
	#number of integers we'are going to store in $s0
	li $v0, 5 # reads an integer
	syscall
	move $s0, $v0 # saving the integer
	
	# adress of array in $s1 (begin position in $s2)
	sll $a0, $s0, 2 # multiplies with 4 and stores in $a0
	li $v0, 9 # the sbrk command
	syscall  # allocates memory and returns address into $v0
	move $s1, $v0 # put the adress in $v0 into $s1 
	addi $sp, $sp, -4 # to remember the start adress of the array (on the stack)
	sw $s1, ($sp) 
	
	li $t1, 0 #integer for iterating
	jal loop # the loop for storing the integers
	
	li $t1, 0 #integer for iterating (reset)
	lw $s1, ($sp) # load word the start adress
	jal print # to print the array
	
	
	lw $s1, ($sp) # load word the start adress
	addi $s0, $s0, -1 # to iterate correctly
	j sort # to sort the array
	
	
	
sort:
	li $t1, 0 #integer for iterating (reset)
	li $t2, 0 # nrOfSwaps = 0
	jal loop1
	
	lw $s1, ($sp) # putting array pointer back on the beginning
	bgtz $t2, sort # the while statement
	
	#printing out again the array
	
	la $a0, nl # load adress from tekst in $a0
	li $v0, 4 # print string
	syscall
	
	addi $s0, $s0, 1 # to iterate correctly
	li $t1, 0 #integer for iterating (reset)
	lw $s1, ($sp) # load word the start adress
	jal print # to print the array
	
	j exit
	
tussenstap:
	jr $ra #jump back to (last position in) sort 

loop1:
	beq $t1, $s0, tussenstap # when they're equal he needs to jump back
	add $t1, $t1, 1 #count 1 with the iterator 

	lw $t3, ($s1) # to load the first integer
	addi $s1, $s1, 4 # setting the pointer of the array correctly	
	lw $t4, ($s1) # to load the second integer
	
	bgt $t3, $t4, swap #jump to swap if $t3 is greater than $t4
	j loop1	

swap:
	la $t5, ($t3) # $t5 is temp place	
	la $t3, ($t4) # put second integer in place of first integer
	la $t4, ($t5) # put first integer in place of second integer 
	
	sw $t4, ($s1) #saving the integer at the right place
	sw $t3, -4($s1) #saving the integer at the right place
		
	add $t2, $t2, 1 # add 1 to the number of swaps
	j loop1
	
print:
	#prints integer
	lw $a0, ($s1) # to load the integer
	li $v0, 1 # prints an integer
	syscall
	
	addi $s1, $s1, 4 # go to the next register
	
	la $a0, spatie # load adress from tekst in $a0
	li $v0, 4 # print string
	syscall
	
	# to iterate correctly
	add $t1, $t1, 1 #count 1 with the iterator 
	blt $t1, $s0, print #as long the integer $t1 is less then the $s0 
			   #keep looping
	jr $ra #jump back to (last position in) main 
loop:

	#printing text
	la $a0, tekst1 # load adress from tekst in $a0
	li $v0, 4 # print string
	syscall
	
	#getting the integer
	li $v0, 5 # reads an integer
	syscall
	
	sw $v0, 0($s1) #saving the integer at the right place
	addi $s1, $s1, 4 # setting the pointer of the array correctly	
	
	# to iterate correctly
	add $t1, $t1, 1 #count 1 with the iterator 
	blt $t1, $s0, loop #as long the integer $t1 is less then the $s0 
			   #keep looping
	jr $ra #jump back to (last position in) main 
				   		   
exit:
        # to prevent memoryleaks
	addi $sp, $sp, 4 # to put the sp back on it's place
	
	li $v0, 10
	syscall
	
	
