from .ASTNode import ASTNode, varGen
from .Type import Type, INT
from .TerNode import TerNode
from .PrintFormatNode import PrintFormatNode
from .IoArgListNode import IoArgListNode
import src.llvm.LLVM as LLVM


class ScanfNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'scanf', maxChildren, ast)
        Type.__init__(self, INT())  # default return value of a function is integer
        self.format = None
        self.argList = None
        self.name = "scanf"
        self.returnVar = None
        self.strings = None

    def getStrings(self):
        return self.strings

    def getFormat(self):
        if self.isSimplified:
            return self.format
        raise Exception("scanf getFormat() called before simplify")

    def getArgList(self):
        if self.isSimplified:
            return self.argList
        raise Exception("scanf getArgList() called before simplify")

    def getName(self):
        return "scanf"

    def setType(self, type):  # set return type
        pass

    def getType(self):
        return INT()

    # give scope where function is defined
    def simplify(self, scope):
        self.isSimplified = True
        #check if scanf is defined:
        value = scope.search("scanf")
        if value is None:
            raise Exception(str(self.pos[0]) + ":" + str(self.pos[1]) + "scanf not declared, add #include <stdio.h>")

        toDelete = []
        newChildren = []
        for c in self.children:
            if isinstance(c, TerNode):
                toDelete.append(c)
            elif isinstance(c, PrintFormatNode):
                c.simplify(scope)
                newChildren.append(c)
            elif isinstance(c, IoArgListNode):
                node = c.simplify(scope)
                if node is not c:
                    toDelete.append(c)
                newChildren.append(node)
                self.argList = node
            else:
                node = c.simplify(scope)
                if node is not c:
                    toDelete.append(c)
                newChildren.append(node)
        self.format = newChildren[0]
        self.children = newChildren
        for c in toDelete:
            self.AST.delNode(c)

        self.checkInput()
        return self

    def checkInput(self):
        #check if all inputs are correct
        # format = self.children[0].getFormat()    #scanformat node
        # inputValues = self.children[1].getInputTypes()
        #
        pass

    def printLLVM(self):
        self.strings = self.format.printLLVM() + "\n"#get strings
        self.returnVar = varGen.getNewVar(varGen)
        type = self.getType().printLLVM()
        code = ""
        if self.argList is not None:
            code += self.argList.printLLVM(True)
        stat = self.returnVar + " = call " + type + " "
        code += stat + "(i8*, ...) @scanf(i8* getelementptr inbounds ("+self.format.returnType+", "+self.format.returnType+"* " + \
               "@"+self.format.returnVar +", i32 0, i32 0)"
        if self.argList is not None:
            code += self.argList.printLLVM(False)
        code += ")\n"
        return code

    def toLLVM(self):
        llStr = self.format.toLLVM()
        ll = [llStr]
        ll += self.argList.toLLVM()
        ll += [LLVM.CallF(varGen.getNewVar(varGen), self.argList.args, llStr, False)]
        return ll