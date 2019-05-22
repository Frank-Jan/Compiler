from .TerNode import TerNode


class numberNode(TerNode):

    def __init__(self, value, ast, pos):
        TerNode.__init__(self, value, ast, pos)

    def simplify(self, scope):
        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        return self

class NumberNode(TerNode):
    def __init__(self, value, ast, pos):
        TerNode.__init__(self, value, ast, pos)

    def getValue(self):
        return self.name

    def simplify(self, scope):
        return self.name