import copy
from src.types import *
from src.SymbolTable import SymbolTable

llvmTypes = {'int': 'i32',
             'double': 'double'
             }


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
        for child in self.children:
            child.simplify()

    def getSymbolTable(self):
        return self.parent.getSymbolTable()

    def fillSymbolTable(self):
        for c in self.children:
            c.fillSymbolTable()
        # self.isSimplified = True
        # print("Base simplify: ", type(self))
        # if self.parent == None or self.maxChildren == 0:
        #     return
        # elif self.maxChildren == 2:
        #     self.AST.delNode(self.children[1])
        # elif self.maxChildren > 2:
        #     print("Say whut?!")
        #
        # self.children[0].parent = self.parent
        # self.parent[0].children[self.parent[1]] = self.children[0]
        # self.AST.delNode(self)


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
        if len(self.children) != 2:
            printError("AssignNode doesn't have 2 children: ", len(self.children))
        self.left = self.children[0]
        self.right = self.children[1].simplify()  # assignRight wil return value node
        self.AST.delNode(self.children[1])
        self.children[1] = self.right  # remove old child and replace


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
        self.value = "="
        tmp = self.children[1].simplify()
        if isinstance(type, VOID):
            self.type = tmp
        else:
            self.type = VOID()
        self.AST.delNode(self.children[0])
        del self.children[0]
        return self.type


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
        if isinstance(self.children[0], TerNode):
            # TerNode will have void as value
            self.setType(VOID())
        else:
            self.setType(self.children[0].simplify())  # first child is TypeSpecNode
        self.children[1].simplify()  # simplify funcSign
        self.returnTypes = self.children[2].simplify()  # simplify code block
        self.fsign = self.children[1]
        self.block = self.children[2]
        print("Simplify FuncDefNode: ", self.getType(), " ", self.fsign.name)

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
        print("Simplified FuncSignNode to ", self.name, args)
        for d in toDelete:
            self.AST.delNode(d)
            self.children.remove(d)
        # self.isSimplified = True
        # val = ""
        # getal = 0
        # for node in self.children:
        #     if isinstance(node, TypeSpecBaseNode) or isinstance(node, TypeSpecPtrNode):
        #         self.types.append(node.value)
        #     elif isinstance(node, VarNode):
        #         self.vars.append(node.value)
        #     elif isinstance(node, IdentNode):
        #         self.id = node
        #     elif isinstance(node, TerNode):
        #         if getal == 0:
        #             getal += 1
        #             self.name = node.value
        #         else:
        #             print("node ", node, " gedropped")
        #     else:
        #         print("oei, iets vergeten: ", type(node))
        #     val += node.value + " "
        #     self.AST.delNode(node)
        #
        # self.children = []
        # self.maxChildren = 0
        # self.value = val

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
        print("Simplified FuncSignDefNode to ", self.name, sign)
        for d in toDelete:
            self.AST.delNode(d)
            self.children.remove(d)

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
        self.returnStats = []  # full return statements

    def simplify(self):
        print("Simplify Codeblock")
        funcSyntax = self.children[1]
        returnStat = funcSyntax.simplify()

        # delete first and last node ('{' and '}')
        self.AST.delNode(self.children[2])
        self.AST.delNode(self.children[0])
        del self.children[2]
        del self.children[0]

        # steal children of funcSyntax
        self.children = funcSyntax.children
        funcSyntax.children = []
        self.AST.delNode(funcSyntax)

        return returnStat  # simplify FuncSyntax node and return return statements

        # self.isSimplified = True
        # kopie = copy.copy(self.children)
        # for node in kopie:
        #     if isinstance(node, ReturnStatNode):
        #         self.returnStats.append(node)
        #     elif isinstance(node, CodeBlockNode):
        #         self.returnStats += node.returnStats
        #     elif isinstance(node, TerNode):
        #         print("node ", node, " gedropped")
        #         self.AST.delNode(node)
        #         self.children.remove(node)
        # self.maxChildren = len(self.children)
        # self.scopeCounter = self.maxChildren + 1

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
        print("Simplify VarNode")
        self.setType(self.children[0].simplify())
        self.AST.delNode(self.children[0])
        self.children = []
        return self.getType()


class LvalueNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Lvalue', maxChildren, ast)

    def simplify(self):
        print("Simplify LvalueNode")
        if len(self.children) == 1:
            self.setType(self.children[0].simplify())
        elif len(self.children) == 2:
            self.children[1].simplify()
            if not isinstance(self.children[1].getType(), POINTER):
                printError("error: dereferencing non-pointer")
                return
            self.setType(self.children[1].getType().getBase())
        else:
            self.setType(self.children[2].simplify())   #* and & cancel eachother in '*&'

        for c in self.children:
            self.AST.delNode(c)
        self.children = []

        return self.getType()


class RvalueNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Rvalue', maxChildren, ast)

    def simplify(self):
        print("Simplify RvalueNode")
        if len(self.children) == 1:
            if isinstance(self.children[0], FuncNode):
                printError("FuncDefNode simplify not yet implemented: returning VOID type")
                return VOID()
            elif isinstance(self.children[0], ArOpNode):
                printError("ArOpNode simplify not yet implemented: returning VOID type")
                return VOID()
            else:
                self.setType(self.children[0].simplify())
        elif len(self.children) == 2:
            self.children[1].simplify() #simplify lvalue node
            if not isinstance(self.children[1].getType(), POINTER):
                printError("error: dereferencing non-pointer")
                return
            self.setType(POINTER(self.children[1].getType()))
        else:
            printError("error: unexpected number of children (", len(self.children) ,") in: ", type(RvalueNode))
            return VOID()

        for c in self.children:
            self.AST.delNode(c)
        self.children = []

        return self.getType()


class FuncSyntaxNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncSyntax', maxChildren, ast)

    def simplify(self):
        print("Simplify FuncSyntaxNode")
        retStatements = []  # all return statement nodes
        for c in self.children:
            c.simplify()
            if isinstance(c, ReturnStatNode):
                retStatements.append(c)
        return retStatements
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


class ArOpNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'ArOp', maxChildren, ast)

    # def simplify(self):
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
            self.children[0].simplify()
            if isinstance(self.children[0], FuncNode) or isinstance(self.children[0], ArOpNode):
                self.type = None
            # can't take type because a function's output might be returned
        print("Simplify returnStatNode: ", self.getType())

        # self.isSimplified = True
        # val = ""
        # getal = 0
        # kopie = copy.copy(self.children)
        # for node in kopie:
        #     if isinstance(node, VarNode) or isinstance(node, LitNode) or isinstance(node, FuncNode) or isinstance(node, ArOpNode):
        #         if getal == 1:
        #             self.returnVal = node
        #         continue
        #     elif isinstance(node, TerNode):
        #         pass
        #     else:
        #         print("oei, iets vergeten bij ReturnStatNode: ", type(node))
        #     getal += 1
        #     val += node.value + " "
        #     self.AST.delNode(node)
        #     self.children.remove(node)
        #
        # self.maxChildren = len(self.children)
        # self.value = val


class VarDefNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'VarDef', maxChildren, ast)

    def simplify(self):
        print("Simplify vardefnode")
        self.children[0].simplify()  # VarDeclNode
        self.children[1].simplify()  # AssignRightNode

        # self.isSimplified = True
        # val = ""
        # kopie = copy.copy(self.children)
        # getal = 0
        # for node in kopie:
        #     if isinstance(node, TypeSpecBaseNode) or isinstance(node, TypeSpecPtrNode):
        #         self.type = node
        #     elif isinstance(node, VarNode):
        #         if getal == 1:
        #             self.var = node
        #         elif getal > 1:
        #             self.right = node
        #     elif isinstance(node, IdentNode):
        #         self.id = node
        #     elif isinstance(node, FuncNode) or isinstance(node, RefNode) \
        #             or isinstance(node, DeRefNode) or isinstance(node, TerNode):
        #         self.right = node
        #     elif isinstance(node, AddNode):
        #         self.arop = node
        #         continue
        #     else:
        #         print("oei, iets vergeten: simply_vardef ", type(node))
        #     val += node.value + " "
        #     self.AST.delNode(node)
        #     self.maxChildren -= 1
        #     self.children.remove(node)
        #     getal += 1
        #
        # self.value = val

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
        # self.isSimplified = True
        # val = ""
        # for node in self.children:
        #     print("\ttype child: ", type(node))
        #     if isinstance(node, TypeSpecNode):
        #         print("\t\ttype")
        #         self.type = node
        #     elif isinstance(node, VarNode):
        #         print("\t\tvarnode")
        #         self.var = node
        #     else:
        #         print("oei, iets vergeten: simply_vardecl ", type(node))
        #     val += node.value + " "
        #     self.AST.delNode(node)
        #
        # self.children = []
        # self.maxChildren = 0
        # self.value = val

    def toLLVM(self):
        print("VARDECL to LLVM")
        return self.type.toLLVM() + " " + self.var.toLLVM()

class FuncNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Func', maxChildren, ast)
        self.name = None
        self.idents = []

    def getType(self):
        return VOID()

    def getName(self):
        return self.name

    def simplify(self):
        self.isSimplified = True
        val = ""
        for node in self.children:
            if isinstance(node, TerNode):
                self.name = node
            elif isinstance(node, IdentNode):
                self.idents.append(node)
            else:
                print("oei, iets vergeten: ", type(node))
            val += node.value + " "
            self.AST.delNode(node)

        self.children = []
        self.maxChildren = 0
        self.value = val


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

        # self.isSimplified = True
        # val = ""
        # for node in self.children:
        #     if isinstance(node, TypeSpecPtrNode) or isinstance(node, TypeSpecBaseNode) or isinstance(node, TerNode):
        #         self.returnType = node
        #     elif isinstance(node, FuncSignNode):
        #         self.fsign = node
        #     else:
        #         print("oei, iets vergeten Bij FuncDeclNode: ", type(node))
        #     val += node.value + " "
        #     self.AST.delNode(node)
        #
        # self.children = []
        # self.maxChildren = 0
        # self.value = val

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

    def simplify(self):
        return
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
        self.setType(self.children[0].getType())
        self.value = self.children[0].value
        self.AST.delNode(self.children[0])
        self.children = []

    # def toLLVM(self):
    #     print("LITNODE to LLVM")
    #     return self.type.toLLVM() + " " + self.value


class IntNode(TerNode, Type):

    def __init__(self, value, ast, pos):
        Type.__init__(self, INT())
        TerNode.__init__(self, value, ast, pos)


class FloatNode(TerNode, Type):

    def __init__(self, value, ast, pos):
        Type.__init__(self, FLOAT())
        TerNode.__init__(self, value, ast, pos)


class CharNode(TerNode, Type):

    def __init__(self, value, ast, pos):
        Type.__init__(self, CHAR())
        TerNode.__init__(self, value, ast, pos)


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
        print("Child: ", self.children[0].value)
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

