from .ASTNode import ASTNode
from .Type import Type
from .Type import POINTER
from .Type import REFERENCE


class AssignRightNode(ASTNode, Type):

    def __init__(self, ast):
        ASTNode.__init__(self, 'Assign', 2, ast)  # always 2 children

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: AssignRight getType called before simplify")

    def simplify(self, scope):
        self.isSimplified = True
        node = self.children[1].simplify(scope)

        if node is not self.children[1]:
            self.AST.delNode(self.children[1])
        self.AST.delNode(self.children[0])
        self.children = []

        self.type = node.getType()
        if isinstance(node.getType(), REFERENCE):
            self.type = POINTER(node.getType().getBase())

        self.AST.printDotDebug(str(self.getCount()) + "AssignRight.dot")
        return node