from .llvmInstructionTable import LLVMInstructionsTable
import src.llvm2mips.Registry as R
import src.llvm.LLVM as llvm
import src.llvm2mips.MipsInstructions as MIPS

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


    def defineToMips(self, instruction):
        # create label for function:
        mips = str(instruction.name) + ":\n"
        mips += "# store values:\n"
        # store content registers s0-s7, $fp, $ra
        mips += MIPS.storeRegisters(self.registry, [R.raIndex(), R.fpIndex()] + R.getSindices())
        # set frame pointer to stackpointer
        mips += MIPS.M_move(R.fpIndex(), R.spIndex())

        return mips

    def endDefineToMips(self, instruction):
        # move stackpointer back to frame pointer
        mips = "# restore values:\n"
        mips += MIPS.M_move(R.spIndex(), R.fpIndex())
        # restore s registers:
        mips += MIPS.loadRegisters(self.registry, [R.raIndex(), R.fpIndex()] + R.getSindices())
        # jump back
        mips += MIPS.M_jr(R.raIndex())
        return mips

    def callFunctionToMips(self, instruction):
        # save $ra and temporaries:
        mips = "# save $ra and temporaries:\n"
        mips += MIPS.storeRegisters(self.registry, [R.raIndex()] + R.getTindices())
        mips += "# jump and link to function:\n"
        mips += MIPS.M_jal(instruction.name)
        mips += "# restore temporaries\n"
        mips += MIPS.loadRegisters(self.registry, [R.raIndex()] + R.getTindices())
        mips += "# TODO : LOAD RETURN VALUE"
        return mips

    def allocaToMips(self, instruction):
        mips = ""
        return mips

    def storeToMips(self, instruction):
        mips = ""
        return mips
