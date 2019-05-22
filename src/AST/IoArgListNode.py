from .ASTNode import ASTNode, varGen
from .TerNode import TerNode
from .ValueNode import ValueNode
from .VarNode import VarNode
#from .FuncNode import FuncNode
from .Type import POINTER, CHAR, FLOAT
from .Types import llvmTypes


class IoArgListNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'IoArgList', maxChildren, ast)
        self.returnVars = {}

    def simplify(self, scope):
        newChildren = []
        toDelete = []
        for c in self.children:
            if isinstance(c, TerNode):
                toDelete.append(c)
            elif isinstance(c, ValueNode):
                retnode = c.simplify(scope)
                if retnode is not c:
                    self.AST.delNode(c)
                newChildren.append(retnode)
            elif isinstance(c, IoArgListNode):
                #steal children
                c.simplify(scope)
                newChildren.extend(c.stealChildren())
                toDelete.append(c)
            else:
                raise "IoArgListNode: unexpected node: {}".format(type(c))

        self.children = newChildren
        for d in toDelete:
            self.AST.delNode(d)
        return self

    def getInputTypes(self):
        pass

    def printLLVM(self, cast = False):
        code = ""
        if cast:
            for c in self.children:
                if isinstance(c, VarNode): # or isinstance(c, FuncNode)
                    code += c.printLLVM(True)
                    type = c.getType()
                    if isinstance(type, POINTER):
                        for niv in range(c.deref-1):
                            type = type.getBase()
                    if isinstance(type, CHAR):
                        self.returnVars[c] = varGen.getNewVar(varGen)
                        code += self.returnVars[c] + " = sext " + llvmTypes[str(c.returnType)] +" "+ c.returnVar + " to i32\n" #  %4 = sext i8 %3 to i32
                    elif isinstance(type, FLOAT):
                        self.returnVars[c] = varGen.getNewVar(varGen)
                        code += self.returnVars[c] + " = fpext " + llvmTypes[str(c.returnType)] +" "+ c.returnVar + " to double\n"# %7 = fpext float %6 to double
                    else:
                        self.returnVars[c] = c.returnVar
        else:
            #i32 %5, double %7, i32 99
            for i in range(len(self.children)):
                if isinstance(self.children[i], VarNode): # or isinstance(self.children[i], FuncNode):
                    if isinstance(self.children[i].getType(), FLOAT):
                        code += ", double " + self.returnVars[self.children[i]]
                    else:
                        code += ", i32 " + self.returnVars[self.children[i]]
                else:
                    if isinstance(self.children[i].getType(), FLOAT):
                        code += ", double " + self.children[i].printLLVM(True)
                    else:
                        code += ", i32 " + self.children[i].printLLVM(True)
        return code
