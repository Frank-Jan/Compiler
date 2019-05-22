from .ASTNode import ASTNode
from src.SymbolTable import SymbolTable

class ScopeNode(ASTNode):
    def __init__(self, value, maxChildren, ast):
        ASTNode.__init__(self, value, maxChildren, ast)
        self.symbolTable = None

    def getSymbolTable(self):
        if self.symbolTable is None:
            parent = None
            if self.parent is not None:
                parent = self.parent.getSymbolTable()
            self.symbolTable = SymbolTable(parent)
        return self.symbolTable

    def setParent(self, parentScope):
        self.symbolTable.parent = parentScope