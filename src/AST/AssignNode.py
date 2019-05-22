from .ASTNode import ASTNode
from .VarNode import VarNode
from .ArOpNode import ArOpNode
from .Type import Type, compareTypes, ARRAY


class AssignNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Assign', maxChildren, ast)
        self.left = None  # right node
        self.right = None  # left node
        self.returnVar = None

    def simplify(self, scope):
        self.left = self.children[0].simplify(scope)
        self.right = self.children[1].simplify(scope)  # assignRight wil return funcNode or ...

        self.AST.delNode(self.children[0])
        self.AST.delNode(self.children[1])
        self.children[0] = self.left
        self.children[1] = self.right
        self.left.parent = self
        self.right.parent = self

        if isinstance(self.left.getType(), ARRAY):
            raise Exception("error: assignment to expression with array type")

        #check if left side is declared/defined and a variable
        # check if declared or defined in symboltable:
        self.left.checkDeclaration(scope)

        # check if left and right have the same type:
        if not compareTypes(self.left, self.right):
            raise Exception("error: assigning two different types: "
                            "{} {} and {} {}".format(self.left.getType().getBase(), self.left.value , self.right.getType(), self.right.value))

        self.AST.printDotDebug(str(self.getCount()) + "Assign.dot")
        return self


    def printLLVM(self):
        code = ""
        #self.returnVar = VarGen.getNewVar(varGen)
        # symbolTable = self.getSymbolTable()
        # record = symbolTable.search(self.left.value)
        # if record is None:
        #     raise Exception("error: VarNode has no record in symbolTable")
        # type = record.getType().printLLVM()
        type = self.right.getType().printLLVM()
        align = self.right.getType().getAlign()

        if isinstance(self.right, VarNode) or isinstance(self.right, ArOpNode):
            code = self.right.printLLVM(True)
            code += "store " + type + " " + self.right.returnVar + ", " + type + "* " + self.left.printLLVM() + align + "\n"  # store i32 %8, i32* %2, align 4
        elif isinstance(self.right, Type):
            code += "store " + self.right.printLLVM() + ", " + type + "* " + self.left.printLLVM() + align + "\n"  # store i32 %8, i32* %2, align 4
        else:
            code = self.right.printLLVM(True)
            code += "store " + type + " " + self.right.returnVar + ", " + type + "* " + self.left.printLLVM() + align + "\n"  # store i32 %8, i32* %2, align 4
        return code