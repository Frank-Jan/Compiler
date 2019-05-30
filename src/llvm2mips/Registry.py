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
        self.__S__ = [None]*8
        self.__T__ = [None]*10
        self.__V__ = [None]*2
        self.__A__ = [None]*4
        self.___SP__ = 0
        self.__GP__ = 0
        self.__FP__ = 0

    # functions to get registers:
    # get stack pointer:
    # number of spaces from starting point:
    def getSP(self):
        return self.___SP__

    # return global pointer:
    # number of places from starting point:
    def getGP(self):
        return self.__GP__

    # return frame pointer
    # see stack pointer
    def getFP(self):
        return self.__FP__

    # check if index is empty
    def s_isEmpty(self, index):
        return self.__S__[index] is None

    def t_isEmpty(self, index):
        return self.__T__[index] is None

    #set registers:
    def setS(self, index, var):
        if not self.s_isEmpty(index):
            self.__S__[index].register = None
        var.register = StoIndex(index)
        self.__S__[index] = var

    def setT(self, index, var):
        if not self.t_isEmpty(index):
            self.__T__[index].register = None
        var.register = TtoIndex(index)
        self.__T__[index] = var

    # always overwrite:
    def setA(self, index, var):
        if self.__A__[index] is not None:
            self.__A__[index].register = None
        self.__A__[index] = var
        var.register = AtoIndex(index)

    def setV(self, index, var):
        if self.__V__[index] is not None:
            self.__V__[index].register = None
        self.__V__[index] = var
        var.register = VtoIndex(index)

    def setSP(self, value):
        self.__S__ = value

