from .ArOpNode import ArOpNode
from .Type import compareTypes
from .ASTNode import varGen
from .VarNode import VarNode
from .FuncNode import FuncNode


class ProdNode(ArOpNode):

    def __init__(self, maxChildren, ast):
        ArOpNode.__init__(self, maxChildren, ast)
        ArOpNode.__init__(self, maxChildren, ast)
        self.value = 'Product'
        self.multiplication = True
        self.left = None
        self.right = None
        self.returnVar = None

    def isMultiplication(self):
        return self.multiplication

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: ProdNode getType called before simplify")

    def simplify(self, scope=None):
        self.isSimplified = True
        oldLeft = self.children[0]
        newLeft = oldLeft.simplify(scope)
        if len(self.children) == 1:
            self.AST.delNode(oldLeft)
            self.children = []
            self.AST.printDotDebug(str(self.getCount()) + "Prod.dot")
            self.type = newLeft.getType()
            return newLeft

        self.multiplication = (self.children[1].value == '*')

        oldRight = self.children[2]
        newRight = oldRight.simplify(scope)

        self.AST.delNode(self.children[1])  # delete TerNode +/-
        del self.children[1]
        if newLeft is not oldLeft:
            self.AST.delNode(oldLeft)
            self.children[0] = newLeft
        if newRight is not oldRight:
            self.AST.delNode(oldRight)
            self.children[1] = newRight
        for c in self.children:
            c.parent = self
        self.AST.printDotDebug(str(self.getCount()) + "Prod.dot")
        self.left = self.children[0]
        self.right = self.children[1]

        # check left and right types:
        if not compareTypes(self.left, self.right):
            raise Exception("error: trying to multiply two different types: "
                            "{} and {}".format(self.left.getType(), self.right.getType()))
        self.type = self.left.getType()
        self.deref = self.left.deref

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
        if self.isMultiplication():
            op = "mul"
        else:
            op = "sdiv"
        code += self.returnVar + " = " + op + " " + l + ", " + r + "\n"
        return code
