.text
# Begin program
# SET GLOBAL VARIABLES:
jal main
# End program
li $v0, 10
syscall

# FUNCTION DEFINITIONS:
main:# store registries:
addi $sp, $sp, -40
sw $ra, 0($sp)
sw $fp, 4($sp)
sw $s0, 8($sp)
sw $s1, 12($sp)
sw $s2, 16($sp)
sw $s3, 20($sp)
sw $s4, 24($sp)
sw $s5, 28($sp)
sw $s6, 32($sp)
sw $s7, 36($sp)
move $fp, $sp
# Alloca
addi $sp, $sp, -4
move $s6, $sp
# Store
addi $t4, $zero, 0
sw $t4, 0($s6)
# Alloca
addi $sp, $sp, -4
move $s0, $sp
# Store
addi $t4, $zero, 0
sw $t4, 0($s0)
# Alloca
addi $sp, $sp, -4
move $s2, $sp
# Store
addi $t3, $zero, 0.0
sw $t3, 0($s2)
# Alloca
addi $sp, $sp, -4
move $s6, $sp
# Alloca
addi $sp, $sp, -4
move $s2, $sp
# Alloca
addi $sp, $sp, -4
move $s2, $sp
# Alloca
addi $sp, $sp, -4
move $s6, $sp
# Alloca
addi $sp, $sp, -4
move $s2, $sp
# Alloca
addi $sp, $sp, -4
move $s6, $sp
# Alloca
addi $sp, $sp, -4
move $s5, $sp
# Store
addi $t6, $zero, 123
sw $t6, 0($s5)
# Alloca
addi $sp, $sp, -4
move $s5, $sp
# Store
addi $t6, $zero, 83
sw $t6, 0($s5)
# Alloca
addi $sp, $sp, -4
move $s4, $sp
# Store
addi $t5, $zero, 0x4012449ba0000000
sw $t5, 0($s4)
# Alloca
addi $sp, $sp, -4
move $s7, $sp
# Store
sw $s5, 0($s7)
# Alloca
addi $sp, $sp, -4
move $s5, $sp
# Store
sw $s5, 0($s5)
# Alloca
addi $sp, $sp, -4
move $s2, $sp
# Store
sw $s4, 0($s2)
# Alloca
addi $sp, $sp, -4
move $s5, $sp
# Store
sw $s7, 0($s5)
# Alloca
addi $sp, $sp, -4
move $s3, $sp
# Store
sw $s5, 0($s3)
# Alloca
addi $sp, $sp, -4
move $s4, $sp
# Store
sw $s2, 0($s4)
# restore s register
move $sp, $fp
# load registries:
lw $ra, 0($sp)
lw $fp, 4($sp)
lw $s0, 8($sp)
lw $s1, 12($sp)
lw $s2, 16($sp)
lw $s3, 20($sp)
lw $s4, 24($sp)
lw $s5, 28($sp)
lw $s6, 32($sp)
lw $s7, 36($sp)
addi $sp, $sp, 40
# jump back
jr $ra
