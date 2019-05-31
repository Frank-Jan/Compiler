from .ASTNode import ASTNode
from .Type import Type, POINTER, INT, VOID, ARRAY
from .ShortArrayDeclaration import ShortArrayDeclNode
from .VarNode import VarNode
from .TerNode import TerNode


class ArrayDeclNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'ArrayDecl', maxChildren, ast)
        Type.__init__(self, VOID())
        self.var = None  # VarNode itself
        self.size = None # None betekent moet bepaalt worden door initialiser

    def getName(self):
        if self.isSimplified:
            return self.var.getName()
        raise Exception("error: getName used in VarDeclNode before simplify")

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: getType used in VarDeclNode before simplify")

    def simplify(self, scope):
        self.isSimplified = True
        short = False
        child = self.children[0]
        if isinstance(child, ShortArrayDeclNode):
            short = True
        self.children = child.children
        self.AST.delNode(child)

        if not short:
            self.AST.delNode(self.children[4])  # ']'
            self.size = int(self.children[3].value)
            self.type.array = int(self.children[3].value)

        self.type = ARRAY(self.children[0].simplify(scope))
        self.var = self.children[1].simplifyAsName(scope)
        self.AST.delNode(self.children[2])  # '['
        self.AST.delNode(self.children[3])  # Number or ']'

        if self.size is not None and self.size < 0:
            raise Exception("error: array size is negative")

        self.AST.delNode(self.children[0])
        self.AST.delNode(self.children[1])
        self.children = []
        self.value = str(self.type) + " " + str(self.var)

        scope.insertVariable(self.getName(), self.getType(), self)
        return self