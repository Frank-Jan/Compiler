class VOID:
    def getType(self):
        return 0

    def __str__(self):
        return "void"

    def __eq__(self, other):
        return self.__str__() == other.__str__()

class CHAR(VOID):
    def getType(self):
        return 1

    def __str__(self):
        return "char"

class INT(VOID):
    def getType(self):
        return 2

    def __str__(self):
        return "int"

class FLOAT(VOID):
    def getType(self):
        return 3

    def __str__(self):
        return "float"

class POINTER(VOID):
    def __init__(self, type):
        self.type = type

    def getType(self):
        return 4

    def getBase(self):
        return self.type

    def __str__(self):
        return self.type.__str__() + "*"

class REFERENCE(VOID):
    def __init__(self, type):
        self.type = type

    def getType(self):
        return 5

    def getBase(self):
        return self.type

    def __str__(self):
        return self.type.__str__() + "&"