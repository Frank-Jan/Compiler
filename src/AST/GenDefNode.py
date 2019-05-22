from .ASTNode import ASTNode

class GenDefNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenDef', maxChildren, ast)

    def simplify(self, scope):
        retNode = self.children[0].simplify(scope)
        self.children = []
        return retNode