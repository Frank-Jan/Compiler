from .ASTNode import ASTNode

class GenDeclNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenDecl', maxChildren, ast)

    def simplify(self, scope=None):
        # only children need to simplify
        retNode = self.children[0].simplify(scope)
        self.children = []
        return retNode