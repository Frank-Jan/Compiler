import copy
from src.types import *
from src.SymbolTable import SymbolTable
from src.VarGen import *

varGen = VarGen()

llvmTypes = {'int': 'i32',
             'double': 'double'
             }
counter = 0  # counter to make sure all print debug filenames are unique

class Type:
    # for nodes who have a type/return type
    def __init__(self, type=VOID()):
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
        self.isSimplified = False
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

    def buildSymbolTable(self, symbolTable):
        print("Using base buildSymbolTable: ", type(self))
        return symbolTable

    def isLeaf(self):
        return len(self.children) == 0

    def hasMaxChildren(self):
        count = 0
        for child in self.children:
            if child is not None:
                count += 1
        return self.maxChildren == count

    def toLLVM(self):
        if len(self.children) == 0:
            print("TO DO LLVM: " + str(type(self)))

        code = ""
        for child in self.children:
            code += child.toLLVM()  # + "\n"
        return code

    def simplify(self, scope=None):
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


class ScopeNode(ASTNode):
    def __init__(self, value, maxChildren, ast):
        ASTNode.__init__(self, value, maxChildren, ast)
        self.symbolTable = None

    def getSymbolTable(self):
        if self.symbolTable is None:
            parent = None
            if self.parent is not None:
                parent = self.parent.getSymbolTable()
            self.symbolTable = SymbolTable(parent)
        return self.symbolTable

    def setParent(self, parentScope):
        self.symbolTable.parent = parentScope


class RootNode(ScopeNode):
    def __init__(self, value, maxChildren, ast):
        ScopeNode.__init__(self, value, maxChildren, ast)
        self.symbolTable = SymbolTable()

    def setParent(self, parentScope):
        pass  # is the highest parent (global scope)

    def simplify(self):
        toDelete = []
        newChildren = []
        for c in self.children:
            if isinstance(c, GenStatNode):
                tmp = c.simplify(self.symbolTable)
                newChildren.append(tmp)
            else:
                toDelete.append(c)

        for c in self.children:
            self.AST.delNode(c)
        self.children = newChildren
        self.AST.printDotDebug(str(self.getCount()) + "RootSimplify.dot")
        return self


class GenStatNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenStat', maxChildren, ast)

    def simplify(self, scope):
        # only children need to simplify
        retNode = self.children[0].simplify(scope)
        self.AST.printDotDebug(str(self.getCount()) + "GenStatNode.dot")
        if retNode is not self.children[0]:
            self.AST.delNode(self.children[0])
        self.children.remove(self.children[0])
        return retNode


class AssignNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Assign', maxChildren, ast)
        self.left = None  # right node
        self.right = None  # left node

    def simplify(self, scope=None):
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

    def simplify(self, scope=None):
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
        return self.fsign.getName()

    def setType(self, type):  # set return type
        self.type = type

    #give scope where function is defined
    def simplify(self, scope):
        print("Simplify: FuncDefNode")
        functionScope = SymbolTable(scope)
        if isinstance(self.children[0], TerNode):
            # TerNode will have void as value
            self.setType(VOID())
        else:
            self.setType(self.children[0].simplify())  # first child is TypeSpecNode

        #simplify function signature and fill functionscope
        self.fsign = self.children[1].simplify(functionScope)

        #define function in scope
        scope.defineFunction(self.getName(), self.getType(), self.fsign.types)

        self.returnTypes = self.children[2].simplify(functionScope)  # simplify code block
        self.block = self.children[2]
        self.AST.printDotDebug(str(self.getCount()) + "FuncDef.dot")
        return self

    def buildSymbolTable(self, scope):
        functionScope = SymbolTable(scope)
        self.fsign.buildSymbolTable(functionScope)
        self.block.buildSymbolTable(functionScope)
        return scope

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

    def getName(self):
        if self.isSimplified:
            return self.name
        raise(Exception("error: FuncSignNode getName call before simplify"))

    def simplify(self, scope=None):
        print("Simplify FuncSignNode")
        self.isSimplified = True
        self.name = self.children[0].getName()  # function name
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

    def getName(self):
        if self.isSimplified:
            return self.name
        raise(Exception("error: FuncSignNode getName call before simplify"))

    #give a local scope
    def simplify(self, functionscope):
        print("Simplify FuncSignDefNode")
        self.isSimplified = True
        self.children[0].simplify()
        self.name = self.children[0].getName()  # function name

        toDelete = []  # delete useless Ternodes ('(' ')' ',' variable)
        for c in self.children[1:]:
            if isinstance(c, TypeSpecFuncNode):
                self.types.append(c.simplify())
            elif isinstance(c, VarNode):
                self.varNames.append(c)
            else:
                toDelete.append(c)

        #insert variables of signature in functionscope
        for i in range(len(self.types)):
            functionscope.insertVariable(self.varNames[i].getName(), self.types[i])

        sign = '('
        for i in range(len(self.types)):
            sign += str(self.types[i]) + " " + str(self.varNames[i]) + ", "
        sign += ')'
        for d in toDelete:
            self.AST.delNode(d)
            self.children.remove(d)
        self.AST.printDotDebug(str(self.getCount()) + "FuncSignDef.dot")
        return self

    def buildSymbolTable(self, globalscope):
        localScope = SymbolTable(globalscope)
        # insert variables
        for i in range(len(self.types)):
            localScope.insertVariable(self.varNames[i], self.types[i])
        print("Func sign table:")
        print(localScope)
        return localScope

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

    def simplify(self, scope):
        print("Simplify Codeblock")
        self.symbolTable = scope

        funcSyntax = self.children[1]
        funcSyntax.simplify(scope)
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

        print("CODEBLOCK SCOPE:")
        print(scope)
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

    def simplify(self, scope=None):
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

    def simplify(self, scope=None):
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

    def simplify(self, scope=None):
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

    def simplify(self, scope):
        print("Simplify FuncSyntaxNode")
        new_children = []
        for c in self.children:
            if isinstance(c, FuncStatNode) or isinstance(c, FuncDefNode):
                tmp = c.simplify(scope)
                if tmp is not None:
                    new_children.append(tmp)
                if tmp
                if tmp is not c:
                    self.AST.delNode(c)
            elif isinstance(c, CodeBlockNode):
                #create new scope for CodeBlock
                localScope = SymbolTable(scope)
                self.returnStatements += c.simplify(localScope)
                new_children.append(c)
            elif isinstance(c, LoopNode):
                #needs new scope
                localScope = SymbolTable(scope)
                node = c.simplify(localScope)
                self.returnStatements += node.returnStatements
                new_children.append(node)
                if node is not c:
                    self.AST.delNode(c)
            elif isinstance(c, TerNode):
                self.AST.delNode(c)
                continue
            else:
                printError("Forgot something in FuncSyntax simplify: ", type(c))
        print("FuncSyntax children: ")
        for c in new_children:
            print("\t", type(c))
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

    def simplify(self, scope):
        print("Simplify FuncStatNode")
        if isinstance(self.children[0], VarNode) or isinstance(self.children[0], LitNode):
            self.AST.delNode(self.children[0])
            del self.children[0]
            return None
        ret = self.children[0].simplify(scope)
        del self.children[0]
        self.AST.printDotDebug(str(self.getCount()) + "Funcstat.dot")
        return ret


class ArOpNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'ArOp', maxChildren, ast)
        Type.__init__(self, VOID())

    def simplify(self, scope=None):
        print("Simplify ArOpNode")
        node = self.children[0].simplify()
        if node is not self.children[0]:
            print("\treplace child")
            self.AST.delNode(self.children[0])
            print("ArOpNode Final child: ", type(node), " ", len(node.children), " ", (node in self.AST.nodes))
            # self.children[0] = node
        self.AST.printDotDebug(str(self.getCount()) + "ArOpNode.dot")
        self.children = []
        return node


