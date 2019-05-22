from .ASTNode import ASTNode, buildinFunctions
from .TypeSpecFuncNode import TypeSpecFuncNode

class FuncSignNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncSign', maxChildren, ast)
        self.name = None  # name
        self.types = []  # arguments

    def getName(self):
        if self.isSimplified:
            return self.name
        raise (Exception("error: FuncSignNode getName call before simplify"))

    def simplify(self, scope=None):
        self.isSimplified = True
        self.name = self.children[0].simplifyAsName(scope).getName()  # function name

        if self.name in buildinFunctions:
            raise Exception("error: {} already a built-in function".format(self.name))

        toDelete = []  # delete useless Ternodes ('(' ')' ',' variable)
        for c in self.children[1:]:
            if isinstance(c, TypeSpecFuncNode):
                self.types.append(c.simplify(scope))
            else:
                toDelete.append(c)
        args = '('
        for i in self.types:
            args += str(i)
        args += ')'
        for d in toDelete:
            self.AST.delNode(d)
            self.children.remove(d)
            self.AST.printDotDebug(str(self.getCount()) + "FuncSign.dot")
        return self

    def printLLVM(self):
        args = ""
        for type in self.types:
            args += type.printLLVM() + ", "
        args = args[:-2]
        curCode = self.name + "(" + args + ")"
        return curCode