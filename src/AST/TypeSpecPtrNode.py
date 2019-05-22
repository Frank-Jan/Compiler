from .Type import Type, POINTER, VOID
from .ASTNode import ASTNode
from .TerNode import TerNode

class TypeSpecPtrNode(Type, ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'TypeSpecPtr', maxChildren, ast)
        Type.__init__(self, POINTER())

    def setType(self, childType):
        self.type = POINTER(childType)

    def simplify(self, scope=None):
        if isinstance(self.children[0], TerNode):
            # first child is 'void'
            self.setType(VOID())
        else:
            self.setType(self.children[0].simplify(scope))  # first child is the type
            # second child holds "*"
        return self.type

    def printLLVM(self):
        return self.type.printLLVM() + " " + self.value