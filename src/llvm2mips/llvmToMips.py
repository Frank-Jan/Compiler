# from .llvmInstructionTable import LLVMInstructionsTable
import src.llvm2mips.Registry as R
import src.llvm.LLVM as llvm
import src.llvm2mips.MipsInstructions as MIPS
import src.llvm2mips.SymbolTable as ST
from random import *


class MIPSBuilder:
    def __init__(self, llvmInstructions, symbolTable, registry):
        self.registry = registry
        self.llvmTable = llvmInstructions
        self.symbolTable = symbolTable
        self.todo = []

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

class MipsTable:
    def __init__(self):
        self.mips = []

    def addComment(self, comment):
        self.mips.append("# " + comment)

    def addInstruction(self, instruction):
        self.mips.append(instruction)

    def addTable(self):
        table = MipsTable()
        self.mips.append(table)
        return table

    def toString(self, depth=0):
        string = ""
        i = 0
        tabs = ""
        while i < depth:
            tabs += "\t"
            i += 1

        for m in self.mips:
            if isinstance(m, MipsTable):
                string += "\n"
                string += m.toString(depth+1)
            else:
                string += tabs + str(m) + "\n"
        return string


class GlobalBuilder:

    def __init__(self, llvmInstructions):
        self.llvmInstructions = llvmInstructions
        self.symbolTable = ST.SymbolTable()
        self.registry = R.Registry()
        # self.llvmTable.addInstructions(llvmInstructions)
        self.functionTable = []     # defined functions
        self.variableTable = []     # globally defined/declared variables
        # self.mipsTable += ["text:\n# begin program:\njal main\n#end program:\nli $v0, 10\nsyscall\n"]
        self.mips = []
        self.readLLVM()

    def readLLVM(self):
        for instr in self.llvmInstructions:
            if isinstance(instr, llvm.Define):
                self.buildDefine(instr)

    def build(self):
        self.mips.append(".text\n")
        self.mips.append("# Begin program\n")

        self.globalsToMips()

        self.mips.append("jal main\n")
        self.mips.append("# End program\n")
        self.mips.append("li $v0, 10\n")
        self.mips.append("syscall\n")
        self.mips.append("\n")

        self.functionsToMips()


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

        # self.toMips()
        # string = ""
        for s in self.mips:
            file.write(s)

    # def toMips(self):
    #     self.mips.addInstruction(".text")
    #     self.mips.addComment("Begin program")
    #     # self.globalsToMips()
    #
    #     self.mips.addInstruction("jal main")
    #     self.mips.addComment("End program")
    #     self.mips.addInstruction("li $v0, 10")
    #     self.mips.addInstruction("syscall")
    #     self.mips.addInstruction("\n")
    #
    #     self.functionsToMips()

    def functionsToMips(self):
        self.mips.append("# FUNCTION DEFINITIONS:\n")
        for function in self.functionTable:
            function.build()
            self.mips += function.mips

    def globalsToMips(self):
        self.mips.append("# SET GLOBAL VARIABLES:\n")

    def buildDefine(self, define):
        # build define builder
        function = DefineBuilder(define, self.symbolTable, self.registry)
        self.functionTable.append(function)

    # def getVariable(self, var, instr):
    #     # is variable in registry:
    #     if var.register is not None:
    #         return var.register
    #
    #     # variable is not in registry:
    #     # generate random number
    #     reg = randint(0, 7)
    #     mips = ""
    #     # check if registry is empty:
    #     if not self.registry.s_isEmpty(reg):
    #         # registry is not empty
    #         toStore = self.registry[reg]
    #         # is variable still needed:
    #         needed = False
    #         if var.uses[-1].function is instr.function:
    #               if var.uses[-1].line >= instr.line:
    #                   needed = True
    #         if needed:
    #             # variable still usefull:
    #             # check if variable already in storage:
    #             if var.storage is not None:
    #                 # store variable
    #                 toStore.inRegistry = False
    #                 mips += MIPS.storeRegisters(self.registry, [reg])
    #                 toStore.storage = self.registry.getSP()
    #     var.register = reg
    #     self.registry.setS(reg, var)
    #     return mips

    # def getRegT(self):
    #     reg = randint(0, 7)
    #     pass

    # # guaranteed registry
    # # searches for empty S registry
    # # if not found: take variable which will not be used in future
    # # if not found: find variable used furthest in the future
    # # store variable
    # # return register
    # def getSRegistry(self):
    #     Sreg = self.registry.getEmptyS()
    #     if Sreg > 0:
    #         # empty S registry
    #         return Sreg
    #
    #     Sreg = self.registry.getSRegister()


        # for llvm_instr in self.llvmInstructions:
        #     if isinstance(llvm_instr, )
        #         self.instructions.append()