class ProdNode(ArOpNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Prod', maxChildren, ast)
        self.isMultiplication = True
        self.left = None
        self.right = None

    def isMultiplication(self):
        return self.isMultiplication

    def simplify(self, scope=None):
        print("Simplify ProdNode")
        oldLeft = self.children[0]
        newLeft = oldLeft.simplify()
        if len(self.children) == 1:
            self.AST.delNode(oldLeft)
            self.children = []
            self.AST.printDotDebug(str(self.getCount()) + "Prod.dot")
            return newLeft

        self.isMultiplication = (self.children[1].value == '*')

        oldRight = self.children[2]
        newRight = oldRight.simplify()

        self.AST.delNode(self.children[1])  # delete TerNode +/-
        del self.children[1]
        for c in self.children:
            print("\t", type(c))
        if newLeft is not oldLeft:
            self.AST.delNode(oldLeft)
            self.children[0] = newLeft
        if newRight is not oldRight:
            self.AST.delNode(oldRight)
            self.children[1] = newRight
        for c in self.children:
            c.parent = self
        self.AST.printDotDebug(str(self.getCount()) + "Prod.dot")
        self.left = self.children[0]
        self.right = self.children[1]
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

    def simplify(self, scope = None):
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

        self.AST.delNode(self.children[1])  # delete TerNode +/-
        del self.children[1]
        # for c in self.children:
        #     print("\t", type(c))
        if newLeft is not oldLeft:
            self.AST.delNode(oldLeft)
            self.children[0] = newLeft
        if newRight is not oldRight:
            self.AST.delNode(oldRight)
            self.children[1] = newRight
        self.left = self.children[0]
        self.right = self.children[1]
        self.AST.printDotDebug(str(self.getCount()) + "Addnode.dot")
        return self

    def toLLVM(self):
        self.returnVar = varGen.getNewVar(varGen)
        code = ""
        code += self.left.toLLVM()
        code += self.right.toLLVM()
        code += self.returnVar + " = add " + self.left.returnVar + ", " + self.right.returnVar
        return code


class IdentNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Ident', maxChildren, ast)


class AtomNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Atom', maxChildren, ast)

    def simplify(self, scope = None):
        print("Simplify atomNode")
        if len(self.children) > 1:
            # rule: (ArOpNode)
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
        print("AtomNode retNode ", type(retNode), "children exist?")
        for c in retNode.children:
            print("\t", type(c), " ", (c in self.AST.nodes))
        self.AST.printDotDebug(str(self.getCount()) + "Atom.dot")
        return retNode


class ReturnStatNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'ReturnStat', maxChildren, ast)
        Type.__init__(self, VOID())
        self.returnVal = None

    def simplify(self, scope = None):
        self.AST.delNode(self.children[0])  # del return TerNode
        del self.children[0]
        if len(self.children) == 0:
            self.setType(VOID())  # no return value
        else:
            node = self.children[0].simplify()
            if isinstance(self.children[0], FuncNode) or isinstance(self.children[0], ArOpNode):
                self.type = None
                if node is not self.children[0]:
                    self.AST.delNode(self.children[0])
                self.children[0] = node
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
                return child.toLLVM() + "ret " + child.getType().toLLVM() + " " + child.returnVar
            elif isinstance(child, VarNode):
                return child.toLLVM(True) + "ret " + child.getType().toLLVM() + " " + child.returnVar
            code += child.toLLVM()  # + "\n"
        return code


class VarDefNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'VarDef', maxChildren, ast)

    def getName(self):
        if self.isSimplified:
            return self.children[0].getName()
        raise Exception("VarDefNode getName called before simplified")

    def getType(self):
        if self.isSimplified:
            return self.children[0].getType()
        raise Exception("VarDefNode getType called before simplified")

    def simplify(self, scope):
        print("Simplify vardefnode")
        self.isSimplified = True

        #VarDecl simplify adds variable to node
        varDecl = self.children[0].simplify(scope)  # VarDeclNode
        assignRight = self.children[1].simplify(scope)  # AssignRightNode
        if assignRight is not self.children[1]:
            self.AST.delNode(self.children[1])
            self.children[1] = assignRight

        self.AST.printDotDebug(str(self.getCount()) + "vardef.dot")
        return self

    def toLLVM(self):
        node = self.children[1]
        code = self.children[0].toLLVM()
        var = self.children[1].toLLVM()
        if isinstance(node, VarNode):
            code += node.toLLVM(True)
            var = node.getType().toLLVM() + " " + node.returnVar
        elif isinstance(node, FuncNode):
            code += node.toLLVM()
            var = node.getType().toLLVM() + " " + node.returnVar
        code += "store " + var + ", " + self.children[0].type.toLLVM() + "* " + \
                self.children[0].var.toLLVM() + ", align 4"  # store i32 0, i32* %1
        return code


class GenDefNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenDef', maxChildren, ast)

    def simplify(self, scope):
        print("Simplify GenDefNode")
        retNode = self.children[0].simplify(scope)
        self.children = []
        return retNode


class VarDeclNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'VarDecl', maxChildren, ast)
        # self.type = None  # Types
        self.var = None  # VarNode itself
        self.size = 0

    def getName(self):
        if self.isSimplified:
            return self.var.getName()
        raise Exception("error: getName used in VarDeclNode before simplify")

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: getType used in VarDeclNode before simplify")

    def simplify(self, scope):
        print("Simplify: VarDeclNode")
        self.isSimplified = True
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
        scope.insertVariable(self.getName(), self.getType())
        return self

    def buildSymbolTable(self,symbolTable):
        print("BST: vardecl: ", self.var.value, " ", self.type)
        if not symbolTable.insertVariable(self.var.value, self.type):
            raise Exception("error: {} already defined/declared in local scope".format(self.var.value))



    def toLLVM(self):
        print("VARDECL to LLVM")
        return self.var.toLLVM() + " = alloca " + self.type.toLLVM() + ", align 4\n"  # %1 = alloca i32, align 4


class FuncNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Func', maxChildren, ast)
        self.name = None
        self.arguments = []
        self.returnVar = None  # hulpvar om waarde te returnen

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: FuncNode getType called before simplify")

    def getName(self):
        if self.isSimplified:
            return self.name
        raise Exception("error: FuncNode getName called before simplify")

    def simplify(self, scope):
        print("Simplify FuncNode")
        self.isSimplified = True
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

        #check if exist in scope:
        value = scope.search(self.name)
        if value is None:
            raise Exception("error: function {} called before declaration".format(self.name))
        if value.isVar():
            raise Exception("error: {} is a variable not a function".format(self.name))
        self.AST.printDotDebug(str(self.getCount()) + "func.dot")
        return self

    def getType(self):
        return INT()  # NEEDS TO CHANGE

    def toLLVM(self):
        self.returnVar = varGen.getNewVar(varGen)
        args = ""
        for arg in self.arguments:
            args += arg.toLLVM() + ", "
        args = args[:-2]

        return self.returnVar + " = call " + self.getType().toLLVM() + " " + "@" + self.name + "(" + args + ")\n"  # symboltable.gettype


class GenDeclNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenDecl', maxChildren, ast)

    def simplify(self, scope = None):
        # only children need to simplify
        print("Simplifying declare node")
        retNode = self.children[0].simplify(scope)
        self.children = []
        return retNode


class FuncDeclNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncDecl', maxChildren, ast)
        self.fsign = None

    def setType(self, type):  # set return type
        self.type = type

    def simplify(self, scope = None):
        if isinstance(self.children[0], TerNode):
            # TerNode will have void as value
            self.setType(VOID())
        else:
            self.setType(self.children[0].simplify())  # first child is TypeSpecNode
        self.children[1].simplify()  # simplify funcSign
        self.fsign = self.children[1]

        self.buildSymbolTable(scope)
        return self

    def buildSymbolTable(self, symbolTable):
        string  = "BST: Funcdecl: " + str(self.type) + " " + self.fsign.name + "("
        if len(self.fsign.types) >= 1:
            string += str(self.fsign.types[0])
        if len(self.fsign.types) > 1:
            for a in self.fsign.types[1:]:
                string += ", " + str(a)
        string += ")"
        print(string)

        code = symbolTable.declareFunction(self.fsign.name, self.type, self.fsign.types)
        if code == -1:
            raise Exception("error: {} function already defined/declared as variable in local scope".format(self.fsign.name))
        if code == -2:
            raise Exception("error: {} function already defined/declared with different signature  in local scope".format(self.fsign.name))
        if code == -3:
            raise Exception("error: {} function already defined in local scope".format(self.fsign.name))
        return symbolTable

    def toLLVM(self):
        curCode = "declare " + self.type.toLLVM() + " @" + self.fsign.toLLVM()
        return curCode


class CondExpNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'CondExp', maxChildren, ast)
        self.expression = None

    def simplify(self, scope = None):
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

    def simplify(self, scope = None):
        print("Simplify LoopNode")
        retNode = self.children[0].simplify()  # return while or ifelseLoop
        self.children = []
        return retNode



class WhileNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'While', maxChildren, ast)
        self.cond = None
        self.block = None  # will be CodeblockNode or FuncStatNode
        self.returnStatements = []

    def simplify(self, scope = None):
        print("Simplify WhileNode")
        self.cond = self.children[2].simplify()
        self.block = self.children[4]  # codeblock or functionstatement
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

    def simplify(self, scope = None):
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

    def simplify(self, scope = None):
        print("Simplify TerNode: ", self.value)
        return self.value

    def toLLVM(self):
        return self.value


class VarNode(ASTNode):

    def __init__(self, value, ast, pos):
        # TerNode.__init__(self, value, ast, pos)
        ASTNode.__init__(self, value, 1, ast)
        self.name = value

    def getName(self):
        print("VarNode self name is called: ", self.name)
        return self.name

    def getType(self):  # linken met symbol table
        return VOID()

    def simplify(self, scope = None):
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

    def toLLVM(self, load=False):
        type = self.getType().toLLVM()
        self.returnVar = varGen.getNewVar(varGen)

        if load:  # %6 = load i32, i32* %2, align 4
            return self.returnVar + " = load " + type + ", " + type + "* %" + self.value + ", align 4\n"
        else:
            return "%" + self.value  # %6


class LitNode(ASTNode, Type):

    def __init__(self, maxChildren, ast, _type=VOID()):
        ASTNode.__init__(self, "LIT", maxChildren, ast)
        Type.__init__(self, _type)

    def getValue(self):
        return self.value

    def simplify(self, scope = None):
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

    def simplify(self, scope = None):
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

    def simplify(self, scope = None):
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

    def simplify(self, scope = None):
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

    def simplify(self, scope = None):
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

    def simplify(self, scope = None):
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

    def simplify(self, scope = None):
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

    def simplify(self, scope = None):
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

    def simplify(self, scope = None):
        if isinstance(self.children[0], TerNode):
            # first child is 'void'
            self.setType(VOID())
        else:
            self.setType(self.children[0].simplify())  # first child is the type
            # second child holds "*"
        return self.type

    def toLLVM(self):
        return self.type.toLLVM() + " " + self.value


# includes:
class StdioNode(TerNode):
    def __init__(self, value, ast, pos):
        TerNode.__init__(self, '#include <stdio>', ast, pos)

    def simplify(self, scope = None):
        return self

