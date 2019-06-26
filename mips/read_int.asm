.data
part1: .asciiz "This is my "
part2: .asciiz "-th MIPS-program"
.text


main:
	li $v0, 5
	syscall
	move $t0, $v0
	
	la $a0, part1 # load adrres of part 1 into $a0
	li $v0, 4 # 4 is the print_string syscall
	syscall # do the syscall
	
	la $a0, ($t0)
	li $v0, 1
	syscall
	
	la $a0, part2 # load adrres of part2 into $a0
	li $v0, 4 # 4 is the print_string syscall
	syscall # do the syscall
	

exit:
	li $v0, 10
	syscall