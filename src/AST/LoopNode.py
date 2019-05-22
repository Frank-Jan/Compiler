from .ASTNode import ASTNode

class LoopNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'LoopNode', maxChildren, ast)

    # give local scope
    def simplify(self, scope):
        retNode = self.children[0].simplify(scope)  # return while or ifelseLoop
        self.children = []
        return retNode