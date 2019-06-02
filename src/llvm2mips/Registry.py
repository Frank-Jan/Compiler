# virtual Registry


# returns string:
def SToStr(index):
    # range: [0-7]
    if index < 0 or index > 7:
        error = "Index saved temporary registry out of bounds [0-7]: {}".format(index)
        raise Exception(error)
    return "$s" + str(index)


def TToStr(index):
    # range [0-9]
    if index < 0 or index > 9:
        error = "Index temporary registry out of bounds [0-9]: {}".format(index)
        raise Exception(error)
    return "$t" + str(index)


def VToStr(index):
    # range [0-1]
    if index < 0 or index > 1:
        error = "Index v registry out of bounds [0-1]: {}".format(index)
        raise Exception(error)
    return "$v" + str(index)


def AToStr(index):
    # range [0-4]
    if index < 0 or index > 4:
        error = "Index argument registry out of bounds [0-9]: {}".format(index)
        raise Exception(error)
    return "$a" + str(index)


def indexToStr(index):
    if index < 1:
        return "$zero"
    if index < 2:
        return "$at"
    if index < 4:
        return "$v" + str(index-2)
    if index < 8:
        return "$a" + str(index-4)
    if index < 16:
        return "$t" + str(index-8)
    if index < 24:
        return "$s" + str(index-16)
    if index < 26:
        return "$t" + str(index-16)
    if index == 28:
        return "$gp"
    if index == 29:
        return "$sp"
    if index == 30:
        return "$fp"
    if index == 31:
        return "$ra"
    return "$" + str(index)


def SPToStr():
    return "$sp"


def FPToStr():
    return "$fp"


def GPToStr():
    return "$gp"


def RAToStr():
    return "$ra"


def StoIndex(index):
    return index + 16


def TtoIndex(index):
    if index < 8:
        return index + 8
    return index + 16


def VtoIndex(index):
    return index+2


def AtoIndex(index):
    return index+4


def GPtoIndex():
    return 28


def SPtoIndex():
    return 29


def FPtoIndex():
    return 30


def RAtoIndex():
    return 31


def Sindices():
    return [16, 17, 18, 19, 20, 21, 22, 23]


def Tindices():
    return [8, 9, 10, 11, 12, 13, 14, 15, 24, 25]


class Registry:
    def __init__(self):
        self.S__ = [None]*8
        self.T__ = [None]*10
        self.V__ = [None]*2
        self.A__ = [None]*4
        self.SP__ = 0
        self.GP__ = 0
        self.FP__ = 0

    # functions to get registers:
    # get stack pointer:
    # number of spaces from starting point:
    def getSP(self):
        return self.SP__

    # return global pointer:
    # number of places from starting point:
    def getGP(self):
        return self.GP__

    # return frame pointer
    # see stack pointer
    def getFP(self):
        return self.FP__

    def getS(self, index):
        return self.S__[index]

    def getT(self, index):
        return self.T__[index]

    def getV(self, index):
        return self.V__[index]

    def getA(self, index):
        return self.A__[index]

    # check if index is empty
    def s_isEmpty(self, index):
        return self.S__[index] is None

    def t_isEmpty(self, index):
        return self.T__[index] is None

    #set registers:
    def setS(self, index, var):
        if not self.s_isEmpty(index):
            self.S__[index].register = None
        var.register = StoIndex(index)
        self.S__[index] = var

    def setT(self, index, var):
        if not self.t_isEmpty(index):
            self.T__[index].register = None
        var.register = TtoIndex(index)
        self.T__[index] = var

    # always overwrite:
    def setA(self, index, var):
        if self.A__[index] is not None:
            self.A__[index].register = None
        self.A__[index] = var
        var.register = AtoIndex(index)

    def setV(self, index, var):
        if self.V__[index] is not None:
            self.V__[index].register = None
        self.V__[index] = var
        var.register = VtoIndex(index)

    def setSP(self, value):
        self.SP__ = value

