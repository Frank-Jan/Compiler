from .Type import Type, VOID
from .ASTNode import ASTNode

class TypeSpecNode(Type, ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'TypeSpecNode', maxChildren, ast)
        Type.__init__(self, VOID())

    def setType(self, childType):
        self.type = childType

    def simplify(self, scope=None):
        type = self.children[0].simplify(scope)
        self.setType(type)
        self.AST.delNode(self.children[0])
        self.children = []
        self.value = self.type
        return self.getType()

    def printLLVM(self):
        return self.type.printLLVM() + " " + self.value