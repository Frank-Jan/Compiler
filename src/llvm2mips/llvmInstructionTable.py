import src.llvm.LLVM as llvm
from .llvmObject import *

class LLVMInstructionsTable:
    def __init__(self):
        self.instructions = []
        self.line = 0
        self.variables = dict()     # name, llvmVar
        self.functions = dict()     # name, llvmFunc

    def addInstructions(self, instructions):

        for instr in instructions:
            instr.line = self.line
            self.line += 1
            self.instructions.append(instr)
            if isinstance(instr, llvm.Define):
                # add arguments:
                for arg in instr.args:
                    self.variables[arg.name] = LLVMVariable(arg.getName(), arg.getType(), instr)
                self.addInstructions(instr.stats)

                endDefine = llvm.endDefine(instr)
                endDefine.line = self.line
                self.line += 1
                self.instructions.append(endDefine)

            elif isinstance(instr, llvm.Alloca):
                # add variable
                self.variables[instr.result] = LLVMVariable(instr.result, instr.type, instr)

            elif isinstance(instr, llvm.Store):
                # add instruction to llvmVar
                var = LLVMVariable(instr._to, instr.type, instr)
                try:
                    self.variables[instr._to] = var
                    self.variables[instr._from].addInstruction(instr)
                except Exception as e:
                    print("llvm instructions:")
                    for i in self.instructions:
                        print(i.line, "\t", i)
                    print("from:    ", instr._from)
                    print("to:      ", instr._to)
                    raise e

            elif isinstance(instr, llvm.Load):
                # add instruction to llvmVar
                self.variables[instr.var].addInstruction(instr)

                var = LLVMVariable(instr.result, instr._type, instr)
                self.variables[var.getName()] = var

            elif isinstance(instr, llvm.Arithmetic):
                self.variables[instr.val1].addInstruction(instr)
                self.variables[instr.val1].addInstruction(instr)

                var = LLVMVariable(instr.result, instr._type, instr)
                self.variables[var.getName()] = var
            else:
                error = "error: unknown llvm instruction: {} line: {}".format(type(instr), self.line)
                raise Exception(error)

    def __iter__(self):
        return self.instructions.__iter__()

