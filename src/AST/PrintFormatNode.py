from .ASTNode import ASTNode, varGen
from .FormatCharPrintNode import FormatCharPrintNode
from .TerNode import TerNode
import src.llvm.LLVM as LLVM


class PrintFormatNode(ASTNode):
    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'printformat', maxChildren, ast)
        self.returnVar = None
        self.returnType = None

    def simplify(self, scope):
        toDelete = []
        newChildren = []
        for c in self.children:
            if isinstance(c, TerNode):
                toDelete.append(c)
            else:
                c.simplify(scope)
                newChildren.append(c)

        for d in toDelete:
            self.AST.delNode(d)
        self.children = newChildren
        return self

    def getFormat(self):
        format = []
        for c in self.children:
            if isinstance(c, FormatCharPrintNode):
                format.append(c.getType())
        return format

    def printLLVM(self):
        # @.str = private unnamed_addr constant [21 x i8] c"hey, een char %c, %i\00", align 1
        strings = "c\""
        self.returnVar = "."+varGen.getNewVar(varGen)[1:]
        count = 1 # om wille van \00 einde
        for child in self.children:
            strings += child.printLLVM()
            count += child.length
        strings += "\\00"
        # -2 voor "c"" en -2 voor "\00
        self.returnType = "[" + str(count) + " x i8]"
        return "@" + self.returnVar + " = private unnamed_addr constant " + self.returnType + " " + strings + "\", align 1\n"

    def toLLVM(self):
        self.returnVar = varGen.getNewVar(varGen)
        deString = ""
        count = 0  # om wille van \00 einde ,  -2 voor "c"" en -2 voor "\00
        for child in self.children:
            deString += child.toLLVM()
            count += child.length
        return LLVM.Str(self.returnVar, deString, count)
