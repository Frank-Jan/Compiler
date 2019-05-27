from src.VarGen import VarGen


varGen = VarGen()

counter = 0  # counter to make sure all print debug filenames are unique

buildinFunctions = ["printf", "scanf"]



class ASTNode:

    def __init__(self, value, maxChildren, ast):
        self.value = value  # waarde van de node
        self.parent = None  # tupel of parent node and position
        self.children = []  # children
        self.maxChildren = maxChildren  # max aantal children
        self.AST = ast
        self.id = 0
        self.isSimplified = False
        for i in range(self.maxChildren):
            self.children.append(None)

    def removeChild(self, child):
        if child in self.children:
            self.children.remove(child)

    def stealChildren(self):
        children = self.children
        self.children = []
        return children

    def getCount(self):
        global counter
        counter += 1
        return counter

    def __str__(self):
        return str(self.value) + "  [" + str(self.id) + "]"  # \nNrChildren: " + str(self.maxChildren)

    def isRoot(self):
        return self.value == "Root"

    def buildSymbolTable(self, symbolTable):
        return symbolTable

    def isLeaf(self):
        return len(self.children) == 0

    def hasMaxChildren(self):
        count = 0
        for child in self.children:
            if child is not None:
                count += 1
        return self.maxChildren == count

    def printLLVM(self):
        if len(self.children) == 0:
            print("TO DO LLVM: " + str(type(self)))

        code = ""
        for child in self.children:
            code += child.printLLVM()  # + "\n"
        return code

    def toLLVM(self):
        raise Exception("toLLVM() method not yet implemented in: " + str(type(self)))

    def simplify(self, scope):
        # Base simplify will only call simplify(scope) on all children
        raise Exception("Called ASTNode simplify on {}".format(type(self)))

    def getSymbolTable(self):
        return self.parent.getSymbolTable()
