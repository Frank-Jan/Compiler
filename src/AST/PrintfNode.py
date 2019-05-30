from .ASTNode import ASTNode, varGen
from .Type import Type, INT
from .TerNode import TerNode
from .PrintFormatNode import PrintFormatNode
from .IoArgListNode import IoArgListNode


class PrintfNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'printf', maxChildren, ast)
        Type.__init__(self, INT())  # default return value of a function is integer
        self.format = None
        self.argList = None
        self.name = "printf"
        self.returnVar = None
        self.strings = None

    def getStrings(self):
        return self.strings

    def getFormat(self):
        if self.isSimplified:
            return self.format
        raise Exception("printf getFormat() called before simplify")

    def getArgList(self):
        if self.isSimplified:
            return self.argList
        raise Exception("printf getArgList() called before simplify")

    def getName(self):
        return "printf"

    def setType(self, type):  # set return type
        pass

    def getType(self):
        return INT()

    # give scope where function is defined
    def simplify(self, scope):
        self.isSimplified = True
        #check if printf is defined:
        value = scope.search("printf")
        if value is None:
            raise Exception("printf not declarded, add #include <stdio.h>")

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
        # format = self.children[0].getFormat()    #printformat node
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
        code += stat + "(i8*, ...) @printf(i8* getelementptr inbounds ("+self.format.returnType+", "+self.format.returnType+"* " + \
               "@"+self.format.returnVar +", i32 0, i32 0)"
        if self.argList is not None:
            code += self.argList.printLLVM(False)
        code += ")\n"
        return code

    def toLLVM(self):
        ll = self.format.toLLVM()
        ll += self.argList.toLLVM()
        return ll