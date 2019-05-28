from .ASTNode import ASTNode
from .Type import Type


class ArOpNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'ArOp', maxChildren, ast)
        Type.__init__(self)

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: ArOpNode getType called before simplify")

    def simplify(self, scope=None):
        node = self.children[0].simplify(scope)
        if node is not self.children[0]:
            self.AST.delNode(self.children[0])
        self.AST.printDotDebug(str(self.getCount()) + "ArOpNode.dot")
        self.children = []
        return node