class DefineBuilder:

    def __init__(self, define, symbolTable, registry):
        self.label = define.name
        self.llvmInstructions = define.stats
        self.arguments = define.args
        self.type = define.type
        self.returnVars = []
        self.symbolTable = ST.SymbolTable(symbolTable)
        self.mips = []
        self.registry = registry
        self.readLLVM()

    def readLLVM(self):
        for arg in self.arguments:
            var = self.symbolTable.create(arg.ogName, arg.tempName)

        for instr in self.llvmInstructions:
            if isinstance(instr, llvm.Alloca):
                self.symbolTable.create(str(instr.result), instr.type)
            if isinstance(instr, llvm.Load):
                self.symbolTable.create(str(instr.result), instr.type)

    def build(self):
        # building function:
        # add arguments to instructions
        self.begin()
        for llvm_instr in self.llvmInstructions:
            l = llvm_instr.toMips(self)
            if l is not None:
                self.mips += l
        self.end()

    def createVariable(self, varname, line):
        mips = []

    def GetSavedRegister(self, varname, line):
        mips = []
        # get new register:
        rng = randint(0,7)
        if not self.registry.s_isEmpty(rng):
            store = self.registry.getS(rng)
            store.register = None
            if store.useful(line):
                # store:
                mips += MIPS.moveSP(self.registry, 1)   #store value
                store.storage = self.registry.getSP()
        rng = R.StoIndex(rng)
        var = self.symbolTable.get(varname, None)
        if var is None:
            print("Error: unknown varname: {}".varname)
        var.register = rng
        return rng, mips

    def GetVariable(self, varname, line):
        mips = []
        var = self.symbolTable.get(varname, None)
        if var is None:
            print("Error: unknown varname: {}".varname)
        if var.register is not None:
            return var.register, []

        if var.storage is not None:
            rng, temp = self.GetSavedRegister(line)
            mips += temp
            self.registry.setS(rng, var)
            Tregister = self.GetTemporaryRegister()
            mips += MIPS.M_addi(0, var.storage, Tregister)
            mips += MIPS.M_lw(rng, Tregister, 0)
            var.register = R.StoIndex(rng)
            return var, mips

        raise Exception("ERROR: GET VARIABLE NOT IN REGISTER AND STORAGE")

    def GetTemporaryRegister(self):
        rng = randint(0,7)
        return R.TtoIndex(rng)

    def toMips(self):
        return self.mips

    def begin(self):
        self.mips = [str(self.label) + ":"]
        store = MIPS.storeRegisters(self.registry, [R.RAtoIndex(), R.FPtoIndex()] + R.Sindices())
        # for s in store:
        self.mips += store
        self.mips += MIPS.M_move(R.FPtoIndex(), R.SPtoIndex())

    def end(self):
        self.mips.append("# restore s register\n")
        self.mips += MIPS.M_move(R.SPtoIndex(), R.FPtoIndex())
        load = MIPS.loadRegisters(self.registry, [R.RAtoIndex(), R.FPtoIndex()] + R.Sindices())
        self.mips += load
        self.mips.append("# jump back\n")
        self.mips += MIPS.M_jr(R.RAtoIndex())
        # self.mips += []


