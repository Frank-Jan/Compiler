from .llvmInstructionTable import LLVMInstructionsTable
from .Register import Register, Registry
import src.llvm.LLVM as llvm

class MIPSBuilder:
    def __init__(self, llvmInstructions):
        self.llvmTable = LLVMInstructionsTable()
        self.register = Register()
        self.llvmTable.addInstructions(llvmInstructions)
        self.mipsTable = []

    def build(self):
        for instr in self.llvmTable:
            if isinstance(instr, llvm.Define):
                self.mipsTable.append(instr)
            elif isinstance(instr, llvm.Store):
                self.mipsTable.append(instr)
            elif isinstance(instr, llvm.Load):
                self.mipsTable.append(instr)
            elif isinstance(instr, llvm.Alloca):
                self.mipsTable.append(instr)
            elif isinstance(instr, llvm.endDefine):
                pass
            elif isinstance(instr, llvm.Arithmetic):
                self.mipsTable.append(instr)
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
