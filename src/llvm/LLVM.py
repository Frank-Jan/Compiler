from src.AST.Arg import Arg
from src.AST.Types import *
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
