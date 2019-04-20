import copy
from src.types import *
from src.SymbolTable import SymbolTable

llvmTypes = {'int': 'i32',
             'double': 'double'
             }

counter = 0;

class Type:
    # for nodes who have a type/return type
    def __init__(self, type):
        self.type = type

    def getType(self):
        return self.type  # returns full type (i.e. int ** or char)

    def setType(self, childType):
        self.type = childType


class ASTNode:

    def __init__(self, value, maxChildren, ast):
        self.value = value  # waarde van de node
        self.parent = None  # tupel of parent node and position
        self.children = []  # children
        self.maxChildren = maxChildren  # max aantal children
        self.AST = ast
        self.id = 0
        for i in range(self.maxChildren):
            self.children.append(None)

    def __str__(self):
        return str(self.value) + "  [" + str(self.id) + "]"  # \nNrChildren: " + str(self.maxChildren)

    def isRoot(self):
        return self.value == "Root"

    def isLeaf(self):
        return len(self.children) == 0

    def hasMaxChildren(self):
        count = 0
        for child in self.children:
            if child is not None:
                count += 1
        return self.maxChildren == count

    def timeToSimplify(self):
        for node in self.children:
            if not node.isSimplified:
                return False
        return True

    def toLLVM(self):
        if len(self.children) == 0:
            print("TO DO LLVM: " + str(type(self)))

        code = ""
        for child in self.children:
            code += child.toLLVM()  # + "\n"
        return code

    def simplify(self):
        # Base simplify will only call simplify() on all children
        print("Base simplify for: ", type(self))
        for child in self.children:
            child.simplify()

    def getSymbolTable(self):
        return self.parent.getSymbolTable()

    def fillSymbolTable(self):
        for c in self.children:
            c.fillSymbolTable()


class ScopeNode(ASTNode):
    def __init__(self, value, maxChildren, ast):
        ASTNode.__init__(self, value, maxChildren, ast)
        self.symbolTable = None

    def getSymbolTable(self):
        if self.symbolTable is None:
            self.symbolTable = SymbolTable()
        return self.symbolTable

    def setParent(self, parentScope):
        self.symbolTable.parent = parentScope

    def fillSymbolTable(self):
        if self.parent is None:
            # create new scope
            self.symbolTable = SymbolTable()
        else:
            # create symboltable with parent symboltable
            self.symbolTable = SymbolTable(self.parent.getSymbolTable())
        for c in self.children:
            c.fillSymbolTable(self.symbolTable)


class GenStatNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenStat', maxChildren, ast)

    def simplify(self):
        # only children need to simplify
        for child in self.children:
            child.simplify()


class AssignNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Assign', maxChildren, ast)
        self.left = None  # right node
        self.right = None  # left node

    def simplify(self):
        print("Simplify AssignNode")
        if len(self.children) != 2:
            printError("AssignNode doesn't have 2 children: ", len(self.children))
        self.left = self.children[0].simplify()
        self.right = self.children[1].simplify()  # assignRight wil return funcNode or ...
        self.AST.delNode(self.children[0])
        self.AST.delNode(self.children[1])
        self.children[0] = self.left
        self.children[1] = self.right
        self.left.parent = self
        self.right.parent = self
        return self


class AssignRightNode(ASTNode, Type):

    def __init__(self, ast):
        ASTNode.__init__(self, 'Assign', 2, ast)  # always 2 children
        Type.__init__(self, VOID())

    def getType(self):
        return self.type  # returns full type (i.e. int ** or char)

    def setType(self, childType):
        self.type = childType

    def simplify(self):
        print("Simplify AssignRightNode")
        node = self.children[1].simplify()
        self.setType(node.getType())
        if node is not self.children[1]:
            self.AST.delNode(self.children[1])
        self.AST.delNode(self.children[0])
        self.children = []
        return node


class FuncDefNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncDef', maxChildren, ast)
        Type.__init__(self, INT())  # default return value of a function is integer
        self.fsign = None  # function signature
        self.block = None  # easy acces to code block
        self.returnTypes = []

    def getName(self):
        return self.name

    def setType(self, type):  # set return type
        self.type = type

    def simplify(self):
        print("Simplify: FuncDefNode")
        if isinstance(self.children[0], TerNode):
            # TerNode will have void as value
            self.setType(VOID())
        else:
            self.setType(self.children[0].simplify())  # first child is TypeSpecNode
        self.children[1].simplify()  # simplify funcSign
        self.returnTypes = self.children[2].simplify()  # simplify code block
        self.fsign = self.children[1]
        self.block = self.children[2]

    def fillSymbolTable(self):
        scope = self.children[2].getSymbolTable()


    def toLLVM(self):
        curCode = "define " + llvmTypes[str(self.getType())] + " @" + self.fsign.toLLVM() + "{"
        curCode += self.block.toLLVM()
        curCode += "}"
        return curCode


class FuncSignNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncSign', maxChildren, ast)
        self.name = None  # name
        self.types = []  # arguments

    def simplify(self):
        print("Simplify FuncSignNode")
        self.name = self.children[0].value  # function name
        toDelete = []  # delete useless Ternodes ('(' ')' ',' variable)
        for c in self.children[1:]:
            if isinstance(c, TypeSpecFuncNode):
                self.types.append(c.simplify())
            else:
                toDelete.append(c)
        args = '('
        for i in self.types:
            args += str(i)
        args += ')'
        for d in toDelete:
            self.AST.delNode(d)
            self.children.remove(d)
        return self

    def toLLVM(self):
        args = ""
        for type in self.types:
            args += type.toLLVM() + ", "
        args = args[:-2]
        curCode = self.name + "(" + args + ")"
        return curCode


class FuncSignDefNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncSign', maxChildren, ast)
        self.name = None  # name
        self.types = []  # arguments Types
        self.varNames = []  # VarNodes itself (not strings)

    def simplify(self):
        print("Simplify FuncSignDefNode")
        self.children[0].simplify()
        self.name = self.children[0].value  # function name
        toDelete = []  # delete useless Ternodes ('(' ')' ',' variable)
        for c in self.children[1:]:
            if isinstance(c, TypeSpecFuncNode):
                self.types.append(c.simplify())
            elif isinstance(c, VarNode):
                self.varNames.append(c)
            else:
                toDelete.append(c)
        sign = '('
        for i in range(len(self.types)):
            sign += str(self.types[i]) + " " + str(self.varNames[i]) + ", "
        sign += ')'
        for d in toDelete:
            self.AST.delNode(d)
            self.children.remove(d)
        return self

    def toLLVM(self):
        args = ""
        for i in range(len(self.types)):
            args += self.types[i].toLLVM()
            args += " " + self.varNames[i].toLLVM() + ", "
        args = args[:-2]
        curCode = self.name + "(" + args + ")"
        return curCode


class CodeBlockNode(ScopeNode):

    def __init__(self, maxChildren, ast, symboltable=None):
        ASTNode.__init__(self, 'CodeBlock', maxChildren, ast)
        self.returnStatements = []  # full return statements

    def simplify(self):
        print("Simplify Codeblock")
        funcSyntax = self.children[1]
        funcSyntax.simplify()
        self.returnStatements += funcSyntax.returnStatements

        # delete first and last node ('{' and '}')
        self.AST.delNode(self.children[2])
        self.AST.delNode(self.children[0])
        del self.children[2]
        del self.children[0]

        # steal children of funcSyntax
        self.children = funcSyntax.children
        for c in self.children:
            c.parent = self
            print("\t", type(c), " ", len(c.children))
        funcSyntax.children = []
        self.AST.delNode(funcSyntax)

        return self.returnStatements  # simplify FuncSyntax node and return return statements

    def getSymbolTable(self):
        return self.symboltable

    def toLLVM(self):
        code = "\n"
        for child in self.children:
             code += child.toLLVM() + "\n"
        return code


class ValueNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Value', maxChildren, ast)

    def simplify(self):
        print("Simplify ValueNode")
        retNode = self.children[0].simplify()
        self.AST.delNode(self.children[0])
        self.children = []
        return retNode


class LvalueNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Lvalue', maxChildren, ast)

    def simplify(self):
        print("Simplify LvalueNode")
        if len(self.children) == 1:
            retNode = self.children[0].simplify()
        elif len(self.children) == 2:
            retNode = self.children[1].simplify()
            if not isinstance(retNode.getType(), POINTER):
                printError("error: dereferencing non-pointer")
                return None
            retNode.type = retNode.getType().getBase()
        else:
            retNode = self.children[2].simplify()   #* and & cancel eachother in '*&'

        self.children.remove(retNode)
        for c in self.children:
            self.AST.delNode(c)
        self.children = []

        return retNode


class RvalueNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Rvalue', maxChildren, ast)

    def simplify(self):
        print("Simplify RvalueNode")
        retNode = None
        if len(self.children) == 1:
            if isinstance(self.children[0], ArOpNode):
                printError("ArOpNode simplify not yet implemented: returning VOID type")
                return None
            retNode = self.children[0].simplify()
        elif len(self.children) == 2:
            retNode = self.children[1].simplify() #simplify lvalue node
            retNode.type = POINTER(retNode.getType())
        else:
            printError("error: unexpected number of children (", len(self.children) ,") in: ", type(RvalueNode))
            retNode = None

        if retNode in self.children:
            self.children.remove(retNode)
        for c in self.children:
            self.AST.delNode(c)
        self.children = []

        return retNode


class FuncSyntaxNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncSyntax', maxChildren, ast)
        self.returnStatements = []
    def simplify(self):
        print("Simplify FuncSyntaxNode")
        new_children = []
        for c in self.children:
            if isinstance(c, FuncStatNode):
                new_children.append(c.simplify())
                self.AST.delNode(c)
                pass
            elif isinstance(c, CodeBlockNode):
                self.returnStatements += c.simplify()
                new_children.append(c)
            elif isinstance(c, LoopNode):
                print("LOOP NODE SIMPLIFY NOT YET IMPLEMENTED")
                new_children.append(c)
        self.children = new_children
        return self
        # self.isSimplified = True
        #
        # for i in range(len(self.children)):
        #     self.children[i].parent = self.parent
        #     if i == 0:
        #         self.parent[0].children[self.parent[1]] = self.children[i]
        #     else:
        #         self.parent[0].children.insert(self.parent[1] + i, self.children[i])
        # self.AST.delNode(self)


class FuncStatNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncStat', maxChildren, ast)

    def simplify(self):
        print("Simplify FuncStatNode")
        if isinstance(self.children[0], VarNode) or isinstance(self.children[0], LitNode):
            # print("")
            self.AST.delNode(self.children[0])
            del self.children[0]
            return None
        ret = self.children[0].simplify()
        del self.children[0]
        return ret


class ArOpNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'ArOp', maxChildren, ast)

    def simplify(self):
        return self
    # ASTNode.simplify(self)
    # self.isSimplified = True
    # val = ""
    # getal = 0
    # for node in self.children:
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
    # self.children = []
    # self.maxChildren = 0
    # self.value = val


class ProdNode(ArOpNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Prod', maxChildren, ast)
        self.left = None
        self.right = None

    def simplify(self):
        self.isSimplified = True
        if self.maxChildren == 1:
            ASTNode.simplify(self)
        else:
            val = ""
            getal = 0
            for node in self.children:
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
                        self.maxChildren -= 1
                        self.children.remove(node)
                else:
                    print("oei, iets vergeten simply_prod: ", type(node))
                getal += 1

            self.value = val


class AddNode(ArOpNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Add', maxChildren, ast)
        self.left = None
        self.right = None

    def simplify(self):
        self.isSimplified = True
        if self.maxChildren == 1:
            ASTNode.simplify(self)
        else:
            val = ""
            getal = 0
            kopie = copy.copy(self.children)
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
                        self.maxChildren -= 1
                        self.children.remove(node)
                else:
                    print("oei, iets vergeten: simply_add ", type(node))
                getal += 1

            self.value = val


class IdentNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Ident', maxChildren, ast)


class AtomNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Atom', maxChildren, ast)

    def simplify(self):
        self.isSimplified = True
        if self.maxChildren == 1:
            ASTNode.simplify(self)
        elif self.maxChildren == 3:
            haakje1 = self.children[0]
            haakje2 = self.children[2]
            self.children.remove(haakje1)
            self.children.remove(haakje2)
            self.AST.delNode(haakje1)
            self.AST.delNode(haakje2)
            self.maxChildren = 1
            ASTNode.simplify(self)
        else:
            print("oei, iets vergeten bij AtomNode")


class ReturnStatNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'ReturnStat', maxChildren, ast)
        Type.__init__(self, VOID())
        self.returnVal = None

    def simplify(self):
        self.AST.delNode(self.children[0])  # del return TerNode
        del self.children[0]
        if len(self.children) == 0:
            self.setType(VOID())  # no return value
        else:
            node = self.children[0].simplify()
            if isinstance(self.children[0], FuncNode) or isinstance(self.children[0], ArOpNode):
                self.type = None
            # can't take type because a function's output might be returned
            if isinstance(node, IntNode) or isinstance(node, FloatNode) or isinstance(node, CharNode):
                self.AST.delNode(self.children[0])
                del self.children[0]
                self.children.append(node)
        print("Simplify returnStatNode: ", self.getType())
        return self


class VarDefNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'VarDef', maxChildren, ast)

    def simplify(self):
        print("Simplify vardefnode")

        self.children[0].simplify()  # VarDeclNode
        node = self.children[1].simplify()  # AssignRightNode
        self.AST.delNode(self.children[1])
        self.children[1] = node
        return self


class GenDefNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenDef', maxChildren, ast)

    def simplify(self):
        print("Simplify GenDefNode")
        self.children[0].simplify()


class VarDeclNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'VarDecl', maxChildren, ast)
        self.type = None  #Types
        self.var = None   #VarNode itself
        self.size = 0

    def simplify(self):
        print("SIMPLIFY: VarDeclNode")
        if len(self.children) == 2:
            # no array
            self.size = 1
            self.type = self.children[0].simplify()
            self.var = self.children[1]
        else:
            self.size = self.children[3].value
            self.type = self.children[0].simplify()
            self.var = self.children[1]
            self.AST.delNode(self.children[2])  # '('
            self.AST.delNode(self.children[3])  # DIGIT
            self.AST.delNode(self.children[4])  # ')'

        self.AST.delNode(self.children[0])
        self.AST.delNode(self.children[1])
        self.children = []
        self.value = str(self.type) + " " + str(self.var)
        return self

    def toLLVM(self):
        print("VARDECL to LLVM")
        return self.type.toLLVM() + " " + self.var.toLLVM()

class FuncNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Func', maxChildren, ast)
        self.name = None
        self.arguments = []

    def getType(self):
        return VOID()

    def getName(self):
        return self.name

    def simplify(self):
        print("Simplify FuncNode")
        self.children[0].simplify()
        self.name = self.children[0].value
        for c in self.children[1:]:
            if isinstance(c,ValueNode):
                self.arguments.append(c.simplify())

        toDelete = [item for item in self.children[1:] if item not in self.arguments]
        for c in toDelete:
            self.AST.delNode(c)
        self.children = [self.children[0]]
        self.children += self.arguments
        return self


class GenDeclNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenDecl', maxChildren, ast)

    def simplify(self):
        # only children need to simplify
        print("Simplifying declare node")
        for child in self.children:
            child.simplify()
        self.isSimplified = True



class FuncDeclNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncDecl', maxChildren, ast)
        self.fsign = None

    def setType(self, type):  # set return type
        self.type = type

    def simplify(self):
        if isinstance(self.children[0], TerNode):
            # TerNode will have void as value
            self.setType(VOID())
        else:
            self.setType(self.children[0].simplify())  # first child is TypeSpecNode
        self.children[1].simplify()  # simplify funcSign
        self.fsign = self.children[1]
        return self

    def toLLVM(self):
        curCode = "declare " + self.type.toLLVM() + " @" + self.fsign.toLLVM()
        return curCode


class CondExpNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'CondExp', maxChildren, ast)
        self.left = None
        self.right = None

    def simplify(self):
        self.isSimplified = True
        val = ""
        getal = 0
        for node in self.children:
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
            self.children.remove(node)

        self.maxChildren = len(self.children)
        self.value = val


class LoopNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'LoopNode', maxChildren, ast)


class WhileNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'While', maxChildren, ast)
        self.cond = None
        self.block = None

    def simplify(self):
        self.isSimplified = True
        val = "While"
        getal = 0
        kopie = copy.copy(self.children)
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
            self.children.remove(node)

        self.maxChildren = len(self.children)
        self.value = val


class IfElseNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'IfElse', maxChildren, ast)
        self.cond = None
        self.ifBlock = None
        self.elseBlock = None

    def simplify(self):
        self.isSimplified = True
        val = "If()Else"
        getal = 0
        kopie = copy.copy(self.children)
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
            self.children.remove(node)

        self.maxChildren = len(self.children)
        self.value = val


# CHILDREN THAT ARE NOT PARENTS = LEAFS
class TerNode(ASTNode):  # leafs

    def __init__(self, value, ast, pos):
        ASTNode.__init__(self, value, 0, ast)
        self.child = True
        self.pos = pos

    def simplify(self):
        print("Simplify TerNode: ", self.value)
        return self.value


class VarNode(ASTNode):

    def __init__(self, value, ast, pos):
        # TerNode.__init__(self, value, ast, pos)
        ASTNode.__init__(self, value, 1, ast)

    def getName(self):
        return self.name

    def getType(self):
        return VOID()

    def simplify(self):
        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        return self
        # self.isSimplified = True
        # print("SIMPLIFY:")
        # print("\t", self.name)
        # print("\tchildren:")
        # for c in self.children:
        #     print("\t\t", c, "/", c.value)
        # self.name = self.children[0].value
        # self.AST.delNode(self.children[0])
        # self.children[0].parent = self.parent
        # self.parent[0].children[self.parent[1]] = self.children[0]
        # self.AST.delNode(self)

    def toLLVM(self):
        return "%" + self.value

