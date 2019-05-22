from .ASTNode import ASTNode
from .VarNode import VarNode
from .LitNode import LitNode

class FuncStatNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncStat', maxChildren, ast)

    def simplify(self, scope):
        if isinstance(self.children[0], VarNode) or isinstance(self.children[0], LitNode):
            self.AST.delNode(self.children[0])
            del self.children[0]
            return None
        ret = self.children[0].simplify(scope)
        del self.children[0]
        self.AST.printDotDebug(str(self.getCount()) + "Funcstat.dot")
        return ret
