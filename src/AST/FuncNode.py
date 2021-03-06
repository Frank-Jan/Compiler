from .ASTNode import ASTNode, varGen
from .Type import Type, POINTER, INT
from .ValueNode import ValueNode
from .PrintfNode import PrintfNode
from .VarNode import VarNode
from .ScanfNode import ScanfNode
import src.llvm.LLVM as LLVM
from .Arg import Arg
from .TerNode import TerNode
from .IntNode import IntNode


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

        if isinstance(self.children[0], PrintfNode) or isinstance(self.children[0], ScanfNode):
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
            raise Exception(str(self.pos[0]) + ":" + str(self.pos[1]) + ":error: function {} called before declaration".format(self.name))
        if value.isVar():
            raise Exception(str(self.pos[0]) + ":" + str(self.pos[1]) + ":error: {} is a variable not a function".format(self.name))

        # check if argument types are correct
        if len(self.arguments) != len(value.argumentList):
            raise Exception(
                str(self.pos[0]) + ":" + str(self.pos[1]) + ":error: {} has a different signature".format(self.name))
        for i in range(len(self.arguments)):
            if value.argumentList[i] != self.arguments[i].getType():
                raise Exception(
                    str(self.pos[0]) + ":" + str(self.pos[1]) + ":error: {} has a different signature".format(
                        self.name))


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

    def toLLVM(self, load=True):
        tmp = varGen.getNewVar(varGen)
        self.returnVar = tmp

        stats = []
        args = []
        for arg in self.arguments:
            if isinstance(arg, VarNode):
                stats += arg.toLLVM(True)
                stat = stats[len(stats)-1]
                args.append(Arg(stat.type, stat.result, None, False))
            else:
                a = arg.toLLVM()
                args.append(Arg(a[0], a[1], None, True))

        stats += [LLVM.Call(self.returnVar, self.getType(), self.name, args)]
        type = self.getType()
        if isinstance(type, POINTER):
            for niv in range(self.deref-1):
                type = type.getBase()
                self.returnVar = varGen.getNewVar(varGen)
                stats.append(LLVM.Load(self.returnVar, type, tmp))
                tmp = self.returnVar

        return stats

