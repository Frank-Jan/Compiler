from .ASTNode import ASTNode, varGen
from .CodeBlockNode import CodeBlockNode
from src.SymbolTable import SymbolTable
import src.llvm.LLVM as LLVM


class WhileNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'While', maxChildren, ast)
        self.cond = None
        self.block = None  # will be CodeblockNode or FuncStatNode
        self.returnStatements = []
        self.endCode = False  # if code behind the while loop is reachable

    def simplify(self, scope):
        self.cond = self.children[2].simplify(scope)
        self.block = self.children[4]  # codeblock or functionstatement
        localScope = SymbolTable(scope)
        if isinstance(self.block, CodeBlockNode):
            self.returnStatements = self.block.simplify(localScope)
            self.endCode = self.block.endCode
        else:
            raise Exception(str(self.pos[0]) + ":" + str(self.pos[1]) + "Forgot something in while simplify: " + str(
                type(self.block)))

        self.AST.delNode(self.children[0])
        self.AST.delNode(self.children[1])
        self.AST.delNode(self.children[3])
        del self.children[3]
        del self.children[1]
        del self.children[0]
        return self

    def printLLVM(self):
        lbl1 = varGen.getNewLabel(varGen)
        lbl2 = varGen.getNewLabel(varGen)
        lbl3 = varGen.getNewLabel(varGen)
        code = ""
        code += "br label %" + lbl3 + "\n"
        code += lbl3 + ":\n"
        code += self.cond.printLLVM()
        code += "br i1 " + self.cond.returnVar + ", label %" + lbl1 + ", label %" + lbl2 + "\n\n"  # br i1 %6, label %label1, label %label2

        code += lbl1 + ":\n" + self.block.printLLVM() + "\n"
        code += "br label %" + lbl3 + "\n"
        code += lbl2 + ":\n"

        return code

    def toLLVM(self):

        label1 = LLVM.Label()
        label2 = LLVM.Label()
        label3 = LLVM.Label()

        firstBranch = LLVM.Branch(label1)

        ll = self.cond.toLLVM()
        icmp = ll[-1]
        condBranch = LLVM.Branch(label2, label3, icmp.result)

        stats = self.block.toLLVM()
        backBranch = LLVM.Branch(label1)

        return [firstBranch, label1] + ll + [condBranch, label2] + stats + [backBranch, label3]
