
class LLVMObject:
    def __init__(self, name, _type):
        self.name = name            # name or label of the object
        self._type = _type

    def getName(self):
        return self.name

    def getType(self):
        return self._type


class LLVMFunction(LLVMObject):
    def __init__(self, name, _type):
        LLVMObject.__init__(self, name, _type)

    def isVariable(self):
        return False


class LLVMVariable(LLVMObject):
    def __init__(self, name, _type, instruction):
        LLVMObject.__init__(self, name, _type)
        self.storage = None         # Places from frame pointer
        self.register = None
        self.uses = [instruction]   # The llvm instructions where it is used


    def addInstruction(self, instruction):
        self.uses.append(instruction)

    def lastUse(self):
        return self.uses[-1].line

    def isVariable(self):
        return True
