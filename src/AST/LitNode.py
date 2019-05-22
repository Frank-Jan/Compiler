from .ASTNode import ASTNode
from .Type import Type, VOID

class LitNode(ASTNode, Type):

    def __init__(self, maxChildren, ast, _type=VOID()):
        ASTNode.__init__(self, "LIT", maxChildren, ast)
        Type.__init__(self, _type)

    def getValue(self):
        return self.value

    def simplify(self, scope=None):
        retNode = self.children[0].simplify(scope)
        self.value = self.children[0].value
        self.setType(self.children[0].getType())
        self.children.remove(retNode)
        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        return retNode
