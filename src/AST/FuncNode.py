from .ASTNode import ASTNode, varGen
from .Type import Type, POINTER, INT
from .ValueNode import ValueNode
from .PrintfNode import PrintfNode
from .VarNode import VarNode


class FuncNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Func', maxChildren, ast)
        Type.__init__(self, INT())
        self.name = None
        self.arguments = []
        self.returnVar = None  # hulpvar om waarde te returnen
        self.record = None  # node to func definition

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: FuncNode getType called before simplify")

    def getName(self):
        if self.isSimplified:
            return self.name
        raise Exception("error: FuncNode getName called before simplify")

    def simplify(self, scope):
        self.isSimplified = True

        if isinstance(self.children[0], PrintfNode):
            printf = self.children[0].simplify(scope)
            self.children.remove(printf)
            self.AST.delNode(self)
            self.children = []
            return printf

        self.name = self.children[0].simplifyAsName(scope).getName()

        for c in self.children[1:]:
            if isinstance(c, ValueNode):
                self.arguments.append(c.simplify(scope))

        toDelete = [item for item in self.children[1:] if item not in self.arguments]
        for c in toDelete:
            self.AST.delNode(c)
        self.children = [self.children[0]]
        self.children += self.arguments

        # check if exist in scope:
        value = scope.search(self.name)
        if value is None:
            raise Exception("error: function {} called before declaration".format(self.name))
        if value.isVar():
            raise Exception("error: {} is a variable not a function".format(self.name))
        value.isUsed = True
        self.record = value
        self.type = self.record.getType()
        self.AST.printDotDebug(str(self.getCount()) + "func.dot")
        self.value = self.name + '(' + ')'
        return self

    def printLLVM(self, load = True):
        self.returnVar = varGen.getNewVar(varGen)
        self.returnType = self.getType()
        code = ""
        args = ""
        type = ""
        for arg in self.arguments:
            if isinstance(arg, VarNode):
                code += arg.printLLVM(True)
                type = arg.getType()
                args += arg.getType().printLLVM() + " " + arg.returnVar + ", "
            else:
                args += arg.printLLVM() + ", "
        args = args[:-2]

        stat = code + self.returnVar + " = call " + self.getType().printLLVM() + " "
        stat = stat + "@" + self.name + "(" + args + ")\n"  # symboltable.gettype
        if isinstance(self.getType(), POINTER):
            code = ""
            tmp2 = self.returnVar
            type = self.getType().getBase()
            # tmp = varGen.getNewVar(varGen)
            print('funcnode')
            if self.deref == 1:
                tmp = self.returnVar
                type = self.getType()
            for niv in range(self.deref-1):
                print('t')
                tmp = varGen.getNewVar(varGen)
                code += tmp + " = load " + type.printLLVM() + ", " + type.printLLVM() + "* " + tmp2 + type.getAlign() + "\n"
                type = type.getBase()
                tmp2 = tmp
            self.returnVar = tmp
            self.returnType = type
            for niv in range(self.deref - 1):
                self.returnType = self.returnType.getBase()
        return stat + code
