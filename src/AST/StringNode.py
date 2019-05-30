from .ASTNode import ASTNode
from .Type import Type, ARRAY, CHAR
from .Types import llvmStrings, pythonStrings


class StringNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'StringNode', maxChildren, ast)
        Type.__init__(self, ARRAY(CHAR()))
        self.length = None

    def getString(self):
        if self.isSimplified:
            return self.value
        raise Exception("error: StringNode getString called before simplify()")

    def simplify(self, scope):
        self.isSimplified = True
        self.value = ""
        i=0 # want python leest python string OPNIEUW in als python string...
        while i < len(self.children):
            if self.children[i].value == '\\':
                if self.children[i+1].value != '\\':
                    self.value += pythonStrings[self.children[i+1].value]
                    i += 2
                    continue
                i += 1
            self.value += self.children[i].value
            i += 1

        for c in self.children:
            self.AST.delNode(c)
        self.children = []

        return self

    def printLLVM(self):
        new = ""
        count = 0
        stuk = self.getString()
        if stuk == "":
            return llvmStrings['']
        for i in range(len(stuk)):
            stukje = stuk[i]
            try:
                new += llvmStrings[stukje]
                count += 1
            except(KeyError):
                count += 1
                new += stukje
        self.length = count
        return new

    def toLLVM(self):
        new = ""
        count = 0
        stuk = self.getString()
        if stuk == "":
            return llvmStrings['']
        for i in range(len(stuk)):
            stukje = stuk[i]
            try:
                new += llvmStrings[stukje]
                count += 1
            except(KeyError):
                count += 1
                new += stukje
        self.length = count
        return new
