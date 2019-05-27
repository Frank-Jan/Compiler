from .ScopeNode import ScopeNode
from .ASTNode import ASTNode


class CodeBlockNode(ScopeNode):

    def __init__(self, maxChildren, ast, symboltable=None):
        ASTNode.__init__(self, 'CodeBlock', maxChildren, ast)
        self.returnStatements = []  # full return statements
        self.endCode = False  # if code behind the while loop is reachable

    def simplify(self, scope):
        self.symbolTable = scope

        funcSyntax = self.children[1]
        funcSyntax.simplify(scope)
        self.returnStatements += funcSyntax.returnStatements

        # delete first and last node ('{' and '}')
        self.AST.delNode(self.children[2])
        self.AST.delNode(self.children[0])
        del self.children[2]
        del self.children[0]

        # is endCode if functionSyntax is endCode
        self.endCode = funcSyntax.endCode
        self.returnStatements = funcSyntax.returnStatements
        # steal children of funcSyntax
        self.children = funcSyntax.children
        for c in self.children:
            c.parent = self
        funcSyntax.children = []
        self.AST.delNode(funcSyntax)

        return self.returnStatements

    def getSymbolTable(self):
        return self.symbolTable

    def printLLVM(self):
        code = "\n"
        for child in self.children:
            code += child.printLLVM() + "\n"
        return code

    def toLLVM(self):
        stats = []
        for child in self.children:
            stats = child.toLLVM()
        return stats
