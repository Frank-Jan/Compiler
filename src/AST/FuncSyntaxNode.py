from .ASTNode import ASTNode
from .FuncStatNode import FuncStatNode
from .ReturnStatNode import ReturnStatNode
from .CodeBlockNode import CodeBlockNode
from .LoopNode import LoopNode
from .TerNode import TerNode
from .FuncDefNode import FuncDefNode
from src.SymbolTable import SymbolTable



class FuncSyntaxNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncSyntax', maxChildren, ast)
        self.returnStatements = []
        self.endCode = False

    def simplify(self, scope):
        new_children = []
        for c in self.children:
            if self.endCode:
                self.AST.delNode(c)
            elif isinstance(c, FuncStatNode) or isinstance(c, FuncDefNode):
                tmp = c.simplify(scope)
                if tmp is not None:
                    new_children.append(tmp)
                if tmp is not c:
                    self.AST.delNode(c)
                if isinstance(tmp, ReturnStatNode):
                    self.returnStatements.append(tmp)
                    self.endCode = True
            elif isinstance(c, CodeBlockNode):
                # create new scope for CodeBlock
                localScope = SymbolTable(scope)
                returnStat = c.simplify(localScope)
                self.endCode = c.endCode
                new_children.append(c)
            elif isinstance(c, LoopNode):
                # needs new scope
                localScope = SymbolTable(scope)
                node = c.simplify(localScope)
                self.returnStatements += node.returnStatements
                self.endCode = node.endCode
                new_children.append(node)
                if node is not c:
                    self.AST.delNode(c)
            elif isinstance(c, TerNode):
                self.AST.delNode(c)
                continue
            else:
                print("Forgot something in FuncSyntax simplify: ", type(c))
        self.children = new_children
        self.AST.printDotDebug(str(self.getCount()) + "FuncSyntax.dot")
        return self
