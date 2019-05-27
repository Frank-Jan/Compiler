from .TerNode import TerNode
from .Type import Type, CHAR

class CharNode(TerNode, Type):

    def __init__(self, value, ast, pos):
        Type.__init__(self, CHAR())
        TerNode.__init__(self, value, ast, pos)

    def simplify(self, scope=None):
        toDelete = self.children
        for c in toDelete:
            self.AST.delNode(c)
        self.children = []
        return self

    def printLLVM(self, value = False):
        if len(self.value) == 2:
            raise Exception("error: empty character constant")
        c = str(ord(self.value[1]))
        if value:
            return c
        return self.type.printLLVM() + " " + c

    def toLLVM(self):
        return [self.getType(), ord(self.value[1])]