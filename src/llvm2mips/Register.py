#virtual register
from enum import Enum

#registry types
class Registry(Enum):
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


class Register:
    def __init__(self):
        # Register types:                   length:
        self.__RType__ = [Registry.zero]    #1
        self.__RType__ += [Registry.at]     #2
        self.__RType__ += [Registry.v] * 2  #4
        self.__RType__ += [Registry.a] * 4  #8
        self.__RType__ += [Registry.t] * 8  #16
        self.__RType__ += [Registry.s] * 8  #24
        self.__RType__ += [Registry.t] * 2  #26
        self.__RType__ += [Registry.k] * 2  #28
        self.__RType__ += [Registry.gp]     #29
        self.__RType__ += [Registry.sp]     #30
        self.__RType__ += [Registry.fp]     #31
        self.__RType__ += [Registry.ra]     #32

        # Register:
        self.__R__ = [None]*len(self.__RType__)
        self.__R__[0] = 0

    # returns -1 if not in registry or in exempted registries
    # registry index otherwise
    def inRegistry(self, value):
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
            if self.__RType__[i] == Registry.t and self.__R__ is None:
                return i
        return -1

    # returns -1 if no empty saved temporary register
    # returns index of empty temporary
    def getEmptyS(self):
        for i in range(len(self.__RType__)):
            if self.__RType__[i] == Registry.s and self.__R__ is None:
                return i
        return -1

    def getSizeA(self):
        return self.__RType__.count(Registry.a)

    def getSizeT(self):
        return self.__RType__.count(Registry.t)

    def getSizeS(self):
        return self.__RType__.count(Registry.s)

    def getSizeV(self):
        return self.__RType__.count(Registry.v)

    def getS(self):
        result = []
        for i in range(len(self.__RType__)):
            if self.__RType__[i] == Registry.s:
                result.append(self.__R__[i])
        return result

    def getT(self):
        result = []
        for i in range(len(self.__RType__)):
            if self.__RType__[i] == Registry.t:
                result.append(self.__R__[i])
        return result

    def getV(self):
        result = []
        for i in range(len(self.__RType__)):
            if self.__RType__[i] == Registry.s:
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
        return t != Registry.at and t != Registry.k

    def isWrite(self, index):
        t = self.type(index)
        return t != Registry.at and t != Registry.k and t != Registry.zero

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


