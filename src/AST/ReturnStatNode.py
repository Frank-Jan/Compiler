from .ASTNode import ASTNode
from .Type import Type, VOID
from .ArOpNode import ArOpNode
from .VarNode import VarNode
from .IntNode import IntNode
from .FloatNode import FloatNode
from .FuncNode import FuncNode
from .CharNode import CharNode
import src.llvm.LLVM as LLVM

class ReturnStatNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'ReturnStat', maxChildren, ast)
        Type.__init__(self, VOID())
        self.returnVal = None
        self.child = None

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: ReturnStatNode getType called before simplify")

    def simplify(self, scope):
        self.isSimplified = True
        self.AST.delNode(self.children[0])  # del return TerNode
        del self.children[0]
        if len(self.children) == 0:
            self.setType(VOID())  # no return value
        else:
            node = self.children[0].simplify(scope)
            if isinstance(node, FuncNode) or isinstance(node, ArOpNode) or isinstance(node, VarNode):
                if node is not self.children[0]:
                    self.AST.delNode(self.children[0])
                self.children[0] = node
            # can't take type because a function's output might be returned
            elif isinstance(node, IntNode) or isinstance(node, FloatNode) or isinstance(node, CharNode):
                self.AST.delNode(self.children[0])
                del self.children[0]
                self.children.append(node)
            else:
                raise "ReturnStatNode forgot something: {}".format(type(node))
            self.type = node.getType()
            self.child = node

        self.AST.printDotDebug(str(self.getCount()) + "ReturnStat.dot")
        return self

    def printLLVM(self):
        code = "ret "
        if len(self.children) == 0:
            return "ret void"
        for child in self.children:
            if isinstance(child, FuncNode) or isinstance(child, ArOpNode):
                return child.printLLVM() + "ret " + child.getType().printLLVM() + " " + child.returnVar
            elif isinstance(child, VarNode):
                return child.printLLVM(True) + "ret " + child.getType().printLLVM() + " " + child.returnVar
            code += child.printLLVM()  # + "\n"
        return code

    def toLLVM(self):
        if (self.child == None):
            return [LLVM.Return(self.getType(), "", True)]
        if isinstance(self.child, IntNode):
            tmp = self.child.toLLVM()
            return [LLVM.Return(tmp[0], tmp[1], True)]
        else:
            ll = []
            if isinstance(self.child, VarNode):
                ll = self.child.toLLVM(True)
            if len(ll) == 0:
                self.child.toLLVM()
            ll.append(LLVM.Return(self.child.getType(), self.child.returnVar))
            return ll
