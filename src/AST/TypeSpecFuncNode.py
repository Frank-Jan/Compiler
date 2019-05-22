from .Type import Type, VOID
from .ASTNode import ASTNode

class TypeSpecFuncNode(Type, ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'TypeSpecFunc', maxChildren, ast)
        Type.__init__(self, VOID())

    def setType(self, childType):
        self.type = childType

    def simplify(self, scope=None):
        # self.isSimplified = True
        self.setType(self.children[0].simplify(scope))
        self.value = self.type
        self.AST.delNode(self.children[0])
        self.children = []

        return self.getType()
        # self.AST.delNode(self.children[0])
        # self.children = None

    def printLLVM(self):
        return self.type.printLLVM() + " " + self.value
