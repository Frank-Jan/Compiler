from .ASTNode import ASTNode

# CHILDREN THAT ARE NOT PARENTS = LEAFS
class TerNode(ASTNode):  # leafs

    def __init__(self, value, ast, pos):
        if value == '"':
            value = '\\"'
        ASTNode.__init__(self, value, 0, ast)
        # ASTNode.__init__(self, 'TerNode', 0, ast)
        self.child = True
        self.pos = pos

    def simplify(self, scope=None):
        return self.value

    def printLLVM(self):
        return self.value