from .ASTNode import ASTNode
from .Type import Type, INT, VOID
from .Type import compareTypes
from .TerNode import TerNode
from src.SymbolTable import SymbolTable
import src.llvm.LLVM as LLVM


class FuncDefNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncDef', maxChildren, ast)
        Type.__init__(self, INT())  # default return value of a function is integer
        self.fsign = None  # function signature
        self.block = None  # easy acces to code block

    def getName(self):
        return self.fsign.getName()

    def setType(self, type):  # set return type
        self.type = type

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: FuncDefNode getType called before simplify")

    # give scope where function is defined
    def simplify(self, scope):
        self.isSimplified = True
        functionScope = SymbolTable(scope)
        if isinstance(self.children[0], TerNode):
            # TerNode will have void as value
            self.setType(VOID())
        else:
            self.setType(self.children[0].simplify(scope))  # first child is TypeSpecNode

        self.block = self.children[2]

        # simplify function signature and fill functionscope
        self.fsign = self.children[1].simplify(functionScope, self.block)

        # define function in scope
        scope.defineFunction(self.getName(), self.getType(), self.fsign.types, self)

        self.returnTypes = self.children[2].simplify(functionScope)  # simplify code block

        # check if returnstatements are correct:
        if self.type != VOID() and len(self.block.returnStatements) == 0:
            # expected return statements:
            error = "error: Expected return statements in {}".format(self.getName())
            raise Exception(error)

        for r in self.block.returnStatements:
            if not compareTypes(r, self):
                error = "error: Wrong return type in function {}: returns: {}, expected {}".format(self.getName(), str(r.getType()), str(self.getType()))
                raise Exception(error)

        self.AST.printDotDebug(str(self.getCount()) + "FuncDef.dot")
        return self

    def printLLVM(self):
        curCode = "define " + self.getType().printLLVM() + " @" + self.fsign.printLLVM() + "{\n"
        code = ""
        returnVars = []
        for i in range(len(self.fsign.types)):
            var = self.fsign.newNames[i]
            orVar = self.fsign.varNames[i].printLLVM()
            type = self.fsign.types[i].printLLVM()
            align = self.fsign.types[i].getAlign()
            code += orVar + " = alloca " + type + align + "\n"
            code += "store " + type + " " + var + ", " + type + "* " + orVar + align + "\n"

        curCode += code
        curCode += self.block.printLLVM()  # %2 = alloca i32, align 4
        # store i32 %0, i32* %2, align 4
        curCode += "}"
        return curCode

    def toLLVM(self):
        ll = self.fsign.toLLVM()
        t = self.getType()
        return [LLVM.Define(t, ll[0], ll[1:], self.block.toLLVM())]

