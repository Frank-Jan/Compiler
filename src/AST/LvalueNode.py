from .ASTNode import ASTNode
from .Type import Type, POINTER

class LvalueNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Lvalue', maxChildren, ast)

    def simplify(self, scope):
        if len(self.children) == 1:
            retNode = self.children[0].simplify(scope)
        elif len(self.children) == 2:
            retNode = self.children[1].simplify(scope)
            if not isinstance(retNode.getType(), POINTER):
                raise Exception("error: dereferencing non-pointer")
                # printError("error: dereferencing non-pointer")
                return
            retNode.deref += 1
        else:
            retNode = self.children[2].simplify(scope)  # * and & cancel eachother in '*&'

        if retNode in self.children:
            self.children.remove(retNode)
        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        self.AST.printDotDebug(str(self.getCount()) + "Lvalue.dot")
        return retNode