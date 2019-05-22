from .ASTNode import varGen
from .ArOpNode import ArOpNode
from .VarNode import VarNode
from .FuncNode import FuncNode
from .Type import compareTypes


class AddNode(ArOpNode):

    def __init__(self, maxChildren, ast):
        ArOpNode.__init__(self, maxChildren, ast)
        self.value = "Addition"
        self.left = None
        self.right = None
        self.returnVar = None  # hulpVar to return
        self.add = True

    def isAddition(self):
        return self.add

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: AddNode getType called before simplify")

    def simplify(self, scope=None):
        self.isSimplified = True
        oldLeft = self.children[0]
        newLeft = oldLeft.simplify(scope)
        if len(self.children) == 1:
            if newLeft is not oldLeft:
                self.AST.delNode(oldLeft)
            self.children = []
            self.type = newLeft.getType()
            self.AST.printDotDebug(str(self.getCount()) + "AddRuleA" + ".dot")
            return newLeft

        self.add = (self.children[1].value == '+')
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
        self.left = self.children[0]
        self.right = self.children[1]

        # check left and right types:
        if not compareTypes(self.left, self.right):
            raise Exception("error: trying to add two different types: "
                            "{} and {}".format(self.left.getType(), self.right.getType()))
        self.type = self.left.getType()

        self.AST.printDotDebug(str(self.getCount()) + "Addnode.dot")
        return self

    def printLLVM(self, load = False):
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
        if self.isAddition():
            op = "add"
        else:
            op = "sub"
        code += self.returnVar + " = " + op + " " + l + ", " + r + "\n"
        return code
