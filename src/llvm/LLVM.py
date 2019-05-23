from src.AST.Arg import Arg
from src.AST.Types import *
import copy


class Alloca:

    def __init__(self, result, _type, align=4):
        self.result = result
        self.type = _type
        self.align = align

    def __str__(self):
        tmpType = self.type.toLLVM()

        return "%" + str(self.result) + " = alloca " + str(tmpType) + ", align " + str(self.align) + "\n"


class Store:

    def __init__(self, _type, _from, _to, align=4):
        self.type = _type
        self._from = _from
        self._to = _to
        self.align = align

    def __str__(self):
        tmpType = self.type.toLLVM()
        return "store " + str(tmpType) + " %" + str(self._from) + ", " + str(tmpType) + "* %" + str(
            self._to) + ", align " + str(self.align) + "\n"


class Load:

    def __init__(self, result, _type, var, align=4):
        self.result = result
        self.type = _type
        self.var = var
        self.align = align

    def __str__(self):
        tmpType = self.type.toLLVM()
        return str(self.result) + " = load " + str(tmpType) + ", " + str(tmpType) + "* " + str(
            self.var) + ", align " + str(self.align) + "\n"


class Define:

    def __init__(self, _type, name, args, stats):
        self.type = _type
        self.name = name
        self.args = args  # arg has _type, oldname and newname
        self.stats = stats

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


# ARITHMETIC
########################################################################
class Arithmetic:

    def __init__(self, result, op, _type, val1, val2):
        self.result = result
        self.op = op
        self.type = _type
        self.val1 = val1
        self.val2 = val2

    def __str__(self):
        tmpType = self.type.toLLVM()
        return str(self.result) + " = " + str(self.op) + " " + str(tmpType) + " " + str(self.val1) + ", " + str(
            self.val2) + "\n"


class Add(Arithmetic):

    def __init__(self, result, _type, val1, val2):
        Arithmetic.__init__(result, "add", _type, val1, val2)


class Sub(Arithmetic):

    def __init__(self, result, _type, val1, val2):
        Arithmetic.__init__(result, "sub", _type, val1, val2)


class Mull(Arithmetic):

    def __init__(self, result, _type, val1, val2):
        Arithmetic.__init__(result, "mull", _type, val1, val2)


class Div(Arithmetic):

    def __init__(self, result, _type, val1, val2):
        Arithmetic.__init__(result, "sdiv", _type, val1, val2)
########################################################################
