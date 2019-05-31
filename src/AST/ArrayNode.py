from .ASTNode import ASTNode
from .Type import Type, POINTER, INT, VOID, ARRAY
from .VarNode import VarNode
from .TerNode import TerNode


class ArrayNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Array', maxChildren, ast)
        Type.__init__(self, VOID())
        self.length = 0

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: ArrayNode getType called before simplify")

    def getLenght(self):
        if self.isSimplified:
            return self.length
        raise Exception("error: ArrayPrintNode getLength called before simplify")

    def simplify(self, scope):
        self.isSimplified = True
        toDelete = []
        newChildren = []
        for c in self.children:
            if isinstance(c, TerNode):
                toDelete.append(c)
            else:
                node = c.simplify(scope)
                if node is not c:
                    self.AST.delNode(c)
                newChildren.append(node)
                node.parent = self

        for d in toDelete:
            self.AST.delNode(d)

        if len(newChildren) > 0:
            self.type = newChildren[0].getType()
        for c in newChildren:
            if c.getType() != self.type:
                raise Exception("error: types in array don't match: {} and {}".format(self.type, c.getType()))

        self.length = len(newChildren)
        self.type = ARRAY(self.type)
        self.type.array = self.length
        self.children = newChildren
        return self

class ArrayElementNode(VarNode):

    def __init__(self, maxChildren, ast):
        VarNode.__init__(self, maxChildren, ast)
        self.value = "Array Element"
        self.number = 0

    def getNumber(self):
        if self.isSimplified:
            return self.number
        raise Exception("error: ArrayElement getNumber called before simplify")

    def simplify(self, scope):
        self.isSimplified = True
        nameSet = False
        toDelete = []
        newChildren = []
        node = self.children[0].simplify(scope)
        self.name = node.getName()
        #check if varnode is pointer
        if not (isinstance(node.getType(), POINTER)):
            raise Exception("error: used [] on non-pointer")

        self.type = node.getType().getBase()

        self.number = self.children[2].simplify(scope)  #VarNode/functionNode/LitNode

        if self.number is not self.children[2]:
            self.AST.delNode(self.children[2])

        #check if self.number returns/is a integer
        if not isinstance(self.number.getType(), INT):
            raise Exception("error: didn't use integer or return integer for accessing array element")

        self.children[2] = self.number
        self.value = str(self.name) + "[" + str(self.number.value) + "]"

        self.AST.delNode(self.children[3])
        self.AST.delNode(self.children[1])

        self.children.remove(self.children[3])
        self.children.remove(self.children[1])
        return self