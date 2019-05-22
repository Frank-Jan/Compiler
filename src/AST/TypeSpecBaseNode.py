from .Type import Type, VOID
from .ASTNode import ASTNode
from.Types import toType

class TypeSpecBaseNode(Type, ASTNode):

    def __init__(self, value, maxChildren, ast):
        ASTNode.__init__(self, 'TypeSpecBaseNode', maxChildren, ast)
        Type.__init__(self, VOID())

    def setType(self, childType):
        self.type = childType

    def simplify(self, scope=None):
        self.type = toType(self.children[0].value)
        self.AST.delNode(self.children[0])
        self.children = []
        self.value = self.getType()
        return self.getType()
        # self.isSimplified = True
        # self.setType(toType(self.children[0]))
        # self.AST.delNode(self.children[0])
        # self.children = None

    def printLLVM(self):
        return self.type.printLLVM() + " " + self.value