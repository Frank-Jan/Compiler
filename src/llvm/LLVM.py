from src.AST.Arg import Arg
from src.AST.Types import *
from src.AST.ASTNode import varGen
import copy


class LLVMInstr:

    def __init__(self):
        self.line = 0


class Alloca(LLVMInstr):

    def __init__(self, result, _type):
        LLVMInstr.__init__(self)
        self.result = result
        self.type = _type
        self.align = _type.getAlign()

    def __str__(self):
        tmpType = self.type.toLLVM()

        return "%" + str(self.result) + " = alloca " + str(tmpType) + ", align " + str(self.align) + "\n"


class Store(LLVMInstr):

    def __init__(self, _type, _from, _to, lit=False):
        LLVMInstr.__init__(self)
        self.type = _type
        self._from = _from
        self._to = _to
        self.align = _type.getAlign()
        self.lit = lit

    def __str__(self):
        tmpType = self.type.toLLVM()
        if self.lit:
            return "store " + str(tmpType) + " " + str(self._from) + ", " + str(tmpType) + "* %" + str(
                self._to) + ", align " + str(self.align) + "\n"
        else:
            return "store " + str(tmpType) + " %" + str(self._from) + ", " + str(tmpType) + "* %" + str(
                self._to) + ", align " + str(self.align) + "\n"


class Load(LLVMInstr):

    def __init__(self, result, _type, var):
        LLVMInstr.__init__(self)
        self.result = result
        self.type = _type
        self.var = var
        self.align = _type.getAlign()

    def __str__(self):
        tmpType = self.type.toLLVM()
        return "%" + str(self.result) + " = load " + str(tmpType) + ", " + str(tmpType) + "* %" + str(
            self.var) + ", align " + str(self.align) + "\n"


class Define(LLVMInstr):

    def __init__(self, _type, name, args, stats):
        LLVMInstr.__init__(self)
        self.type = _type
        self.name = name
        self.args = args  # arg has _type, oldname and newname
        self.stats = stats

    def __iter__(self):
        return self.stats.__iter__()

    def __str__(self):
        tmpType = self.type.toLLVM()
        ll = "define " + str(tmpType) + " @" + str(self.name) + "("
        for arg in self.args:
            ll += str(arg.type.toLLVM()) + " %" + str(arg.tempName) + ", "
        if len(self.args) != 0:
            ll = ll[:-2]
        ll += ") {\n"

        # load values from newNames into oldNames
        load = []
        for arg in self.args:
            load.append(Alloca(arg.ogName, arg.type))
            load.append(Store(arg.type, arg.tempName, arg.ogName))
        self.stats = load + self.stats

        for stat in self.stats:
            ll += str(stat)
        ll += "}\n\n"
        return ll


class endDefine(LLVMInstr):

    def __init__(self, define):
        LLVMInstr.__init__(self)
        self.beginDefine = define


class Call(LLVMInstr):  # %2 = call i32 @test()

    def __init__(self, result, _type, name, args):
        self.result = result
        self.type = _type
        self.name = name
        self.args = args  # arg has _type, oldname and newname

    def __str__(self):
        tmpType = self.type.toLLVM()
        ll = "%" + str(self.result) + " = call " + str(tmpType) + " @" + str(self.name) + "("
        for arg in self.args:
            if arg.lit:
                ll += str(arg.type.toLLVM()) + " " + str(arg.ogName) + ", "
            else:
                ll += str(arg.type.toLLVM()) + " %" + str(arg.ogName) + ", "
        if len(self.args) != 0:
            ll = ll[:-2]
        ll += ")\n"
        return ll


class Return(LLVMInstr):  # ret i32 %6

    def __init__(self, _type, var, lit=False):
        self.type = _type
        self.var = var  # in case of void var = ""
        self.lit = lit

    def __str__(self):
        tmpType = self.type.toLLVM()
        retVal = ""
        if self.lit == True:
            retVal = str(self.var)
        else:
            retVal = "%" + str(self.var)

        return "ret " + str(tmpType) + " " + str(retVal) + "\n"


# ARITHMETIC
########################################################################
class Arithmetic(LLVMInstr):

    def __init__(self, result, op, _type, val1, val2, lit1=False, lit2=False):
        LLVMInstr.__init__(self)
        self.result = result
        self.op = op
        self.type = _type
        self.val1 = val1
        self.val2 = val2
        self.lit1 = lit1
        self.lit2 = lit2

    def __str__(self):
        tmpType = self.type.toLLVM()
        lit1 = "%"
        lit2 = "%"
        if self.lit1:
            lit1 = ""
        if self.lit2:
            lit2 = ""
        return "%" + str(self.result) + " = " + str(self.op) + " " + str(tmpType) + " " + lit1 + str(
            self.val1) + ", " + lit2 + str(self.val2) + "\n"


class Add(Arithmetic):

    def __init__(self, result, _type, val1, val2, lit1=False, lit2=False):
        Arithmetic.__init__(self, result, _type.getAdd(), _type, val1, val2, lit1, lit2)


class Sub(Arithmetic):

    def __init__(self, result, _type, val1, val2, lit1=False, lit2=False):
        Arithmetic.__init__(self, result, _type.getSub(), _type, val1, val2, lit1, lit2)


class Mul(Arithmetic):

    def __init__(self, result, _type, val1, val2, lit1=False, lit2=False):
        Arithmetic.__init__(self, result, _type.getMul(), _type, val1, val2, lit1, lit2)


class Div(Arithmetic):

    def __init__(self, result, _type, val1, val2, lit1=False, lit2=False):
        Arithmetic.__init__(self, result, _type.getDiv(), _type, val1, val2, lit1, lit2)
########################################################################


class Branch:

    def __init__(self, result, stats1, stats2, label0=None):
        self.result = result
        self.label0 = label0
        self.label1 = Label()
        self.label2 = Label()
        self.label3 = Label()
        self.stats1 = stats1
        self.stats2 = stats2

    def __str__(self):
        #br i1 %5, label %6, label %7
        ll = "br i1 %" + str(self.result) + ", label %" + self.label1.label + ", label %" + self.label2.label + "\n\n"

        ll += str(self.label1)
        for stat in self.stats1:
            ll += str(stat)
        if self.label0 is None:
            ll += "br label %"+ self.label3.label + "\n\n"
        else:# while node
            ll += "br label %" + self.label0.label + "\n\n"

        ll += str(self.label2)
        for stat in self.stats2:
            ll += str(stat)
        ll += "br label %"+ self.label3.label + "\n\n"
        ll += str(self.label3)
        return ll


class Icmp:

    def __init__(self, op, _type, val1, val2, lit1=False, lit2=False):
        self.result = varGen.getNewVar(varGen)
        self.op = op
        self.type = _type
        self.val1 = val1
        self.val2 = val2
        self.lit1 = lit1
        self.lit2 = lit2
        self.label0 = varGen.getNewLabel(varGen)

    def __str__(self):
        #%5 = icmp eq i32 1, %4
        tmpType = self.type.toLLVM()
        lit1 = "%"
        lit2 = "%"
        if self.lit1:
            lit1 = ""
        if self.lit2:
            lit2 = ""
        ll = "%" + str(self.result) + " = icmp " + str(self.op) + " " + str(tmpType) + " " + lit1 + str(
            self.val1) + ", " + lit2 + str(self.val2) + "\n"
        return ll

class Label:

    def __init__(self, br=False):
        self.label = varGen.getNewLabel(varGen)
        self.br = br

    def __str__(self):
        ll = ""
        if self.br:
            ll += "\nbr label %" + self.label + "\n"
        ll += self.label + ":\n"
        return ll