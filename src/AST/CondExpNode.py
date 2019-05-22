from .ASTNode import ASTNode, varGen
from .FuncNode import FuncNode
from .VarNode import VarNode
from .ArOpNode import ArOpNode
from .Types import opTypes


class CondExpNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'CondExp', maxChildren, ast)
        self.expression = None
        self.left = None
        self.right = None
        self.returnVar = None

    def simplify(self, scope=None):
        self.expression = self.children[1].value
        self.value = self.expression
        self.AST.delNode(self.children[1])
        del self.children[1]
        tmpLeft = self.children[0].simplify(scope)
        tmpRight = self.children[1].simplify(scope)
        if tmpLeft is not self.children[0]:
            self.AST.delNode(self.children[0])
            self.children[0] = tmpLeft
        if tmpRight is not self.children[1]:
            self.AST.delNode(self.children[1])
            self.children[1] = tmpRight
        self.left = tmpLeft
        self.right = tmpRight
        return self

    def printLLVM(self):
        self.returnVar = varGen.getNewVar(varGen)
        code = ""
        l = self.left.printLLVM()
        r = self.right.value  # het type mag niet nog is getoond worden
        if isinstance(self.left, VarNode):
            code += self.left.printLLVM(True)
            l = self.left.getType().printLLVM() + " " + self.left.returnVar
        if isinstance(self.right, VarNode):
            code += self.right.printLLVM(True)
            r = self.right.returnVar
        if isinstance(self.left, FuncNode) or isinstance(self.left, ArOpNode):
            code += self.left.printLLVM()
            l = self.left.getType().printLLVM() + " " + self.left.returnVar
        if isinstance(self.right, FuncNode) or isinstance(self.right, ArOpNode):
            code += self.right.printLLVM()
            r = self.right.returnVar
        op = opTypes[self.value]
        # %6 = icmp eq i32 1, %5
        code += self.returnVar + " = icmp " + op + " " + l + ", " + r + "\n"
        return code