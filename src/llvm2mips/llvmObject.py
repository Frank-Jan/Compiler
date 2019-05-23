

class LLVMVariable:
    def __init__(self, name):
        self.name = name
        self.uses = []

    def addInstruction(self, instruction):
        self.uses.append(instruction)

    # def lastUse(self):
        # return self.uses[-1].line