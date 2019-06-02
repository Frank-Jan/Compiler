from .ASTNode import ASTNode
from .Type import Type, POINTER, ARRAY, REFERENCE, compareTypes
from .VarNode import VarNode
from .FuncNode import FuncNode
from .ArOpNode import ArOpNode
from .ArrayInitialiser import ArrayInitNode
from .VarDeclNode import VarDeclNode
from .ArrayDeclaration import ArrayDeclNode
from .TerNode import TerNode
from .ArrayNode import ArrayNode
import src.llvm.LLVM as LLVM


class VarDefNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'VarDef', maxChildren, ast)
        self.glob = False

    def getName(self):
        if self.isSimplified:
            return self.children[0].getName()
        raise Exception("VarDefNode getName called before simplified")

    def getType(self):
        if self.isSimplified:
            return self.children[0].getType()
        raise Exception("VarDefNode getType called before simplified")

    def isConstant(self):
        if self.isSimplified:
            constant = self.children[-1]
            if isinstance(constant, TerNode):
                return True
            elif isinstance(constant, VarNode):
                if isinstance(constant.getType(), REFERENCE):
                    return True
            return False
        raise Exception("VarDefNode isConstant called before simplified")

    def simplify(self, scope):
        self.isSimplified = True

        if scope.parent is None:
            self.glob = True

        # VarDecl simplify adds variable to node
        varDecl = self.children[0].simplify(scope)  # VarDeclNode
        assignRight = self.children[1]  # AssignRightNode or ArrayINitNode

        if isinstance(assignRight, ArrayInitNode):
            children = assignRight.stealChildren()
            self.AST.delNode(assignRight)
            assignRight = children[1]
            self.AST.delNode(children[0])

        assignRight = assignRight.simplify(scope)  # AssignRightNode

        if assignRight is not self.children[1]:
            self.AST.delNode(self.children[1])
            self.children[1] = assignRight

        # check if left and right have the same type:
        if not compareTypes(varDecl, assignRight):
            if isinstance(varDecl.getType(), POINTER) and isinstance(assignRight.getType(), REFERENCE):
                if varDecl.getType().getBase() != assignRight.getType().getBase():
                    raise Exception(
                        str(self.pos[0]) + ":" + str(self.pos[1]) + "error: types don't match in var definition: "
                                                                    "{} and {}".format(varDecl.getType().getBase(),
                                                                                       assignRight.getType()))
            else:
                if not (isinstance(varDecl.getType(), ARRAY) and isinstance(assignRight.getType(), ARRAY)):
                    raise Exception(
                        str(self.pos[0]) + ":" + str(self.pos[1]) + "error: types don't match in var definition: "
                                                                    "{} {} and {}".format(varDecl.getType(),
                                                                                          varDecl.getName(),
                                                                                          assignRight.getType()))

        if isinstance(self.children[0].getType(), ARRAY) and isinstance(self.children[1].getType(), ARRAY):
            if self.children[0].size is None:
                self.children[0].setSize(self.children[1].length)

            elif self.children[0].size < self.children[1].length:  # check if right array is long enough
                # printError("{} != {}".format(type(self.children[0].getType().array),type(self.children[1].getType().array)))
                raise Exception(str(self.pos[0]) + ":" + str(
                    self.pos[1]) + "error: assigning initialiser greater than array: {}[{}] and [{}]"
                                .format(self.children[0].getName(), self.children[0].getType().array,
                                        self.children[1].getType().array))

            if isinstance(self.children[1], VarNode):
                raise Exception(str(self.pos[0]) + ":" + str(
                    self.pos[1]) + "error: invalid initialisation: array and variable array")

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
        # else een litnode
        # store i32 0, i32* %1
        code += "store " + var + ", " + self.children[0].type.printLLVM() + "* " + \
                self.children[0].var.printLLVM() + node.getType().getAlign() + "\n"
        return code

    def toLLVM(self):
        node = self.children[1]
        if isinstance(node, ArrayNode):
            node.length = self.children[0].size
            self.children[0].arrayInit = node
        ll = node.toLLVM()
        stats = self.children[0].toLLVM(True)

        if self.glob:
            res = self.children[0].var.value
            type = self.getType()
            lit = True
            var = ll[1]
            if isinstance(node, VarNode):
                lit = False

            glob = LLVM.Global(res, type, var, lit)
            stats += [glob]
        else:
            if isinstance(node, VarNode):
                ll2 = node.toLLVM(True)
                stats += ll2
                stats += [LLVM.Store(self.getType(), node.returnVar, stats[0].result)]
            elif isinstance(node, ArrayNode):
                stats += ll
            elif isinstance(node, FuncNode) or isinstance(node, ArOpNode):
                ll2 = node.toLLVM()
                stats += ll2
                stats += [LLVM.Store(ll2[len(ll2) - 1].type, ll2[len(ll2) - 1].result, stats[0].result)]
            else:
                stats += [LLVM.Store(ll[0], ll[1], stats[0].result, True)]

        return stats
