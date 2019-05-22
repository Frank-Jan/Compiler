import copy
from .Types import VOID, REFERENCE,POINTER, INT, FLOAT, CHAR, ARRAY


class Type:
    # for nodes who have a type/return type
    def __init__(self, type=VOID()):
        self.type = type
        self.deref = 1

    def getType(self):
        return self.type  # returns full type (i.e. int ** or char)

    def setType(self, childType):
        self.type = childType


# A en B have to be of class Type
def compareTypes(A,B):
    return dereferenceType(A) == dereferenceType(B)

def dereferenceType(node):
    if isinstance(node, Type):
        tmp = copy.copy(node.deref)
        type_ = copy.copy(node.getType())
        if isinstance(type_, REFERENCE):
            type_ = POINTER(type_.getBase())
        while tmp > 1:
            tmp -= 1
            if isinstance(type_, POINTER):
                type_ = type_.getBase()
            else:
                raise Exception("error: dereferencing non-pointer {}".format(node.value()))
    else:
        raise Exception("error: trying to get dereference from non-type")
    return type_