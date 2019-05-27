from .ASTNode import ASTNode, varGen
from .Type import Type, REFERENCE, POINTER, VOID
import src.llvm.LLVM as LLVM

class VarNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        # TerNode.__init__(self, value, ast, pos)
        ASTNode.__init__(self, 'Variable Name', maxChildren, ast)
        Type.__init__(self, VOID())
        self.name = None
        self.record = None
        self.returnVar = None
        self.returnType = None

    def getName(self):
        if self.isSimplified:
            return self.name
        raise Exception("error: VarNode getName called before simplify")


    def getType(self):  # linken met symbol table
        if self.isSimplified:
            return self.type
        raise Exception("error: VarNode getType called before simplify")

    def checkDeclaration(self, scope):
        value = scope.search(self.getName())

        if value is None:
            raise Exception("Variable {} used before declaration".format(self.getName()))
        if not value.isVar():
            raise Exception("{} is a function not a variable".format(self.getName()))
        self.type = value.getType()
        value.isUsed = True
        self.record = value

    # simplify as function name
    def simplifyAsName(self,scope):
        self.isSimplified = True
        self.name = self.children[0].simplify(scope)
        self.value = self.name
        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        return self

    def simplify(self, scope):
        self.isSimplified = True
        self.name = self.children[0].simplify(scope)
        self.value = self.name
        record = scope.search(self.name)
        if record is None:
            raise Exception("{} not yet declared".format(self.name))
        if not record.isVar():
            raise Exception("{} called as var but is function".format(self.name))

        self.type = record.getType()

        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        return self

    def printLLVM(self, load=False):
        # type = self.getType().printLLVM()
        symbolTable = self.getSymbolTable()
        record = symbolTable.search(self.getName())
        if record is None:
            raise Exception("error: VarNode has no record in symbolTable")
        type = record.getType().printLLVM()
        self.returnVar = varGen.getNewVar(varGen)
        self.returnType = self.getType()

        if load:  # %6 = load i32, i32* %2, align 4
            if isinstance(self.getType(), REFERENCE):
                self.returnVar = "%" + self.value
                return "" # want heeft geen load nodig
            elif isinstance(self.getType(), POINTER) and self.deref:
                code = ""
                tmp2 = "%" + self.value
                type = self.getType()
                for niv in range(self.deref):
                    tmp = varGen.getNewVar(varGen)
                    code += tmp + " = load " + type.printLLVM() + ", " + type.printLLVM() + "* " + tmp2 + type.getAlign() + "\n"
                    type = type.getBase()
                    tmp2 = tmp
                self.returnVar = tmp
                self.returnType = self.getType()
                for niv in range(self.deref-1):
                    self.returnType = self.returnType.getBase()
                return code
            else:
                return self.returnVar + " = load " + type + ", " + type + "* %" + self.value + self.getType().getAlign() + "\n"
        else:
            return "%" + self.value  # %6

    def toLLVM(self, LLVMOBJ=False):
        if LLVMOBJ:
            if isinstance(self.getType(), REFERENCE):
                self.returnVar = self.value
                return [] # geen load nodig
            if isinstance(self.getType(), POINTER):
                ll = []
                type = self.getType()
                tmp = varGen.getNewVar(varGen)
                self.returnVar = tmp
                ll.append(LLVM.Load(tmp, type, self.value))
                for niv in range(self.deref-1):
                    type = type.getBase()
                    self.returnVar = varGen.getNewVar(varGen)
                    ll.append(LLVM.Load(self.returnVar, type, tmp))
                    tmp = self.returnVar
                return ll
        else:
            return [self.getType(), self.value]