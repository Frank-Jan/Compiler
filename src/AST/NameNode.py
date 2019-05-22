from .TerNode import TerNode

class NameNode(TerNode):
    def __init__(self, value, ast, pos):
        TerNode.__init__(self, value, ast, pos)
        self.name = value

    def getName(self):
        return self.name

    def simplify(self, scope):
        return self.name