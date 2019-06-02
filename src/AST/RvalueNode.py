from .ASTNode import ASTNode
from .Type import Type, REFERENCE


class RvalueNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Rvalue', maxChildren, ast)

    def simplify(self, scope):
        retNode = None
        if len(self.children) == 1:
            retNode = self.children[0].simplify(scope)
        elif len(self.children) == 2:
            retNode = self.children[1].simplify(scope)  # simplify lvalue node
            retNode.type = REFERENCE(retNode.getType())
        else:
            raise Exception(str(self.pos[0]) + ":" + str(self.pos[1]) + ":error: unexpected number of children (" + len(
                self.children) + ") in: " + type(RvalueNode))
            retNode = None

        if retNode in self.children:
            self.children.remove(retNode)
        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        self.AST.printDotDebug(str(self.getCount()) + "Rvalue.dot")
        return retNode
