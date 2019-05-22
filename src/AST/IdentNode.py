from .ASTNode import ASTNode

class IdentNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Ident', maxChildren, ast)