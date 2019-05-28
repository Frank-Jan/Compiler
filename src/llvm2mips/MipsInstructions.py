from .Registry import *

def storeRegister(register):
    # move stack pointer

    mips = "sw"
    return mips


def stackPointerNext():
    mips = ""
    pass


def base3input(r1, r2, result):
    return  indexToStr(result) + ", " + indexToStr(r1) + ", " + indexToStr(r2) + "\n"


def base2immInput(r1, imm, result):
    return indexToStr(result) + ", " + indexToStr(r1) + ", " + imm + "\n"


def M_add(r1, r2, result):
    mips = "add " +  base3input(r1,r2,result)
    return mips


def M_addi(r1, imm, result):
    mips = "addi " + base2immInput(r1,imm,result)
    return mips


def M_addiu(r1, imm, result):
    mips = "addiu " + base2immInput(r1,imm,result)
    return mips


def M_addu(r1, r2, result):
    mips = "addu " +  base3input(r1,r2,result)
    return mips


def M_and(r1, r2, result):
    mips = "and " +  base3input(r1,r2,result)
    return mips


def M_andi(r1, imm, result):
    mips = "andi " + base2immInput(r1,imm,result) + "\n"
    return mips

def M_beq(r1, r2, offset):
    mips = "beq " + indexToStr(r1) + ", " + indexToStr(r2) + ", " + offset + "\n"
    return mips

def M_bgez(r1, offset):
    mips = "bgez " + indexToStr(r1) + ", " + offset + "\n"
    return mips

def M_bgezal(r1, offset):
    mips = "bgezal " + indexToStr(r1) + ", " + offset + "\n"
    return mips

def M_bgtz(r1, offset):
    mips = "bgtz " + indexToStr(r1) + ", " + offset + "\n"
    return mips

def M_blez(r1, offset):
    mips = "blez " + indexToStr(r1) + ", " + offset + "\n"
    return mips

def M_bltz(r1, offset):
    mips = "bltz " + indexToStr(r1) + ", " + offset + "\n"
    return mips

def M_bltzal(r1, offset):
    mips = "bltzal " + indexToStr(r1) + ", " + offset + "\n"
    return mips

def M_bne(r1, offset):
    mips = "bne " + indexToStr(r1) + ", " + offset  + "\n"
    return mips

def M_div_i(nom, div, result):
    mips = "div " + base3input(nom, div, result)
    return mips

def M_div_f(nom, div, result):
    mips = "div.d " + base3input(nom, div, result)
    return mips

# target is immediate address
def M_jump(target):
    mips = "j " + target + "\n"
    return mips

# target is immediate address
def M_jal(target):
    mips = "jal " + target + "\n"
    return mips

# jump register
def M_jr(r):
    mips = "jr " +  indexToStr(r) + "\n"
    return mips

# load upper immediate in register r
def M_liu(r, imm):
    mips = "lui " + indexToStr(r) + "\n"
    return mips

# load word
def M_lw(r, result, offset):
    mips = "lw " + indexToStr(result) + ", " + offset + "(" + indexToStr(r) + ")\n"
    return mips

def M_mult(r1, r2, result):
    mips = "mult " + base3input(r1,r1,result)
    return mips

def M_or(r1, r2, result):
    mips = "or " + base3input(r1,r2, result)
    return mips

def M_ori(r1, result, imm):
    mips = "ori " + indexToStr(result) + ", " + indexToStr(r1) + ", " + imm + "\n"
    return mips

def M_sub(r1, r2, result):
    mips = "sub " + indexToStr(result) + ", " + indexToStr(r1) + ", " + indexToStr(r2) + "\n"
    return mips

# saves r1 to r2+offset
def M_sw(r1, r2, offset):
    mips = "sw " + indexToStr(r1) + ", " + offset + "(" + indexToStr(r2) + ")\n"
    return mips

def M_syscall():
    mips = "syscall\n"
    return mips