from .TerNode import TerNode
from .Type import Type, INT


class IntNode(TerNode, Type):

    def __init__(self, value, ast, pos):
        Type.__init__(self, INT())
        TerNode.__init__(self, value, ast, pos)

    def simplify(self, scope=None):
        toDelete = self.children
        for c in toDelete:
            self.AST.delNode(c)
        self.children = []
        return self

    def printLLVM(self, value=False):
        if value:
            return self.value
        return self.type.printLLVM() + " " + self.value

    def toLLVM(self):
        return [self.getType(), self.value]
