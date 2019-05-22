from .Type import Type, VOID, REFERENCE
from .ASTNode import ASTNode



class TypeSpecReferenceNode(Type, ASTNode):

    def __init__(self, value, maxChildren, ast):
        ASTNode.__init__(self, 'TypeSpecRef', maxChildren, ast)
        Type.__init__(self, VOID())

    def getType(self):
        return self.type

    def setType(self, childType):
        self.type = REFERENCE(childType)

    def simplify(self, scope=None):
        self.setType(self.children[0].simplify(scope))
        self.value = self.getType()
        return self.getType()

    def printLLVM(self):
        return self.type.printLLVM() + " " + self.value