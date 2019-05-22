from .ASTNode import ASTNode
from .Type import Type, VOID
from .TerNode import TerNode

class FuncDeclNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncDecl', maxChildren, ast)
        self.fsign = None

    def setType(self, type):  # set return type
        self.type = type

    def simplify(self, scope):
        if isinstance(self.children[0], TerNode):
            # TerNode will have void as value
            self.setType(VOID())
        else:
            self.setType(self.children[0].simplify(scope))  # first child is TypeSpecNode
        self.children[1].simplify(scope)  # simplify funcSign
        self.fsign = self.children[1]

        self.buildSymbolTable(scope)
        return self

    def buildSymbolTable(self, symbolTable):
        string = "BST: Funcdecl: " + str(self.type) + " " + self.fsign.name + "("
        if len(self.fsign.types) >= 1:
            string += str(self.fsign.types[0])
        if len(self.fsign.types) > 1:
            for a in self.fsign.types[1:]:
                string += ", " + str(a)
        string += ")"

        symbolTable.declareFunction(self.fsign.name, self.type, self.fsign.types, self)
        return symbolTable

    def printLLVM(self):
        curCode = "declare " + self.type.printLLVM() + " @" + self.fsign.printLLVM()
        return curCode