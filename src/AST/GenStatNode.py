from .ASTNode import ASTNode


class GenStatNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenStat', maxChildren, ast)

    def simplify(self, scope):
        # only children need to simplify
        retNode = self.children[0].simplify(scope)
        self.AST.printDotDebug(str(self.getCount()) + "GenStatNode.dot")
        if retNode is not self.children[0]:
            self.AST.delNode(self.children[0])
        self.children.remove(self.children[0])
        return retNode
