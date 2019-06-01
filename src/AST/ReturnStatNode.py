from .ASTNode import ASTNode
from .Type import Type, VOID
from .ArOpNode import ArOpNode
from .VarNode import VarNode
from .IntNode import IntNode
from .FloatNode import FloatNode
from .FuncNode import FuncNode
from .CharNode import CharNode
from .TerNode import TerNode
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
        # ret i32 %6 | ret i32 0 | ret void
        ll = []
        type = self.getType()
        var = ""
        lit = True

        node = self.child

        # IntNode, FloatNode, CharNode
        if isinstance(node, TerNode):
            typVal = node.toLLVM()
            type = typVal[0]
            var = typVal[1]
            return [LLVM.Return(typVal[0], typVal[1], True)]
        # funcNodes, addNodes, varNodes,...
        else:
            ll += node.toLLVM(True)
            lit = False

            # reference
            if ll == []:
                var = node.value
            else:
                var = ll[-1].result

        ret = LLVM.Return(type, var, lit)
        ll += [ret]
        return ll
