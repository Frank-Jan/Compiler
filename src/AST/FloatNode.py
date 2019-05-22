from .TerNode import TerNode
from .Type import Type, FLOAT
from struct import pack, unpack


class FloatNode(TerNode, Type):

    def __init__(self, value, ast, pos):
        Type.__init__(self, FLOAT())
        TerNode.__init__(self, value, ast, pos)

    def simplify(self, scope=None):
        toDelete = self.children
        for c in toDelete:
            self.AST.delNode(c)
        self.children = []
        return self

    def floatprintLLVMHex(self, float):
        # fl = str(hex(unpack('<Q', pack('<d', float(self.value)))[0])).upper()  # llvm wants double hexa value
        single_precision_rep = pack('>f', float)
        single_precision_val = unpack(">f", single_precision_rep)[0]
        double_val = pack('>d', single_precision_val)
        double_hex = "0x" + double_val.hex()
        return double_hex

    def printLLVM(self, value = False):
        # python float = c double
        fl = str(self.floatprintLLVMHex(float(self.value)))
        if value:
            return fl
        return self.type.printLLVM() + " " + fl
