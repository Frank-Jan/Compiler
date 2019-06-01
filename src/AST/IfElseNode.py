from .ASTNode import ASTNode, varGen
from .TerNode import TerNode
from .CondExpNode import CondExpNode
from .FuncStatNode import FuncStatNode
from .ReturnStatNode import ReturnStatNode
from .CodeBlockNode import CodeBlockNode
from src.SymbolTable import SymbolTable
import src.llvm.LLVM as LLVM



class IfElseNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'IfElse', maxChildren, ast)
        self.cond = None
        self.ifBlock = None
        self.elseBlock = None
        self.returnStatements = []
        self.endCode = False  # if code behind the while loop is reachable

    def simplify(self, scope):
        toDelete = []
        newChildren = []
        isIfBlock = True
        ifBlockEndCode = False
        elseBlockEndCode = False
        for c in self.children:
            if isinstance(c, TerNode):
                if c.value == "else":
                    isIfBlock = False
                toDelete.append(c)
            if isinstance(c, CondExpNode):
                self.cond = c.simplify(scope)
                newChildren.append(c)
            if isinstance(c, FuncStatNode):
                localScope = SymbolTable(scope)
                tmp = c.simplify(localScope)
                if isIfBlock:
                    self.ifBlock = tmp
                    ifBlockEndCode = isinstance(tmp, ReturnStatNode)
                else:
                    self.elseBlock = tmp
                    elseBlockEndCode = isinstance(tmp, ReturnStatNode)
                if tmp is not c:
                    self.AST.delNode(c)
                newChildren.append(tmp)
            if isinstance(c, CodeBlockNode):
                if isIfBlock:
                    self.ifBlock = c
                    localScope = SymbolTable(scope)
                    self.returnStatements.extend(c.simplify(localScope))
                    ifBlockEndCode = self.ifBlock.endCode
                else:
                    self.elseBlock = c
                    localScope = SymbolTable(scope)
                    self.returnStatements.extend(c.simplify(localScope))
                    elseBlockEndCode = self.elseBlock.endCode
                newChildren.append(c)

        self.children = newChildren
        for c in toDelete:
            self.AST.delNode(c)
        self.endCode = (ifBlockEndCode and elseBlockEndCode)
        return self

    def printLLVM(self):
        code = ""
        code += self.cond.printLLVM()
        lbl1 = varGen.getNewLabel(varGen)
        lbl2 = varGen.getNewLabel(varGen)
        code += "br i1 " + self.cond.returnVar + ", label %" + lbl1 + ", label %" + lbl2 + "\n"  # br i1 %6, label %label1, label %label2

        code += lbl1 + ":\n" + self.ifBlock.printLLVM() + ""

        el = ""
        if self.elseBlock is not None:
            el = self.elseBlock.printLLVM()
        code += "br label %" + lbl2 + "\n"
        code += lbl2 + ":\n" + el

        return code

    def toLLVM(self):

        label1 = LLVM.Label()
        label2 = LLVM.Label()
        label3 = LLVM.Label()

        ll = self.cond.toLLVM()
        icmp = ll[-1]
        condBranch = LLVM.Branch(label1, label2, icmp.result)

        ifstats = self.ifBlock.toLLVM()
        ifBranch = LLVM.Branch(label3)

        elstats = []
        if self.elseBlock is not None:
            elstats += self.elseBlock.toLLVM()
        elseBranch = LLVM.Branch(label3)

        return ll + [condBranch, label1] + ifstats + [ifBranch, label2] + elstats + [elseBranch, label3]