class LitNode(ASTNode, Type):

    def __init__(self, maxChildren, ast, _type=VOID()):
        ASTNode.__init__(self, "LIT", maxChildren, ast)
        Type.__init__(self, _type)

    def getValue(self):
        return self.value

    def simplify(self):
        print("Simplify LitNode")
        retNode = self.children[0].simplify()
        self.value = self.children[0].value
        self.setType(self.children[0].getType())
        self.children.remove(retNode)
        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        return retNode

    # def toLLVM(self):
    #     print("LITNODE to LLVM")
    #     return self.type.toLLVM() + " " + self.value


class IntNode(TerNode, Type):

    def __init__(self, value, ast, pos):
        Type.__init__(self, INT())
        TerNode.__init__(self, value, ast, pos)

    def simplify(self):
        print("Simplify IntNode: ", self.value)
        toDelete = self.children
        for c in toDelete:
            self.AST.delNode(c)
        self.children = []
        return self


class FloatNode(TerNode, Type):

    def __init__(self, value, ast, pos):
        Type.__init__(self, FLOAT())
        TerNode.__init__(self, value, ast, pos)

    def simplify(self):
        print("Simplify FloatNode: ", self.value)
        toDelete = self.children
        for c in toDelete:
            self.AST.delNode(c)
        self.children = []
        return self

class CharNode(TerNode, Type):

    def __init__(self, value, ast, pos):
        Type.__init__(self, CHAR())
        TerNode.__init__(self, value, ast, pos)

    def simplify(self):
        print("Simplify CharNode: ", self.value)
        toDelete = self.children
        for c in toDelete:
            self.AST.delNode(c)
        self.children = []
        return self

# type/pointer/reference/literal nodes

class TypeSpecNode(Type, ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'TypeSpecNode', maxChildren, ast)
        Type.__init__(self, VOID())

    def setType(self, childType):
        self.type = childType

    def simplify(self):
        type = self.children[0].simplify()
        self.setType(type)
        print("Simplified TypeSpecNode to: ", self.getType())
        self.AST.delNode(self.children[0])
        self.children = []
        self.value = self.type
        return self.getType()


class TypeSpecFuncNode(Type, ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'TypeSpecFunc', maxChildren, ast)
        Type.__init__(self, VOID())

    def setType(self, childType):
        self.type = childType

    def simplify(self):
        # self.isSimplified = True
        self.setType(self.children[0].simplify())
        self.value = self.type
        self.AST.delNode(self.children[0])
        self.children = []
        print("Simplified TypeSpecFuncNode to: ", self.getType())
        return self.getType()
        # self.AST.delNode(self.children[0])
        # self.children = None


class TypeSpecBaseNode(Type, ASTNode):

    def __init__(self, value, maxChildren, ast):
        ASTNode.__init__(self, 'TypeSpecBaseNode', maxChildren, ast)
        Type.__init__(self, VOID())

    def setType(self, childType):
        self.type = childType

    def simplify(self):
        print("Simplify TypeSpecBaseNode")
        self.type = toType(self.children[0].value)
        self.AST.delNode(self.children[0])
        self.children = []
        print("Simplified TypeSpecBaseNode to: ", self.getType())
        self.value = self.getType()
        return self.getType()
        # self.isSimplified = True
        # self.setType(toType(self.children[0]))
        # self.AST.delNode(self.children[0])
        # self.children = None


class TypeSpecReferenceNode(Type, ASTNode):

    def __init__(self, value, maxChildren, ast):
        ASTNode.__init__(self, 'TypeSpecRef', maxChildren, ast)
        Type.__init__(self, VOID())

    def getType(self):
        return self.type

    def setType(self, childType):
        self.type = REFERENCE(childType)

    def simplify(self):
        self.setType(self.children[0].simplify())
        print("Simplified TypeSpecReferenceNode to: ", self.getType())
        self.value = self.getType()
        return self.getType()


class TypeSpecPtrNode(Type, ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'TypeSpecPtr', maxChildren, ast)
        Type.__init__(self, POINTER())

    def setType(self, childType):
        self.type = POINTER(childType)

    def simplify(self):
        if isinstance(self.children[0], TerNode):
            # first child is 'void'
            self.setType(VOID())
        else:
            self.setType(self.children[0].simplify())  # first child is the type
            # second child holds "*"
        return self.type

