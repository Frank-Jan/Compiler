from .ASTNode import ASTNode
from .Type import Type, POINTER, ARRAY, REFERENCE, compareTypes
from .VarNode import VarNode
from .FuncNode import FuncNode
from .ArOpNode import ArOpNode
from .VarDeclNode import VarDeclNode
import src.llvm.LLVM as LLVM

class VarDefNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'VarDef', maxChildren, ast)

    def getName(self):
        if self.isSimplified:
            return self.children[0].getName()
        raise Exception("VarDefNode getName called before simplified")

    def getType(self):
        if self.isSimplified:
            return self.children[0].getType()
        raise Exception("VarDefNode getType called before simplified")

    def simplify(self, scope):
        self.isSimplified = True

        # VarDecl simplify adds variable to node
        varDecl = self.children[0].simplify(scope)  # VarDeclNode
        assignRight = self.children[1].simplify(scope)  # AssignRightNode
        if assignRight is not self.children[1]:
            self.AST.delNode(self.children[1])
            self.children[1] = assignRight

        # check if left and right have the same type:
        if not compareTypes(varDecl, assignRight):
            if isinstance(varDecl.getType(), POINTER) and isinstance(assignRight.getType(), REFERENCE):
                if varDecl.getType().getBase() != assignRight.getType().getBase():
                    raise Exception("error: types don't match in var definition: "
                                    "{} and {}".format(varDecl.getType().getBase(), assignRight.getType()))
            else:
                if not (isinstance(varDecl.getType(), ARRAY) and isinstance(assignRight.getType(), ARRAY)):
                    raise Exception("error: types don't match in var definition: "
                                    "{} {} and {}".format(varDecl.getType(), varDecl.getName(), assignRight.getType()))

        if isinstance(self.children[0].getType(), ARRAY) and isinstance(self.children[1].getType(), ARRAY):
            if self.children[0].getType().array != self.children[1].getType().array:   # check if right array is long enough
                # printError("{} != {}".format(type(self.children[0].getType().array),type(self.children[1].getType().array)))
                raise Exception("error: assigning two elements of different lenghts: {}[{}] and [{}]"
                                .format(self.children[0].getName(), self.children[0].getType().array, self.children[1].getType().array))

            elif isinstance(self.children[0].getType(), ARRAY) and isinstance(self.children[1].getType(), ARRAY):
                if isinstance(self.children[1], VarNode):
                    raise Exception("error: invalid initialisation: array and variable array")

        self.AST.printDotDebug(str(self.getCount()) + "vardef.dot")
        return self

    def printLLVM(self):
        node = self.children[1]
        code = self.children[0].printLLVM(False)
        var = self.children[1].printLLVM()
        if isinstance(node, VarNode):
            code += node.printLLVM(True)
            var = node.getType().printLLVM() + " " + node.returnVar
        elif isinstance(node, FuncNode):
            code += node.printLLVM()
            var = node.returnType.printLLVM() + " " + node.returnVar
        elif isinstance(node, ArOpNode):
            code += node.printLLVM()
            var = node.getType().printLLVM() + " " + node.returnVar
        #else een litnode
        # store i32 0, i32* %1
        code += "store " + var + ", " + self.children[0].type.printLLVM() + "* " + \
                self.children[0].var.printLLVM() + node.getType().getAlign() + "\n"
        return code

    def toLLVM(self):
        node = self.children[1]
        ll = node.toLLVM()
        stats = self.children[0].toLLVM(True)
        if isinstance(node, VarNode):
            ll2 = node.toLLVM(True)
            stats += ll2
            stats += [LLVM.Store(self.getType(), node.returnVar, stats[0].result)]
        elif isinstance(node, FuncNode) or isinstance(node, ArOpNode):
            ll2 = node.toLLVM()
            stats += ll2
            stats += [LLVM.Store(ll2[len(ll2)-1].type, ll2[len(ll2)-1].result, stats[0].result)]
        else:
            stats += [LLVM.Store(ll[0], ll[1], stats[0].result, True)]

        return stats