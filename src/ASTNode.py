import copy
from src.types import *


class ASTNode:

    def __init__(self, value, size, ast):
        self.value = value
        self.parent = None  # tupel of parent node and position
        self.nextNodes = []
        self.size = size
        self.AST = ast
        self.id = 0
        self.simplified = False
        for i in range(self.size):
            self.nextNodes.append(None)

    def __str__(self):
        return str(self.value) + "  [" + str(self.id) + "]"  # \nNrChildren: " + str(self.size)

    def isRoot(self):
        return self.value == "Root"

    def isChild(self):
        return self.size == 0

    def hasMaxChildren(self):
        count = 0
        for child in self.nextNodes:
            if child != None:
                count += 1
        return self.size == count

    def timeToSimplify(self):
        for node in self.nextNodes:
            if not node.simplified:
                return False
        return True

    def simplify(self):
        self.simplified = True

        if self.parent == None or self.size == 0:
            return
        elif self.size == 2:
            self.AST.delNode(self.nextNodes[1])
        elif self.size > 2:
            print("Say whut?!")

        self.nextNodes[0].parent = self.parent
        self.parent[0].nextNodes[self.parent[1]] = self.nextNodes[0]
        self.AST.delNode(self)


class GenStatNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'GenStat', size, ast)


class AssignNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'Assign', size, ast)
        self.var = None
        self.ter = None

    def simplify(self):
        self.simplified = True
        val = ""
        for node in self.nextNodes:
            if isinstance(node, VarNode):
                self.var = node
            elif isinstance(node, TerNode):
                self.ter = node
                val += node.value + " "
                self.AST.delNode(node)
                self.size -= 1
                self.nextNodes.remove(node)
            elif isinstance(node, ArOpNode):
                pass
            else:
                print("oei, iets vergeten: ", type(node))

        self.value = val


class FuncDefNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'FuncDef', size, ast)
        self.returnType = None
        self.types = []
        self.vars = []
        self.args = []  # self.vars en self.types combined in tuples
        self.block = None  # returnstats in dit block
        self.name = None

    def simplify(self):
        self.simplified = True
        val = ""
        getal = 0
        for node in self.nextNodes:
            if isinstance(node, TypeSpecBaseNode) or isinstance(node, TypeSpecPtrNode):
                if getal == 0:
                    self.returnType = node
                else:
                    self.types.append(node.value)
                    self.args.append([node.value, None])
            elif isinstance(node, VarNode):
                self.vars.append(node.value)
                self.args[-1][1] = node.value
            elif isinstance(node, CodeBlockNode):
                self.block = node
                continue
            elif isinstance(node, TerNode):
                if getal == 0:
                    self.returnType = node
                elif getal == 1:
                    self.name = node
                else:
                    print("node ", node, " gedropped")
            else:
                print("oei, iets vergeten: ", type(node))
            getal += 1
            val += node.value + " "
            self.AST.delNode(node)

        self.nextNodes = [self.nextNodes.pop()]
        self.size = 1
        self.value = val


class FuncSignNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'FuncSign', size, ast)
        self.name = None
        self.types = []
        self.vars = []

    def simplify(self):
        self.simplified = True
        val = ""
        getal = 0
        for node in self.nextNodes:
            if isinstance(node, TypeSpecBaseNode) or isinstance(node, TypeSpecPtrNode):
                self.types.append(node.value)
            elif isinstance(node, VarNode):
                self.vars.append(node.value)
            elif isinstance(node, IdentNode):
                self.id = node
            elif isinstance(node, TerNode):
                if getal == 0:
                    getal += 1
                    self.name = node
                else:
                    print("node ", node, " gedropped")
            else:
                print("oei, iets vergeten: ", type(node))
            val += node.value + " "
            self.AST.delNode(node)

        self.nextNodes = []
        self.size = 0
        self.value = val


