import copy
from src.types import *
from src.SymbolTable import SymbolTable
from src.VarGen import *

varGen = VarGen()

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

    def getCount(self):
        global counter
        counter += 1
        return counter

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
        toDelete = []
        for c in self.children:
            if isinstance(c, TerNode):
                toDelete.append(c)
            else:
                c.simplify()

        for c in toDelete:
            self.children.remove(c)
            self.AST.delNode(c)

        self.AST.printDotDebug(str(self.getCount()) + "BaseSimplify.dot")

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

class RootNode(ScopeNode):
    def __init__(self, value, maxChildren, ast):
        ScopeNode.__init__(self, value, maxChildren, ast)
        self.symbolTable = SymbolTable()

    def setParent(self, parentScope):
        pass

    def simplify(self):
        toDelete = []
        newChildren = []
        for c in self.children:
            if isinstance(c, GenStatNode):
                newChildren.append(c.simplify())

        for c in self.children:
            self.AST.delNode(c)
        self.children = newChildren
        self.AST.printDotDebug(str(self.getCount()) + "BaseSimplify.dot")
        return self

class GenStatNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenStat', maxChildren, ast)

    def simplify(self):
        # only children need to simplify
        retNode = self.children[0].simplify()
        self.AST.printDotDebug(str(self.getCount()) + "GenStatNode.dot")
        self.AST.delNode(self.children[0])
        self.children = []
        return retNode


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
        self.AST.printDotDebug(str(self.getCount()) + "Assign.dot")
        return self


class AssignRightNode(ASTNode, Type):

    def __init__(self, ast):
        ASTNode.__init__(self, 'Assign', 2, ast)  # always 2 children
        Type.__init__(self, VOID())

    def simplify(self):
        print("Simplify AssignRightNode")
        node = self.children[1].simplify()
        if node is not self.children[1]:
            self.AST.delNode(self.children[1])
        self.AST.delNode(self.children[0])
        self.children = []
        self.AST.printDotDebug(str(self.getCount()) + "AssignRight.dot")
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
        self.AST.printDotDebug(str(self.getCount()) + "FuncDef.dot")
        return self

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
            self.AST.printDotDebug(str(self.getCount()) + "FuncSign.dot")
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
        self.AST.printDotDebug(str(self.getCount()) + "FuncSignDef.dot")
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
        if retNode is not self.children[0]:
            self.AST.delNode(self.children[0])
        self.children = []
        self.AST.printDotDebug(str(self.getCount()) + "value" + ".dot")
        self.AST.printDotDebug(str(self.getCount()) + "Value.dot")
        return retNode

    def toLLVM(self):
        return self.value


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
            retNode = self.children[2].simplify()  # * and & cancel eachother in '*&'

        self.children.remove(retNode)
        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        self.AST.printDotDebug(str(self.getCount()) + "Lvalue.dot")
        return retNode


class RvalueNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Rvalue', maxChildren, ast)

    def simplify(self):
        print("Simplify RvalueNode")
        retNode = None
        if len(self.children) == 1:
            retNode = self.children[0].simplify()
        elif len(self.children) == 2:
            retNode = self.children[1].simplify()  # simplify lvalue node
            retNode.type = POINTER(retNode.getType())
        else:
            printError("error: unexpected number of children (", len(self.children), ") in: ", type(RvalueNode))
            retNode = None

        if retNode in self.children:
            self.children.remove(retNode)
        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        self.AST.printDotDebug(str(self.getCount()) + "Rvalue.dot")
        return retNode

    def toLLVM(self):
        pass


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
            elif isinstance(c, CodeBlockNode):
                self.returnStatements += c.simplify()
                new_children.append(c)
            elif isinstance(c, LoopNode):
                node = c.simplify()
                self.returnStatements += node.returnStatements
                new_children.append(node)
                self.AST.delNode(c)
        self.children = new_children
        self.AST.printDotDebug(str(self.getCount()) + "FuncSyntax.dot")
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
        self.AST.printDotDebug(str(self.getCount()) + "Funcstat.dot")
        return ret


class ArOpNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'ArOp', maxChildren, ast)
        Type.__init__(self, VOID())

    def simplify(self):
        print("Simplify ArOpNode")
        node = self.children[0].simplify()
        if node is not self.children[0]:
            print("\treplace child")
            self.AST.delNode(self.children[0])
            print("ArOpNode Final child: ", type(node), " ", len(node.children), " ", (node in self.AST.nodes))
            self.children[0] = node
        self.AST.printDotDebug(str(self.getCount()) + "ArOpNode.dot")
        return self


class ProdNode(ArOpNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Prod', maxChildren, ast)
        self.isMultiplication = True

    def isMultiplication(self):
        return self.isMultiplication

    def simplify(self):
        print("Simplify ProdNode")
        oldLeft = self.children[0]
        newLeft = oldLeft.simplify()
        print("ProdNode ret value exist A: ", (newLeft in self.AST.nodes))
        if len(self.children) == 1:
            print("\tProdNode 1 child: ", type(newLeft))
            self.AST.delNode(oldLeft)
            self.children = []
            self.AST.printDotDebug(str(self.getCount()) + "Prod.dot")
            return newLeft

        self.isMultiplication = (self.children[1].value == '*')
        if self.isMultiplication:
            print("Prodnode is multi")
        else:
            print("Prodnode is div")
        oldRight = self.children[2]
        newRight = oldRight.simplify()
        # if isinstance(newRight, ArOpNode):
        #     tmp = newRight.children[0]
        #     newRight.children = []
        #     self.AST.delNode(newRight)
        #     newRight = tmp

        self.AST.delNode(self.children[1])  #delete TerNode +/-
        del self.children[1]
        print("Before replace children ", len(self.children), " ", type(self))
        for c in self.children:
            print("\t", type(c))
        if newLeft is not oldLeft:
            self.AST.delNode(oldLeft)
            self.children[0] = newLeft
        if newRight is not oldRight:
            self.AST.delNode(oldRight)
            self.children[1] = newRight
        print("After replace children")
        for c in self.children:
            print("\t", type(c))
        self.AST.printDotDebug(str(self.getCount()) + "ProductRule" + ".dot")
        print("ProdNode ret value exist: C", (self in self.AST.nodes))
        print("ProdNode children exist?")
        for c in self.children:
            print("\t", type(c), " ", (c in self.AST.nodes))
            c.parent = self
        self.AST.printDotDebug(str(self.getCount()) + "Prod.dot")
        return self

    def toLLVM(self):
        return "mul " + self.left.toLLVM() + ", " + self.right.toLLVM()


class AddNode(ArOpNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Add', maxChildren, ast)
        self.left = None
        self.right = None
        self.returnVar = None  # hulpVar to return
        self.add = True

    def isAddition(self):
        return self.add

    def simplify(self):
        print("Simplify AddNode")
        oldLeft = self.children[0]
        newLeft = oldLeft.simplify()
        if len(self.children) == 1:
            if newLeft is not oldLeft:
                self.AST.delNode(oldLeft)
            self.children = []
            self.AST.printDotDebug(str(self.getCount()) + "AddRuleA" + ".dot")
            for c in newLeft.children:
                print("\t", type(c), " ", (c in self.AST.nodes))
            return newLeft

        self.add = (self.children[1].value == '+')
        oldRight = self.children[2]
        newRight = oldRight.simplify()

        self.AST.delNode(self.children[1])  #delete TerNode +/-
        del self.children[1]
        for c in self.children:
            print("\t", type(c))
        if newLeft is not oldLeft:
            self.AST.delNode(oldLeft)
            self.children[0] = newLeft
        if newRight is not oldRight:
            self.AST.delNode(oldRight)
            self.children[1] = newRight
        self.AST.printDotDebug(str(self.getCount()) + "Addnode.dot")
        return self

    def toLLVM(self):
        self.returnVar = varGen.getNewVar(varGen)
        code = ""
        code += self.left.toLLVM() + "\n"
        code += self.right.toLLVM() + "\n"
        code += self.returnVar + " = add " + self.left.returnVar + ", " + self.right.returnVar
        return code


class IdentNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Ident', maxChildren, ast)


class AtomNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Atom', maxChildren, ast)

    def simplify(self):
        print("Simplify atomNode")
        if len(self.children) > 1:
            #rule: (ArOpNode)
            retNode = self.children[1].simplify()
            if retNode is not self.children[1]:
                self.AST.delNode(self.children[1])
            self.AST.delNode(self.children[0])
            self.AST.delNode(self.children[2])
        else:
            retNode = self.children[0].simplify()
            if retNode is not self.children[0]:
                self.AST.delNode(self.children[0])
        self.children = []
        print("AtomNode retNode: ", type(retNode))
        self.AST.printDotDebug(str(self.getCount()) + "AtomNode" + ".dot")
        print("AtomNode ret value exist: ", (retNode in self.AST.nodes))
        print("AtomNode retNode ", type(retNode),"children exist?")
        for c in retNode.children:
            print("\t", type(c), " ", (c in self.AST.nodes))
        self.AST.printDotDebug(str(self.getCount()) + "Atom.dot")
        return retNode


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
        self.AST.printDotDebug(str(self.getCount()) + "ReturnStat.dot")
        return self

    def toLLVM(self):
        code = "ret "
        for child in self.children:
            if isinstance(child, FuncNode):
                return child.toLLVM() + "\n" + "ret " + child.returnVar
            code += child.toLLVM()  # + "\n"
        return code


class VarDefNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'VarDef', maxChildren, ast)

    def simplify(self):
        print("Simplify vardefnode")

        self.children[0].simplify()  # VarDeclNode
        node = self.children[1].simplify()  # AssignRightNode
        self.AST.delNode(self.children[1])
        self.children[1] = node
        self.AST.printDotDebug(str(self.getCount()) + "vardef.dot")
        return self

    def toLLVM(self):
        code = self.children[0].toLLVM()
        code += "store " + self.children[1].toLLVM() + ", " + self.children[0].type.toLLVM() + "* " + \
                self.children[0].var.toLLVM()  # store i32 0, i32* %1
        return code


class GenDefNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenDef', maxChildren, ast)

    def simplify(self):
        print("Simplify GenDefNode")
        retNode = self.children[0].simplify()
        self.children = []
        return retNode


class VarDeclNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'VarDecl', maxChildren, ast)
        self.type = None  # Types
        self.var = None  # VarNode itself
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
        return self.var.toLLVM() + " = alloca " + self.type.toLLVM() + ", align 4\n"  # %1 = alloca i32, align 4


class FuncNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Func', maxChildren, ast)
        self.name = None
        self.arguments = []
        self.returnVar = None  # hulpvar om waarde te returnen

    def getType(self):
        return VOID()

    def getName(self):
        return self.name

    def simplify(self):
        print("Simplify FuncNode")
        self.children[0].simplify()
        self.name = self.children[0].value
        for c in self.children[1:]:
            if isinstance(c, ValueNode):
                self.arguments.append(c.simplify())

        toDelete = [item for item in self.children[1:] if item not in self.arguments]
        for c in toDelete:
            self.AST.delNode(c)
        self.children = [self.children[0]]
        self.children += self.arguments
        self.AST.printDotDebug(str(self.getCount()) + "func.dot")
        return self

    def toLLVM(self):
        self.returnVar = varGen.getNewVar(varGen)
        args = ""
        for arg in self.arguments:
            args += "i32 " + arg.toLLVM() + ", "
        args = args[:-2]

        return self.returnVar + " = call " + "i32 " + "@" + self.name + "(" + args + ")"  # symboltable.gettype


class GenDeclNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenDecl', maxChildren, ast)

    def simplify(self):
        # only children need to simplify
        print("Simplifying declare node")
        retNode = self.children[0].simplify()
        self.children = []
        return retNode


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
        self.expression = None

    def simplify(self):
        self.expression = self.children[1].value;
        self.value = self.expression
        self.AST.delNode(self.children[1])
        del self.children[1]
        tmpLeft = self.children[0].simplify()
        tmpRight = self.children[1].simplify()
        if tmpLeft is not self.children[0]:
            self.AST.delNode(self.children[0])
            self.children[0] = tmpLeft
        if tmpRight is not self.children[1]:
            self.AST.delNode(self.children[1])
            self.children[1] = tmpRight
        return self


class LoopNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'LoopNode', maxChildren, ast)

    def simplify(self):
        print("Simplify LoopNode")
        retNode = self.children[0].simplify() #return while or ifelseLoop
        self.children = []
        return retNode

class WhileNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'While', maxChildren, ast)
        self.cond = None
        self.block = None   #will be CodeblockNode or FuncStatNode
        self.returnStatements = []

    def simplify(self):
        print("Simplify WhileNode")
        self.cond = self.children[2].simplify()
        self.block = self.children[4]               #codeblock or functionstatement
        if isinstance(self.block, CodeBlockNode):
            self.returnStatements = self.block.simplify()
        elif isinstance(self.block, ReturnStatNode):
            self.returnStatements = [ReturnStatNode]

        self.AST.delNode(self.children[0])
        self.AST.delNode(self.children[1])
        self.AST.delNode(self.children[3])
        if len(self.children) == 4:
            self.AST.delNode(self.children[4])
            del self.children[4]
        del self.children[3]
        del self.children[1]
        del self.children[0]
        return self


class IfElseNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'IfElse', maxChildren, ast)
        self.cond = None
        self.ifBlock = None
        self.elseBlock = None
        self.returnStatements = []

    def simplify(self):
        toDelete = []
        newChildren = []
        isIfBlock = True
        for c in self.children:
            if isinstance(c, TerNode):
                if c.value == "else":
                    isIfBlock = False
                toDelete.append(c)
            if isinstance(c, CondExpNode):
                self.cond = c.simplify()
                newChildren.append(c)
            if isinstance(c, FuncStatNode):
                if isIfBlock:
                    self.ifBlock = c.simplify()
                else:
                    self.elseBlock = c.simplify()
                newChildren.append(c)
            if isinstance(c, CodeBlockNode):
                if isIfBlock:
                    self.ifBlock = c
                else:
                    self.elseBlock = c
                self.returnStatements.extend(c.simplify())
                newChildren.append(c)

        self.children = newChildren
        for c in toDelete:
            self.AST.delNode(c)
        return self


# CHILDREN THAT ARE NOT PARENTS = LEAFS
class TerNode(ASTNode):  # leafs

    def __init__(self, value, ast, pos):
        ASTNode.__init__(self, value, 0, ast)
        self.child = True
        self.pos = pos

    def simplify(self):
        print("Simplify TerNode: ", self.value)
        return self.value

    def toLLVM(self):
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

    def toLLVM(self):
        return self.type.toLLVM() + " " + self.value


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

    def toLLVM(self):
        return self.type.toLLVM() + " " + self.value


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

    def toLLVM(self):
        return self.type.toLLVM() + " " + self.value


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

    def toLLVM(self):
        return self.type.toLLVM() + " " + self.value


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

    def toLLVM(self):
        return self.type.toLLVM() + " " + self.value


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

    def toLLVM(self):
        return self.type.toLLVM() + " " + self.value


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

    def toLLVM(self):
        return self.type.toLLVM() + " " + self.value


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

    def toLLVM(self):
        return self.type.toLLVM() + " " + self.value
