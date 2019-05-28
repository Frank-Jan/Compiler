# virtual Registry
from enum import Enum

# registry types
class RegistryEnum(Enum):
    #name:  value:   Read/Write:
    zero    = 0     #R
    at      = 1     #
    v       = 2     #RW
    a       = 3     #RW
    t       = 4     #RW
    s       = 5     #RW
    k       = 6     #
    gp      = 7     #RW
    sp      = 8     #RW
    fp      = 9     #RW
    ra      = 10    #RW


class Registry:
    def __init__(self):
        # Register types:                   length:
        self.__RType__ = [RegistryEnum.zero]    #1
        self.__RType__ += [RegistryEnum.at]     #2
        self.__RType__ += [RegistryEnum.v] * 2  #4
        self.__RType__ += [RegistryEnum.a] * 4  #8
        self.__RType__ += [RegistryEnum.t] * 8  #16
        self.__RType__ += [RegistryEnum.s] * 8  #24
        self.__RType__ += [RegistryEnum.t] * 2  #26
        self.__RType__ += [RegistryEnum.k] * 2  #28
        self.__RType__ += [RegistryEnum.gp]     #29
        self.__RType__ += [RegistryEnum.sp]     #30
        self.__RType__ += [RegistryEnum.fp]     #31
        self.__RType__ += [RegistryEnum.ra]     #32

        # Registry:
        self.__R__ = [None]*len(self.__RType__)
        self.__R__[0] = 0

    # returns False if not in registry or in exempted registries
    def inRegistry(self, value):
        if value in self.__RType__:
            index = self.__RType__.index(value)
            if self.isWrite(index):
                return True
            return False
        return False

    def getRegistry(self, value):
        if value in self.__RType__:
            index = self.__RType__.index(value)
            if self.isWrite(index):
                return index
            return -1
        return -1

    # returns -1 if no empty temporary register
    # return index of empty temporary
    def getEmptyT(self):
        for i in range(len(self.__RType__)):
            if self.__RType__[i] == RegistryEnum.t and self.__R__ is None:
                return i
        return -1

    # returns -1 if no empty saved temporary register
    # returns index of empty temporary
    def getEmptyS(self):
        for i in range(len(self.__RType__)):
            if self.__RType__[i] == RegistryEnum.s and self.__R__ is None:
                return i
        return -1

    def getSizeA(self):
        return self.__RType__.count(RegistryEnum.a)

    def getSizeT(self):
        return self.__RType__.count(RegistryEnum.t)

    def getSizeS(self):
        return self.__RType__.count(RegistryEnum.s)

    def getSizeV(self):
        return self.__RType__.count(RegistryEnum.v)

    def getSRegister(self):
        result = []
        for i in range(len(self.__RType__)):
            if self.__RType__[i] == RegistryEnum.s:
                result.append(self.__R__[i])
        return result

    def getTRegister(self):
        result = []
        for i in range(len(self.__RType__)):
            if self.__RType__[i] == RegistryEnum.t:
                result.append(self.__R__[i])
        return result

    def getVRegister(self):
        result = []
        for i in range(len(self.__RType__)):
            if self.__RType__[i] == RegistryEnum.s:
                result.append(self.__R__[i])
        return result

    # returns register type
    def type(self, index):
        if index < 0 or index > 31:
            error = "Registry index out of bounds [0-31]: {}".format(index)
            raise Exception(error)
        return self.__RType__[index]

    def isRead(self, index):
        t = self.type(index)
        return t != RegistryEnum.at and t != RegistryEnum.k

    def isWrite(self, index):
        t = self.type(index)
        return t != RegistryEnum.at and t != RegistryEnum.k and t != RegistryEnum.zero

    def __getitem__(self, index):
        if self.isWrite(index):
            return self.__R__[index]

    def setT(self, index, value):
        # range [0-9]
        if index < 0 or index > 9:
            error = "Index temporary registry out of bounds [0-9]: {}".format(index)
            raise Exception(error)
        if index < 8:
            self.__R__[index+8] = value
        else:
            self.__R__[index+16] = value
        
    def setS(self, index, value):
        # range: [0-7]
        if index < 0 or index > 7:
            error = "Index saved temporary registry out of bounds [0-7]: {}".format(index)
            raise Exception(error)
        self.__R__[index+16] = value
    
    def setV(self, index, value):
        # range [0-1]
        if index < 0 or index > 1:
            error = "Index expression evaluation registry out of bounds [0-1]: {}".format(index)
            raise Exception(error)
        self.__R__[index+2] = value
    
    def setA(self, index, value):
        # range [0-3]
        if index < 0 or index > 3:
            error = "Index argument registry out of bounds [0-3]: {}".format(index)
            raise Exception(error)
        self.__R__[index+1] = value
        
    def setGP(self, value):
        self.__R__[28] = value
    
    def setSP(self, value):
        self.__R__[29] = value

    def setFP(self, value):
        self.__R__[30] = value

    def setRA(self, value):
        self.__R__[31] = value

    def getT(self, index):
        # range [0-9]
        if index < 0 or index > 9:
            error = "Index temporary registry out of bounds [0-9]: {}".format(index)
            raise Exception(error)
        if index < 8:
            return self.__R__[index + 8]
        else:
            return self.__R__[index + 16]

    def getS(self, index):
        # range: [0-7]
        if index < 0 or index > 7:
            error = "Index saved temporary registry out of bounds [0-7]: {}".format(index)
            raise Exception(error)
        return self.__R__[index + 16]

    def getV(self, index):
        # range [0-1]
        if index < 0 or index > 1:
            error = "Index expression evaluation registry out of bounds [0-1]: {}".format(index)
            raise Exception(error)
        return self.__R__[index + 2]

    def getA(self, index):
        # range [0-3]
        if index < 0 or index > 3:
            error = "Index argument registry out of bounds [0-3]: {}".format(index)
            raise Exception(error)
        return self.__R__[index + 1]

    def getGP(self):
        return self.__R__[28]

    def getSP(self):
        return self.__R__[29]

    def getFP(self):
        return self.__R__[30]

    def getRA(self):
        return self.__R__[31]


def indexToStr(index):
    if index < 0 or index > 31:
        raise Exception("Registry: index out of bounds: {}".format(index))
    return "$" + str(index)


def tIndexToStr(index):
    if index < 0 or index > 9:
        raise Exception("Registry: index out of bounds: {}".format(index))
    if index < 8:
        return "$" + str(index + 8)
    else:
        return "$" + str(index + 16)


def sIndexToStr(index):
    if index < 0 or index > 7:
        raise Exception("Registry: index out of bounds: {}".format(index))
    return "$" + str(index + 16)


def vIndexToStr(index):
    if index < 0 or index > 1:
        raise Exception("Registry: index out of bounds: {}".format(index))
    return "$" + str(index + 2)


def aIndexToStr(index):
    if index < 0 or index > 3:
        raise Exception("Registry: index out of bounds: {}".format(index))
    return "$" + str(index + 4)


def gpIndexToStr(index=0):
    return "$" + str(28)


def spIndexToStr(index=0):
    return "$" + str(29)


def fpIndexToStr(index=0):
    return "$" + str(30)


def raIndexToStr(index=0):
    return "$" + str(31)


def getTindices():
    indices = list(range(8, 16)) + [24, 25]
    return indices


def getSindices():
    indices = list(range(16, 24))
    return indices