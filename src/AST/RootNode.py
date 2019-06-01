from .ScopeNode import ScopeNode
from .GenStatNode import GenStatNode
from src.SymbolTable import SymbolTable
import src.llvm.LLVM as LLVM


class RootNode(ScopeNode):
    def __init__(self, value, maxChildren, ast):
        ScopeNode.__init__(self, value, maxChildren, ast)
        self.symbolTable = SymbolTable()

    def setParent(self, parentScope):
        pass  # is the highest parent (global scope)

    def simplify(self, scope=None):
        toDelete = []
        newChildren = []
        for c in self.children:
            if isinstance(c, GenStatNode):
                tmp = c.simplify(self.symbolTable)
                newChildren.append(tmp)
            else:
                toDelete.append(c)

        for c in self.children:
            self.AST.delNode(c)
        self.children = newChildren
        self.AST.printDotDebug(str(self.getCount()) + "RootSimplify.dot")
        return self

    def toLLVM(self):
        stats = [LLVM.Memcpy()]
        for child in self.children:
            stats += child.toLLVM()
        return stats