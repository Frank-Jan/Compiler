#Ooms Mathias

.data
nl: .asciiz "\n"
spatie: .asciiz " "
.text

main:
	li $v0, 5 # reads an integer
	syscall
	move $t0, $v0  # move input $v0 naar $t0
	
	li $t1, 0  # put 0 in $t1
	j for_loop1
	
for_loop1:
	li $t2, 1 # put 1 in $t2
	add $t1, $t1, 1 # adds 1 to itself, !!!sequence!!!
	
	la $a0, nl # load adress from nl in $a0
	li $v0, 4 # print string
	syscall      # works only with $v0 #
	
	ble $t1, $t0, for_loop2 #exit when $t0 == 10
	
	bgt $t1, $t0, exit #exit when $t0 == $t0
	
for_loop2:
		

	la $a0, ($t2) #the adress of $t0 in $a0
	li $v0, 1  #print the integer in $a0
	syscall
	
	la $a0, spatie # load adress from spatie in $a0
	li $v0, 4 # print string
	syscall      # works only with $v0 
	
	add $t2, $t2, 1  # add 1 to itself
	bgt $t2, $t1, for_loop1 #whenever $t2 is bigger than $t1 jump back to for_loop1
	ble $t2, $t1, for_loop2 # as long the $t2 isn't bigger as $t1 do this again (jump for_loop2)
	

exit:
	li $v0, 10
	syscall
