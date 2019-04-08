


class ASTNode:

    def __init__(self, value, size, ast):
        self.value = value
        self.parent = None# tupel of parent node and position
        self.nextNodes = []
        self.size = size
        self.AST = ast
        self.id = 0
        self.simplified = False
        for i in range(self.size):
            self.nextNodes.append(None)

    def __str__(self):
        return str(self.value) + "  (" + str(self.id) + ")" #\nNrChildren: " + str(self.size)

    def isRoot(self):
        return self.value == "Root"

    def isChild(self):
        return self.size == 0

    def hasMaxChildren(self):
        count = 0
        for child in self.nextNodes:
            if child != None:
                count += 1
        return self.size == count

    def timeToSimplify(self):
        for node in self.nextNodes:
            if not node.simplified:
                return False
        return True

    def simplify(self):
        self.simplified = True

        if self.parent == None or self.size == 0:
            return
        elif self.size == 2:
            self.AST.delNode(self.nextNodes[1])
        elif self.size > 2:
            print("Say whut?!")

        self.parent[0].nextNodes[self.parent[1]] = self.nextNodes[0]
        self.AST.delNode(self)


class GenStatNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'GenStat', size, ast)


class AssignNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'Assign', size, ast)

    def simplify(self):
        self.simplified = True

class FuncDefNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'FuncDef', size, ast)

    def simplify(self):
        self.simplified = True

class FuncSignNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'FuncSign', size, ast)

    def simplify(self):
        self.simplified = True

class CodeBlockNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'CodeBlock', size, ast)

    def simplify(self):
        self.simplified = True

class FuncSyntaxNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'FuncSyntax', size, ast)

    def simplify(self):
        self.simplified = True

class FuncStatNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'FuncStat', size, ast)


class ArOpNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'ArOp', size, ast)

    def simplify(self):
        self.simplified = True

class ProdNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'Prod', size, ast)

    def simplify(self):
        self.simplified = True

class IdentNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'Ident', size, ast)


class AtomNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'Atom', size, ast)

    def simplify(self):
        self.simplified = True

class ReturnStatNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'ReturnStat', size, ast)

    def simplify(self):
        self.simplified = True

class VarDefNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'VarDef', size, ast)

    def simplify(self):
        self.simplified = True

class GenDefNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'GenDef', size, ast)


class VarDeclNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'VarDecl', size, ast)
        self.type = ""
        self.var = ""

    def simplify(self):
        self.simplified = True
        val = ""
        for node in self.nextNodes:
            if isinstance(node, TypeSpecBaseNode):
                self.type = node.value
            elif isinstance(node, VarNode):
                self.var = node.value
            val += node.value + " "
            self.AST.delNode(node)

        self.nextNodes = []
        self.size = 0
        self.value = val

class FuncNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'Func', size, ast)

    def simplify(self):
        self.simplified = True

class LitNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'Lit', size, ast)

class GenDeclNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'GenDecl', size, ast)


class TypeSpecNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'TypeSpec', size, ast)


#CHILDREN THAT ARE NOT PARENTS = LEAFS
class TerNode(ASTNode):

    def __init__(self, value, ast):
        ASTNode.__init__(self, value, 0, ast)
        self.child = True
        self.simplified = True

class VarNode(TerNode):

    def __init__(self, value, ast):
        TerNode.__init__(self, value, ast)

class TypeSpecBaseNode(TerNode):

    def __init__(self, value, ast):
        TerNode.__init__(self, value, ast)

class IntNode(TerNode):

    def __init__(self, value, ast):
        TerNode.__init__(self, value, ast)

class FloatNode(TerNode):

    def __init__(self, value, ast):
        TerNode.__init__(self, value, ast)
