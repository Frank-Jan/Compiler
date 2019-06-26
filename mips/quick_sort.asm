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
	move $a0, $s1 # int arr[] (adres of array)
	li $a1, 0 # int left
	subi $t0, $s0, 1 #subtract 1 to iterate correctly
	move $a2, $t0 # int right
	
	addi $sp, $sp, -4 # to remember the startadress of the array
	jal quickSort
	
	#printing some newline
	la $a0, nl # load adress from tekst in $a0
	li $v0, 4 # print string
	syscall
	
	li $t1, 0 #integer for iterating (reset)
	lw $s1, 4($sp) # load word the start adress
	jal print # to print the array
	
	j exit

#quicksort:
#-----------------------------------------------------------------------------
quickSort:
	#from frame-example.asm (http://msdl.cs.mcgill.ca/people/hv/teaching/ComputerSystemsArchitecture/)
	
	sw $fp, 0($sp)	# push old frame pointer (dynamic link)
	move $fp, $sp	# frame	pointer now points to the top of the stack
	subu $sp, $sp, 28 # allocate 32 bytes on the stack
	sw $ra, -4($fp)	# store the value of the return address
	# save locally used registers
	sw $s0, -8($fp)	# for the address of the array
	sw $s1, -12($fp) # integer left
	sw $s2, -16($fp) # integer right
	sw $s3, -20($fp) # i
	sw $s3, -24($fp) # j

	move $s0, $a0 # $s0 = the address of the array
	move $s1, $a1 # $s1 = integer left
	move $s2, $a2 # $s2 = integer right
	move $s3, $a1 # $s3 = i
	move $s4, $a2 # $s4 = j
	
	#calculation for pivot index
	add $t8, $s1, $s2 
	srl $t8, $t8, 1
	# to get the pivot out of array
	mul $t8, $t8, 4 
	add $t8, $s0, $t8 # to get the adress of the number
	lw $t8, ($t8) # to get the number on the adress
while:	
	bgt $s3, $s4, if1 # opposite comparison to put while loop in quicksort
while1:
	# to get the number on the place of the index
	mul $t7, $s3, 4
	add $t7, $s0, $t7  # to get the adress of the number
	lw $t4, ($t7)  # to get the number on the adress
	bge $t4, $t8, while2  # opposite comparison to put while loop in quicksort
	addi $s3, $s3, 1 # i++
	j while1
while2:
	# to get the number on the place of the index
	mul $t6, $s4, 4
	add $t6, $s0, $t6  # to get the adress of the number
	lw $t5, ($t6)  # to get the number on the adress
	ble $t5, $t8, if  # opposite comparison to put while loop in quicksort
	subi $s4, $s4, 1 # j--
	j while2
if:
	bgt $s3, $s4, while # opposite comparison to put while loop in quicksort
	
	#setting the number of the array at index i,
	# to the number of the array at index j
	sw $t5, ($t7) # arr[i] = arr[j]
	
	#setting the number of the array at index j,
	# to the number of the array at index i
	sw $t4, ($t6) # arr[j] = arr[i]
	
	addi $s3, $s3, 1 # i++
	subi $s4, $s4, 1 # j--
	j while
if1:
	bge $s1, $s4, if2
	# setting arguments right for next function call
	move $a0, $s0  
	move $a1, $s1
	move $a2, $s4
	jal quickSort
if2:
	bge $s3, $s2, continue
	# setting arguments right for next function call
	move $a0, $s0  
	move $a1, $s3
	move $a2, $s2
	jal quickSort		

continue:
	lw $s4, -24($fp)  # reset saved register $s4
	lw $s3, -20($fp)  # reset saved register $s3
	lw $s2, -16($fp)  # reset saved register $s2
	lw $s1, -12($fp) # reset saved register $s1
	lw $s0, -8($fp)  # reset saved register $s0
	lw $ra, -4($fp)  # get return address from frame
	move $sp, $fp # get old frame pointer from current fra
	lw $fp, ($sp)  # restore old frame pointer
	jr $ra
#-----------------------------------------------------------------------------
	
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

#bubblesort:
#-----------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------
				   		   
exit:
        # to prevent memoryleaks
	addi $sp, $sp, 4 # to put the sp back on it's place
	
	li $v0, 10
	syscall

	
	