class CodeBlockNode(ASTNode):

    def __init__(self, size, ast, symboltable=None):
        ASTNode.__init__(self, 'CodeBlock', size, ast)
        self.symboltable = symboltable
        self.scopeCounter = None
        self.returnStats = []  # full return statements

    def simplify(self):
        self.simplified = True
        kopie = copy.copy(self.nextNodes)
        for node in kopie:
            if isinstance(node, ReturnStatNode):
                self.returnStats.append(node)
            elif isinstance(node, CodeBlockNode):
                self.returnStats += node.returnStats
            elif isinstance(node, TerNode):
                print("node ", node, " gedropped")
                self.AST.delNode(node)
                self.nextNodes.remove(node)
        self.size = len(self.nextNodes)
        self.scopeCounter = self.size + 1

    def getSymbolTable(self):
        return self.symboltable


class FuncSyntaxNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'FuncSyntax', size, ast)

    def simplify(self):
        self.simplified = True

        for i in range(len(self.nextNodes)):
            self.nextNodes[i].parent = self.parent
            if i == 0:
                self.parent[0].nextNodes[self.parent[1]] = self.nextNodes[i]
            else:
                self.parent[0].nextNodes.insert(self.parent[1] + i, self.nextNodes[i])
        self.AST.delNode(self)


class FuncStatNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'FuncStat', size, ast)


class ArOpNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'ArOp', size, ast)

    def simplify(self):
        ASTNode.simplify(self)
        # self.simplified = True
        # val = ""
        # getal = 0
        # for node in self.nextNodes:
        #     if isinstance(node, TypeSpecBaseNode):
        #         self.type = node
        #     elif isinstance(node, VarNode):
        #         self.var = node
        #     elif isinstance(node, IdentNode):
        #         self.id = node
        #     elif isinstance(node, AddNode):
        #         self.
        #     elif isinstance(node, TerNode):
        #         if getal == 0:
        #             getal += 1
        #             self.name = node
        #         else:
        #             print("node ", node, " gedropped")
        #     else:
        #         print("oei, iets vergeten")
        #     val += node.value + " "
        #     self.AST.delNode(node)
        #
        # self.nextNodes = []
        # self.size = 0
        # self.value = val


class ProdNode(ArOpNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'Prod', size, ast)
        self.left = None
        self.right = None

    def simplify(self):
        self.simplified = True
        if self.size == 1:
            ASTNode.simplify(self)
        else:
            val = ""
            getal = 0
            for node in self.nextNodes:
                if getal == 0:
                    if isinstance(node, IntNode):
                        self.left = node
                elif getal == 2:
                    if isinstance(node, IntNode):
                        self.right = node
                elif getal == 1:
                    if isinstance(node, TerNode):
                        val += node.value + " "
                        self.AST.delNode(node)
                        self.size -= 1
                        self.nextNodes.remove(node)
                else:
                    print("oei, iets vergeten: ", type(node))
                getal += 1

            self.value = val


class AddNode(ArOpNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'Add', size, ast)
        self.left = None
        self.right = None

    def simplify(self):
        self.simplified = True
        if self.size == 1:
            ASTNode.simplify(self)
        else:
            val = ""
            getal = 0
            kopie = copy.copy(self.nextNodes)
            for node in kopie:
                if getal == 0:
                    if isinstance(node, IntNode):
                        self.left = node
                elif getal == 2:
                    if isinstance(node, IntNode):
                        self.right = node
                    elif isinstance(node, ProdNode):
                        self.right = node
                elif getal == 1:
                    if isinstance(node, TerNode):
                        val += node.value + " "
                        self.AST.delNode(node)
                        self.size -= 1
                        self.nextNodes.remove(node)
                else:
                    print("oei, iets vergeten: ", type(node))
                getal += 1

            self.value = val


class IdentNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'Ident', size, ast)


class AtomNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'Atom', size, ast)

    def simplify(self):
        self.simplified = True
        if self.size == 1:
            ASTNode.simplify(self)
        elif self.size == 3:
            haakje1 = self.nextNodes[0]
            haakje2 = self.nextNodes[2]
            self.nextNodes.remove(haakje1)
            self.nextNodes.remove(haakje2)
            self.AST.delNode(haakje1)
            self.AST.delNode(haakje2)
            self.size = 1
            ASTNode.simplify(self)
        else:
            print("oei, iets vergeten bij AtomNode")


class ReturnStatNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'ReturnStat', size, ast)
        self.returnVal = None

    def simplify(self):
        self.simplified = True
        val = ""
        getal = 0
        kopie = copy.copy(self.nextNodes)
        for node in kopie:
            if isinstance(node, VarNode) or isinstance(node, LitNode) or isinstance(node, FuncNode) or isinstance(node, ArOpNode):
                if getal == 1:
                    self.returnVal = node
                continue
            elif isinstance(node, TerNode):
                pass
            else:
                print("oei, iets vergeten bij ReturnStatNode: ", type(node))
            getal += 1
            val += node.value + " "
            self.AST.delNode(node)
            self.nextNodes.remove(node)

        self.size = len(self.nextNodes)
        self.value = val


class VarDefNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'VarDef', size, ast)
        self.type = None
        self.var = None
        self.right = None  # right side of assignment
        self.id = None
        self.ter = None
        self.arop = None  # arithmic operation

    def simplify(self):
        self.simplified = True
        val = ""
        kopie = copy.copy(self.nextNodes)
        getal = 0
        for node in kopie:
            if isinstance(node, TypeSpecBaseNode) or isinstance(node, TypeSpecPtrNode):
                self.type = node
            elif isinstance(node, VarNode):
                if getal == 1:
                    self.var = node
                elif getal > 1:
                    self.right = node
            elif isinstance(node, IdentNode):
                self.id = node
            elif isinstance(node, FuncNode) or isinstance(node, RefNode) \
                    or isinstance(node, DeRefNode) or isinstance(node, TerNode):
                self.right = node
            elif isinstance(node, AddNode):
                self.arop = node
                continue
            else:
                print("oei, iets vergeten: ", type(node))
            val += node.value + " "
            self.AST.delNode(node)
            self.size -= 1
            self.nextNodes.remove(node)
            getal += 1

        self.value = val


class GenDefNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'GenDef', size, ast)


class VarDeclNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'VarDecl', size, ast)
        self.type = None
        self.var = None

    def simplify(self):
        self.simplified = True
        val = ""
        for node in self.nextNodes:
            if isinstance(node, TypeSpecBaseNode) or isinstance(node, TypeSpecPtrNode):
                self.type = node
            elif isinstance(node, VarNode):
                self.var = node
            else:
                print("oei, iets vergeten: ", type(node))
            val += node.value + " "
            self.AST.delNode(node)

        self.nextNodes = []
        self.size = 0
        self.value = val


class FuncNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'Func', size, ast)
        self.name = None
        self.idents = []

    def simplify(self):
        self.simplified = True
        val = ""
        for node in self.nextNodes:
            if isinstance(node, TerNode):
                self.name = node
            elif isinstance(node, IdentNode):
                self.idents.append(node)
            else:
                print("oei, iets vergeten: ", type(node))
            val += node.value + " "
            self.AST.delNode(node)

        self.nextNodes = []
        self.size = 0
        self.value = val


class GenDeclNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'GenDecl', size, ast)


class TypeSpecNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'TypeSpec', size, ast)


class FuncDeclNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'FuncDecl', size, ast)
        self.returnType = None
        self.fsign = None

    def simplify(self):
        self.simplified = True
        val = ""
        for node in self.nextNodes:
            if isinstance(node, TypeSpecPtrNode) or isinstance(node, TypeSpecBaseNode):
                self.returnType = node
            elif isinstance(node, FuncSignNode):
                self.fsign = node
            else:
                print("oei, iets vergeten Bij FuncDeclNode: ", type(node))
            val += node.value + " "
            self.AST.delNode(node)

        self.nextNodes = []
        self.size = 0
        self.value = val


class CondExpNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'CondExp', size, ast)
        self.left = None
        self.right = None

    def simplify(self):
        self.simplified = True
        val = ""
        getal = 0
        for node in self.nextNodes:
            getal += 1
            if isinstance(node, VarNode) or isinstance(node, LitNode) or isinstance(node, ProdNode) or isinstance(node,
                                                                                                                  AddNode):
                if getal == 1:
                    self.left = node
                else:
                    self.right = node
                continue
            elif isinstance(node, TerNode):
                pass
            else:
                print("oei, iets vergeten bij CondExpNode: ", type(node))
            val += node.value + " "
            self.AST.delNode(node)
            self.nextNodes.remove(node)

        self.size = len(self.nextNodes)
        self.value = val


class LoopNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'LoopNode', size, ast)


class WhileNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'While', size, ast)
        self.cond = None
        self.block = None

    def simplify(self):
        self.simplified = True
        val = "While"
        getal = 0
        kopie = copy.copy(self.nextNodes)
        for node in kopie:
            getal += 1
            if isinstance(node, CondExpNode):
                self.cond = node
                continue
            elif isinstance(node, CodeBlockNode):
                self.block = node
                continue
            elif isinstance(node, TerNode):
                print("node ", node, " gedropped")
            else:
                print("oei, iets vergeten bij WhileNode: ", type(node))
            self.AST.delNode(node)
            self.nextNodes.remove(node)

        self.size = len(self.nextNodes)
        self.value = val


class IfElseNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'IfElse', size, ast)
        self.cond = None
        self.ifBlock = None
        self.elseBlock = None

    def simplify(self):
        self.simplified = True
        val = "If()Else"
        getal = 0
        kopie = copy.copy(self.nextNodes)
        for node in kopie:
            getal += 1
            if isinstance(node, CondExpNode):
                self.cond = node
                continue
            elif isinstance(node, CodeBlockNode):
                if getal == 5:
                    self.ifBlock = node
                elif getal == 7:
                    self.elseBlock = node
                else:
                    print("CodeBlock op verkeerde plaats bij IfElseNode")
                continue
            elif isinstance(node, TerNode):
                print("node ", node, " gedropped")
            else:
                print("oei, iets vergeten bij IfElseNode: ", type(node))
            self.AST.delNode(node)
            self.nextNodes.remove(node)

        self.size = len(self.nextNodes)
        self.value = val


class DeRefNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'DeRef', size, ast)
        self.right = None

    def simplify(self):
        self.simplified = True
        val = ""
        for node in self.nextNodes:
            if isinstance(node, VarNode):
                self.var = node
            elif isinstance(node, TerNode):
                pass
            else:
                print("oei, iets vergeten: ", type(node))
            val += node.value
            self.AST.delNode(node)

        self.nextNodes = []
        self.size = 0
        self.value = val


class RefNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'Ref', size, ast)
        self.var = None

    def simplify(self):
        self.simplified = True
        val = ""
        for node in self.nextNodes:
            if isinstance(node, VarNode):
                self.var = node
            elif isinstance(node, TerNode):
                pass
            else:
                print("oei, iets vergeten: ", type(node))
            val += node.value
            self.AST.delNode(node)

        self.nextNodes = []
        self.size = 0
        self.value = val


class TypeSpecPtrNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, 'TypeSpecPtr', size, ast)

    def simplify(self):
        self.simplified = True
        val = ""
        for node in self.nextNodes:
            if isinstance(node, TypeSpecPtrNode):
                pass
            elif isinstance(node, TerNode):
                pass
            else:
                print("oei, iets vergeten")
            val += node.value
            self.AST.delNode(node)

        self.nextNodes = []
        self.size = 0
        self.value = val


# CHILDREN THAT ARE NOT PARENTS = LEAFS
class TerNode(ASTNode):

    def __init__(self, value, ast):
        ASTNode.__init__(self, value, 0, ast)
        self.child = True
        self.simplified = True


class VarNode(TerNode):

    def __init__(self, value, ast):
        TerNode.__init__(self, value, ast)
        self.type = "var"


class TypeSpecBaseNode(TerNode):

    def __init__(self, value, ast):
        TerNode.__init__(self, value, ast)
        self.type = "type"


class LitNode(ASTNode):

    def __init__(self, size, ast):
        ASTNode.__init__(self, "Lit", size, ast)
        self.type = None


class IntNode(LitNode, TerNode):

    def __init__(self, value, ast):
        TerNode.__init__(self, value, ast)
        self.type = INT()


class FloatNode(LitNode, TerNode):

    def __init__(self, value, ast):
        TerNode.__init__(self, value, ast)
        self.type = FLOAT()


class CharNode(LitNode, TerNode):

    def __init__(self, value, ast):
        TerNode.__init__(self, value, ast)
        self.type = CHAR()

# # for symbols as: "=", ";"
# class SymbolNode(ASTNode):
#
#     def __init__(self, value, ast):
#         ASTNode.__init__(self, value, 0, ast)
#         self.child = True
#         self.simplified = True
