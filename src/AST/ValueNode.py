from .ASTNode import ASTNode
from .Type import Type, POINTER


class ValueNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Value', maxChildren, ast)

    def simplify(self, scope):
        if len(self.children) == 1:
            retNode = self.children[0].simplify(scope)
            if retNode is not self.children[0]:
                self.AST.delNode(self.children[0])
            self.children = []
        else:
            #*value
            retNode = self.children[1].simplify(scope)
            if retNode is not self.children[1]:
                self.AST.delNode(self.children[1])
            self.children = []
            if not isinstance(retNode.getType(), POINTER):
                raise Exception("Dereferencing non-pointer")
            retNode.deref += 1

        self.AST.printDotDebug(str(self.getCount()) + "value" + ".dot")
        self.AST.printDotDebug(str(self.getCount()) + "Value.dot")
        return retNode

    def printLLVM(self):
        return self.value
