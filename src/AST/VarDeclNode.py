from .ASTNode import ASTNode
from .Type import Type, ARRAY, POINTER, FLOAT
import src.llvm.LLVM as LLVM


class VarDeclNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'VarDecl', maxChildren, ast)
        Type.__init__(self)
        # self.type = None  # Types
        self.var = None  # VarNode itself
        self.size = 0

    def getName(self):
        if self.isSimplified:
            return self.var.getName()
        raise Exception("error: getName used in VarDeclNode before simplify")

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: getType used in VarDeclNode before simplify")

    def simplify(self, scope):
        self.isSimplified = True
        if len(self.children) == 2:
            # no array
            self.size = 1
            self.type = self.children[0].simplify(scope)
            self.var = self.children[1].simplifyAsName(scope)
        else:
            self.size = int(self.children[3].value)
            self.type = ARRAY(self.children[0].simplify(scope))
            self.var = self.children[1].simplifyAsName(scope)

            self.type.array = int(self.children[3].value)
            self.AST.delNode(self.children[2])  # '('
            self.AST.delNode(self.children[3])  # Number
            self.AST.delNode(self.children[4])  # ')'

            if self.size < 0:
                raise Exception("error: array size is negative")

        self.AST.delNode(self.children[0])
        self.AST.delNode(self.children[1])
        self.children = []
        self.value = str(self.type) + " " + str(self.var)

        scope.insertVariable(self.getName(), self.getType(), self)
        return self

    def buildSymbolTable(self, symbolTable):
        if not symbolTable.insertVariable(self.var.value, self.type):
            raise Exception("error: {} already defined/declared in local scope".format(self.var.value))

    def printLLVM(self, init=True):
        type = self.getType()
        # %1 = alloca i32, align 4
        code = self.var.printLLVM() + " = alloca " + self.type.printLLVM() + type.getAlign() + "\n"
        # if init = True, initialize standard on 0
        if init and not isinstance(type, POINTER):
            waarde = 0
            if isinstance(type, FLOAT):
                waarde = 0.0
            code += "store " + self.type.printLLVM() + " " + str(waarde) +", " + self.type.printLLVM() + "* " + \
                    self.var.printLLVM() + type.getAlign() + "\n"
        return code

    def toLLVM(self, vardef = False):
        #% 2 = alloca i32, align 4
        ll = [LLVM.Alloca(self.var.value, self.getType())]
        #initilize 0
        if not vardef and not isinstance(type, POINTER):
            waarde = 0
            if isinstance(type, FLOAT):
                waarde = 0.0
            ll.append(LLVM.Store(self.getType(), waarde, self.var.value, True))
        return ll