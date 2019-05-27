from src.errors import printError

llvmTypes = {'int': 'i32',
             'float': 'float',
             'char': 'i8',
             'void': 'void'}

pythonStrings = {'n': '\n',
             'r': '\r',
             't': '\t',
             'f': '\f',
             'b': '\b'}

llvmStrings = {'\n': '\\0A',
             '\r': '\\0D',
             '\t': '\\09',
             '\f': '\\0C',
             '\b': '\\08',
             '\\': '\\5C',
             '': 'zeroinitializer'}

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

    def getDepth(self):
        return 0

    def getBase(self):
        return self

    def __str__(self):
        return "void"

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def printLLVM(self):
        return 'void'

    def toLLVM(self):
        return 'void'


class CHAR(VOID):
    def getType(self):
        return 1

    def getAlign(self):
        return "1"

    def __str__(self):
        return "char"

    def printLLVM(self):
        return 'i8'

    def toLLVM(self):
        return 'i8'


class INT(VOID):
    def getType(self):
        return 2

    def getAlign(self):
        return "4"

    def __str__(self):
        return "int"

    def printLLVM(self):
        return 'i32'

    def toLLVM(self):
        return 'i32'


class FLOAT(VOID):
    def getType(self):
        return 3

    def getAlign(self):
        return "4"

    def __str__(self):
        return "float"

    def printLLVM(self):
        return 'float'

    def toLLVM(self):
        return 'float'


class POINTER(VOID):
    def __init__(self, type=VOID()):
        self.type = type

    def getType(self):
        return self.__str__()

    def getAlign(self):
        return "8"

    def getDepth(self):
        return self.type.getDepth() + 1

    def getBase(self): # get dereference
        return self.type

    def __str__(self):
        return self.type.__str__() + "*"

    def printLLVM(self):
        return self.getBase().printLLVM() + "*"

    def toLLVM(self):
        return self.getBase().printLLVM() + "*"


class REFERENCE(VOID):
    def __init__(self, type=VOID()):
        self.type = type

    def getType(self):
        return self.__str__()

    def getAlign(self):
        return "8"

    def getBase(self):
        return self.type

    def printLLVM(self):
        return self.type.printLLVM() + "*"

    def toLLVM(self):
        return self.type.printLLVM() + "*"

    def __str__(self):
        return "&" + self.type.__str__()


class ARRAY(POINTER):
    def __init__(self, type=VOID()):
        POINTER.__init__(self, type)

    def printLLVM(self):
        return self.getBase().printLLVM() + "*"

    def toLLVM(self):
        return self.getBase().printLLVM() + "*"
