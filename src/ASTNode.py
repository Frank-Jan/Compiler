


class ASTNode:

    def __init__(self, value, size):
        self.value = value
        self.nextNodes = []
        self.size = size
        self.child = False
        self.id = 0
        for i in range(self.size):
            self.nextNodes.append(None)

    def __str__(self):
        return str(self.value) + "  (" + str(self.id) + ")" #\nNrChildren: " + str(self.size)

    def isRoot(self):
        return self.value == "Root"

    def isChild(self):
        return self.child

    def hasMaxChildren(self):
        count = 0
        for child in self.nextNodes:
            if child != None:
                count += 1
        return self.size == count

class GenStatNode(ASTNode):

    def __init__(self, size):
        ASTNode.__init__(self, 'GenStat', size)


class AssignNode(ASTNode):

    def __init__(self, size):
        ASTNode.__init__(self, 'Assign', size)

class FuncDefNode(ASTNode):

    def __init__(self, size):
        ASTNode.__init__(self, 'FuncDef', size)

class FuncSignNode(ASTNode):

    def __init__(self, size):
        ASTNode.__init__(self, 'FuncSign', size)

class CodeBlockNode(ASTNode):

    def __init__(self, size):
        ASTNode.__init__(self, 'CodeBlock', size)

class FuncSyntaxNode(ASTNode):

    def __init__(self, size):
        ASTNode.__init__(self, 'FuncSyntax', size)

class FuncStatNode(ASTNode):

    def __init__(self, size):
        ASTNode.__init__(self, 'FuncStat', size)

class ArOpNode(ASTNode):

    def __init__(self, size):
        ASTNode.__init__(self, 'ArOp', size)

class ProdNode(ASTNode):

    def __init__(self, size):
        ASTNode.__init__(self, 'Prod', size)

#CHILDREN THAT ARE NOT PARENTS = LEAFS
class TerNode(ASTNode):

    def __init__(self, value):
        ASTNode.__init__(self, value, 0)
        self.child = True

class VarNode(ASTNode):

    def __init__(self, value):
        ASTNode.__init__(self, value, 0)
        self.child = True

class LitNode(ASTNode):

    def __init__(self, value):
        ASTNode.__init__(self, value, 0)
        self.child = True

class TypeSpecBaseNode(ASTNode):

    def __init__(self, value):
        ASTNode.__init__(self, value, 0)
        self.child = True
