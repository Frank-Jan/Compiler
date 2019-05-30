from .TerNode import TerNode
from .Type import INT, POINTER, CHAR
from .Types import PPP
import src.llvm.LLVM as LLVM
from .Arg import Arg


class StdioNode(TerNode):
    def __init__(self, value, ast, pos):
        TerNode.__init__(self, '#include <stdio>', ast, pos)
        ast.stdio = True  # depricated?

    def simplify(self, scope):
        # add printf(char* format,...)
        # add scanf(const char* format,...)
        scope.defineFunction("printf", INT(), [POINTER(CHAR())], self)
        scope.defineFunction("scanf", INT(), [POINTER(CHAR())], self)
        return self

    def printLLVM(self):
        code = "declare i32 @printf(i8*, ...)\ndeclare i32 @scanf(i8*, ...)\n\n"
        return code

    def toLLVM(self):
        return [LLVM.Declare(INT(), "printf", [POINTER(CHAR()), PPP()]),
                             LLVM.Declare(INT(), "scanf", [POINTER(CHAR()), PPP()])]
