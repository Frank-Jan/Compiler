from .ASTNode import ASTNode, buildinFunctions, varGen
from .TypeSpecFuncNode import TypeSpecFuncNode
from .VarNode import VarNode
from src.SymbolTable import SymbolTable
from .Arg import Arg




class FuncSignDefNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncSign', maxChildren, ast)
        self.name = None  # name
        self.types = []  # arguments Types
        self.varNames = []  # VarNodes itself (not strings)
        self.returnStatements = []
        self.newNames = []

    def getName(self):
        if self.isSimplified:
            return self.name
        raise (Exception("error: FuncSignNode getName call before simplify"))

    # give a local scope
    def simplify(self, functionscope, codeBlock):
        self.isSimplified = True
        self.name = self.children[0].simplifyAsName(functionscope).getName()

        if self.name in buildinFunctions:
            raise Exception(str(self.pos[0]) + ":" + str(self.pos[1]) + ":error: {} already a built-in function".format(self.name))

        toDelete = []  # delete useless Ternodes ('(' ')' ',' variable)
        for c in self.children[1:]:
            if isinstance(c, TypeSpecFuncNode):
                self.types.append(c.simplify(functionscope))
            elif isinstance(c, VarNode):
                self.varNames.append(c)
            else:
                toDelete.append(c)

        # insert variables of signature in functionscope
        for i in range(len(self.types)):
            self.varNames[i].simplifyAsName(functionscope)
            self.varNames[i].parent = codeBlock
            self.varNames[i].setType(self.types[i])
            functionscope.insertVariable(self.varNames[i].getName(), self.types[i])

        sign = '('
        for i in range(len(self.types)):
            sign += str(self.types[i]) + " " + str(self.varNames[i]) + ", "
        sign += ')'
        for d in toDelete:
            self.AST.delNode(d)
            self.children.remove(d)
        self.AST.printDotDebug(str(self.getCount()) + "FuncSignDef.dot")
        return self

    def buildSymbolTable(self, globalscope):
        localScope = SymbolTable(globalscope)
        # insert variables
        for i in range(len(self.types)):
            localScope.insertVariable(self.varNames[i], self.types[i])
        return localScope

    def printLLVM(self):
        args = ""
        for i in range(len(self.types)):
            args += self.types[i].printLLVM()
            self.newNames.append(varGen.getNewVar(varGen))
            args += " " + self.newNames[i] + ", "
        args = args[:-2]
        curCode = self.name + "(" + args + ")"
        return curCode

    def toLLVM(self):
        ll = [self.name]
        for i in range(len(self.types)):
            self.newNames.append(varGen.getNewVar(varGen))
            varInfo = self.varNames[i].toLLVM()
            arg = Arg(varInfo[0], varInfo[1], self.newNames[i])
            ll.append(arg)
        return ll