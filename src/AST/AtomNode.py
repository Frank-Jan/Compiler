from .ASTNode import ASTNode


class AtomNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Atom', maxChildren, ast)

    def simplify(self, scope):
        if len(self.children) > 1:
            # rule: (ArOpNode)
            retNode = self.children[1].simplify(scope)
            if retNode is not self.children[1]:
                self.AST.delNode(self.children[1])
            self.AST.delNode(self.children[0])
            self.AST.delNode(self.children[2])
        else:
            retNode = self.children[0].simplify(scope)
            if retNode is not self.children[0]:
                self.AST.delNode(self.children[0])
        self.children = []
        self.AST.printDotDebug(str(self.getCount()) + "AtomNode" + ".dot")
        self.AST.printDotDebug(str(self.getCount()) + "Atom.dot")
        return retNode
