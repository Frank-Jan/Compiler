from .ASTNode import ASTNode
from .VarDefNode import VarDefNode

class GenDefNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenDef', maxChildren, ast)

    def simplify(self, scope):
        self.searchPos()
        node = self.children[0]
        retNode = node.simplify(scope)
        if isinstance(node, VarDefNode):
            if not node.isConstant():
                raise Exception(str(self.pos[0]) + ":" + str(self.pos[1]) + ":error: not a compile-time constant: {}".format(type(node)))
        self.children = []
        return retNode