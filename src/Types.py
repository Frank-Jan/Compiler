from src.errors import printError

llvmTypes = {'int': 'i32',
             'float': 'float',
             'char': 'i8',
             'void': 'void'}

opTypes = {'==': 'eq',
             '>': 'sgt',
             '<': 'slt'}

printTypes = {'int': '@str-i',
             'float': '@str-f',
             'char': '@str-c'}

def toType(string):
    if string == "void":
        return VOID()
    if string == "char":
        return CHAR()
    if string == "int":
        return INT()
    if string == "float":
        return FLOAT()
    if string == "*":
        return POINTER
    if string == "&":
        return REFERENCE
    # printError("Unknown type: default to void")
    return None


class VOID:
    def getType(self):
        return 0

    def getAlign(self):
        return ""

    def __str__(self):
        return "void"

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def toLLVM(self):
        print("VOID to LLVM")
        return llvmTypes[str(self)]


class CHAR(VOID):
    def getType(self):
        return 1

    def getAlign(self):
        return ", align 1"

    def __str__(self):
        return "char"

    def toLLVM(self):
        print("CHAR to LLVM")
        return llvmTypes[str(self)]


class INT(VOID):
    def getType(self):
        return 2

    def getAlign(self):
        return ", align 4"

    def __str__(self):
        return "int"

    def toLLVM(self):
        print("INT to LLVM")
        return llvmTypes[str(self)]


class FLOAT(VOID):
    def getType(self):
        return 3

    def getAlign(self):
        return ", align 4"

    def __str__(self):
        return "float"

    def toLLVM(self):
        print("FLOAT to LLVM")
        return llvmTypes[str(self)]


class POINTER(VOID):
    def __init__(self, type=VOID()):
        self.type = type

    def getType(self):
        return self.__str__()

    def getAlign(self):
        return ", align 8"

    def getBase(self):
        return self.type

    def __str__(self):
        return self.type.__str__() + "*"

    def toLLVM(self):
        print("POINTER to LLVM")
        return llvmTypes[str(self.type)] + "*"


class REFERENCE(VOID):
    def __init__(self, type=VOID()):
        self.type = type

    def getType(self):
        return self.__str__()

    def getAlign(self):
        return ", align 8"

    def getBase(self):
        return self.type

    def toLLVM(self):
        print("REFERENCE to LLVM")
        return llvmTypes[str(self.type)] + "*"

    def __str__(self):
        return self.type.__str__() + "&"
