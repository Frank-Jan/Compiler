from .ASTNode import ASTNode, varGen
from .Type import Type, VOID, CHAR, ARRAY, INT, FLOAT
import src.llvm.LLVM as LLVM


class FormatCharScanNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FormatChar', maxChildren, ast)
        Type.__init__(self, VOID())
        self.width = 0
        self.length = 0

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: FormatCharScanNode getType called before simplify")

    def getWidth(self):
        if self.isSimplified:
            return self.width
        raise Exception("error: FormatCharScanNode getWidth called before simplify")

    def simplify(self, scope):
        self.isSimplified = True
        self.value = self.children[0].value[0] + self.children[0].value[-1]
        if len(self.children[0].value) > 2:
            self.width = int(self.children[0].value[1:-1])

        if self.value == "%c":
            self.type = CHAR()
        elif self.value == "%s":
            self.type = ARRAY(CHAR())
        elif self.value == "%i":
            self.type = INT()
        elif self.value == "%d":
            self.type = INT()
        elif self.value == "%f":
            self.type = FLOAT()
        else:
            raise Exception("error: unknown format specifier {}".format(self.value))

        self.AST.delNode(self.children[0])
        self.children = []
        return self

    def printLLVM(self):
        width = str(self.getWidth())
        if width == '0':
            width = ""
        code = str(self.value[:1]) + width + str(self.value[-1:])
        self.length = len(code)
        return code

    def toLLVM(self):
        self.returnVar = varGen.getNewVar(varGen)
        width = str(self.getWidth())
        if width == '0':
            width = ""
        deString = str(self.value[:1]) + width + str(self.value[-1:])
        return LLVM.Str(self.returnVar, deString, len(deString)+1)