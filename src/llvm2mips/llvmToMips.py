from .llvmInstructionTable import LLVMInstructionsTable
import src.llvm2mips.Registry as R
import src.llvm.LLVM as llvm
import src.llvm2mips.MipsInstructions as MIPS
from random import *


class MIPSBuilder:
    def __init__(self, llvmInstructions):
        self.llvmTable = LLVMInstructionsTable()
        self.registry = R.Registry()
        self.llvmTable.addInstructions(llvmInstructions)
        self.mipsTable = []
        self.mipsTable += ["text:\n# begin program:\njal main\n#end program:\nli $v0, 10\nsyscall\n"]

    def build(self):
        for instr in self.llvmTable:
            if isinstance(instr, llvm.Define):
                mips = self.defineToMips(instr)
                print(mips)
                self.mipsTable.append(mips)
            elif isinstance(instr, llvm.Store):
                # self.mipsTable.append(instr)
                continue
            elif isinstance(instr, llvm.Load):
                # self.mipsTable.append(instr)
                continue
            elif isinstance(instr, llvm.Alloca):
                # self.mipsTable.append(instr)
                continue
            elif isinstance(instr, llvm.endDefine):
                self.mipsTable.append(self.endDefineToMips(instr))
            elif isinstance(instr, llvm.Arithmetic):
                # self.mipsTable.append(instr)
                continue
            elif isinstance(instr, llvm.Call):
                self.mipsTable.append(self.callFunctionToMips(instr))
            else:
                error = "error: unknown llvm instruction in mipsBuilder: {}, line {}".format(type(instr), instr.line)
                raise Exception(error)

    def mipsToFile(self, filename):
        # open file:
        f = filename.rsplit(".", 1)
        if len(f) == 1:
            filename.append(".asm")
        elif len(f) == 2:
            if f[1] != "asm":
                error = "error: unknown file extention: {}".format(f[1])
                raise Exception(error)
        else:
            error = "error: problems splitting filename: {}".format(filename)
            raise Exception(error)

        file = open(filename, "w+")

        for instr in self.mipsTable:
            file.write(instr.__str__())

    def getVariable(self, var, instr):
        # is variable in registry:
        if var.register is not None:
            return var.register

        # variable is not in registry:
        # generate random number
        reg = randint(0,7)
        mips = ""
        # check if registry is empty:
        if not self.registry.s_isEmpty(reg):
            # registry is not empty
            toStore = self.registry[reg]
            # is variable still needed:
            needed = False
            if var.uses[-1].function is instr.function:
                  if var.uses[-1].line >= instr.line:
                      needed = True
            if needed:
                # variable still usefull:
                # check if variable already in storage:
                if var.storage is not None:
                    # store variable
                    toStore.inRegistry = False
                    mips += MIPS.storeRegisters(self.registry, [reg])
                    toStore.storage = self.registry.getSP()
        var.register = reg
        self.registry.setS(reg, var)
        return mips

    def getRegT(self):
        reg = randint(0, 7)
        pass

    # guaranteed registry
    # searches for empty S registry
    # if not found: take variable which will not be used in future
    # if not found: find variable used furthest in the future
    # store variable
    # return register
    def getSRegistry(self):
        Sreg = self.registry.getEmptyS()
        if Sreg > 0:
            # empty S registry
            return Sreg

        Sreg = self.registry.getSRegister()


    def defineToMips(self, instruction):
        # create label for function:
        mips = str(instruction.name) + ":\n"
        mips += "# store values:\n"
        # store content registers s0-s7, $fp, $ra
        mips += MIPS.storeRegisters(self.registry, [R.RAtoIndex(), R.FPtoIndex()] + R.Sindices())
        # set frame pointer to stackpointer
        mips += MIPS.M_move(R.FPtoIndex(), R.SPtoIndex())

        return mips

    def endDefineToMips(self, instruction):
        # move stackpointer back to frame pointer
        mips = "# restore values:\n"
        mips += MIPS.M_move(R.SPtoIndex(), R.FPtoIndex())
        # restore s registers:
        mips += MIPS.loadRegisters(self.registry, [R.RAtoIndex(), R.FPtoIndex()] + R.Sindices())
        # jump back
        mips += MIPS.M_jr(R.RAtoIndex())
        return mips

    def callFunctionToMips(self, instruction):
        # save $ra and temporaries:
        mips = "# save $ra and temporaries:\n"
        mips += MIPS.storeRegisters(self.registry, [R.RAtoIndex()] + R.Tindices())
        mips += "# jump and link to function:\n"
        mips += MIPS.M_jal(instruction.name)
        mips += "# restore temporaries\n"
        mips += MIPS.loadRegisters(self.registry, [R.RAtoIndex()] + R.Tindices())
        mips += "# TODO : LOAD RETURN VALUE"
        return mips

    def allocaToMips(self, instruction):
        mips = MIPS.moveSP(self.registry, 1)    # allocate 1 space
        self.llvmTable.variables[instruction.name].storage = self.registry.getSP()  # remember where the storage space is
        return mips

    def storeToMips(self, instruction):
        var = self.llvmTable.variables[instruction.name];
        storage = var.storage # offset from global pointer
        mips = ""
        return mips

    def loadToMips(self, instruction):
        mips = ""
        mips += ""
        return mips

    def addToMips(self, instruction):
        mips = ""
        return mips