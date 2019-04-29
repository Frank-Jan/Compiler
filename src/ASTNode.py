import copy
from src.Types import *
from src.SymbolTable import SymbolTable
from src.VarGen import *
from struct import *

varGen = VarGen()

counter = 0  # counter to make sure all print debug filenames are unique

buildinFunctions = ["printf", "scanf"]


class Type:
    # for nodes who have a type/return type
    def __init__(self, type=VOID()):
        self.type = type
        self.deref = 1

    def getType(self):
        return self.type  # returns full type (i.e. int ** or char)

    def setType(self, childType):
        self.type = childType


# A en B have to be of class Type
def compareTypes(A,B):
    return dereferenceType(A) == dereferenceType(B)

def dereferenceType(node):
    if isinstance(node, Type):
        tmp = copy.copy(node.deref)
        type_ = copy.copy(node.getType())
        if isinstance(type_, REFERENCE):
            type_ = POINTER(type_.getBase())
        while tmp > 1:
            tmp -= 1
            if isinstance(type_, POINTER):
                type_ = type_.getBase()
            else:
                raise Exception("error: dereferencing non-pointer {}".format(node.value()))
    else:
        raise Exception("error: trying to get dereference from non-type")
    return type_

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

    def removeChild(self, child):
        if child in self.children:
            self.children.remove(child)

    def stealChildren(self):
        children = self.children
        self.children = []
        return children

    def getCount(self):
        global counter
        counter += 1
        return counter

    def __str__(self):
        return str(self.value) + "  [" + str(self.id) + "]"  # \nNrChildren: " + str(self.maxChildren)

    def isRoot(self):
        return self.value == "Root"

    def buildSymbolTable(self, symbolTable):
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

    def simplify(self, scope):
        # Base simplify will only call simplify(scope) on all children
        toDelete = []
        for c in self.children:
            if isinstance(c, TerNode):
                toDelete.append(c)
            else:
                c.simplify(scope)

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

    def simplify(self, scope=None):
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
        self.returnVar = None

    def simplify(self, scope):
        self.left = self.children[0].simplify(scope)
        self.right = self.children[1].simplify(scope)  # assignRight wil return funcNode or ...

        self.AST.delNode(self.children[0])
        self.AST.delNode(self.children[1])
        self.children[0] = self.left
        self.children[1] = self.right
        self.left.parent = self
        self.right.parent = self

        if isinstance(self.left.getType(), ARRAY):
            raise Exception("error: assignment to expression with array type")

        #check if left side is declared/defined and a variable
        # check if declared or defined in symboltable:
        self.left.checkDeclaration(scope)

        # check if left and right have the same type:
        if not compareTypes(self.left, self.right):
            raise Exception("error: assigning two different types: "
                            "{} {} and {} {}".format(self.left.getType().getBase(), self.left.value , self.right.getType(), self.right.value))

        self.AST.printDotDebug(str(self.getCount()) + "Assign.dot")
        return self


    def toLLVM(self):
        code = ""
        #self.returnVar = VarGen.getNewVar(varGen)
        # symbolTable = self.getSymbolTable()
        # record = symbolTable.search(self.left.value)
        # if record is None:
        #     raise Exception("error: VarNode has no record in symbolTable")
        # type = record.getType().toLLVM()
        type = self.right.getType().toLLVM()
        align = self.right.getType().getAlign()

        if isinstance(self.right, VarNode) or isinstance(self.right, ArOpNode):
            code = self.right.toLLVM(True)
            code += "store " + type + " " + self.right.returnVar + ", " + type + "* " + self.left.toLLVM() + align + "\n"  # store i32 %8, i32* %2, align 4
        elif isinstance(self.right, Type):
            code += "store " + self.right.toLLVM() + ", " + type + "* " + self.left.toLLVM() + align + "\n"  # store i32 %8, i32* %2, align 4
        else:
            code = self.right.toLLVM(True)
            code += "store " + type + " " + self.right.returnVar + ", " + type + "* " + self.left.toLLVM() + align + "\n"  # store i32 %8, i32* %2, align 4
        return code


class AssignRightNode(ASTNode, Type):

    def __init__(self, ast):
        ASTNode.__init__(self, 'Assign', 2, ast)  # always 2 children

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: AssignRight getType called before simplify")

    def simplify(self, scope):
        self.isSimplified = True
        node = self.children[1].simplify(scope)

        if node is not self.children[1]:
            self.AST.delNode(self.children[1])
        self.AST.delNode(self.children[0])
        self.children = []

        self.type = node.getType()
        if isinstance(node.getType(), REFERENCE):
            self.type = POINTER(node.getType().getBase())

        self.AST.printDotDebug(str(self.getCount()) + "AssignRight.dot")
        return node


class FuncDefNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncDef', maxChildren, ast)
        Type.__init__(self, INT())  # default return value of a function is integer
        self.fsign = None  # function signature
        self.block = None  # easy acces to code block

    def getName(self):
        return self.fsign.getName()

    def setType(self, type):  # set return type
        self.type = type

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: FuncDefNode getType called before simplify")

    # give scope where function is defined
    def simplify(self, scope):
        self.isSimplified = True
        functionScope = SymbolTable(scope)
        if isinstance(self.children[0], TerNode):
            # TerNode will have void as value
            self.setType(VOID())
        else:
            self.setType(self.children[0].simplify(scope))  # first child is TypeSpecNode

        self.block = self.children[2]

        # simplify function signature and fill functionscope
        self.fsign = self.children[1].simplify(functionScope, self.block)

        # define function in scope
        scope.defineFunction(self.getName(), self.getType(), self.fsign.types, self)

        self.returnTypes = self.children[2].simplify(functionScope)  # simplify code block

        # check if returnstatements are correct:
        if self.type != VOID() and len(self.block.returnStatements) == 0:
            # expected return statements:
            raise Exception("error: Expected return statements")

        for r in self.block.returnStatements:
            if not compareTypes(r, self):
                raise Exception("error: Wrong return type in function: returns: {}, expected {}"
                                .format(str(r.getType()), str(self.getType())))

        self.AST.printDotDebug(str(self.getCount()) + "FuncDef.dot")
        return self

    # def buildSymbolTable(self, scope):
    #     functionScope = SymbolTable(scope)
    #     self.fsign.buildSymbolTable(functionScope)
    #     self.block.buildSymbolTable(functionScope)
    #     return scope

    def toLLVM(self):
        curCode = "define " + self.getType().toLLVM() + " @" + self.fsign.toLLVM() + "{\n"
        code = ""
        returnVars = []
        for i in range(len(self.fsign.types)):
            var = self.fsign.newNames[i]
            orVar = self.fsign.varNames[i].toLLVM()
            type = self.fsign.types[i].toLLVM()
            align = self.fsign.types[i].getAlign()
            code += orVar + " = alloca " + type + align + "\n"
            code += "store " + type + " " + var + ", " + type + "* " + orVar + align + "\n"

        curCode += code
        curCode += self.block.toLLVM()  # %2 = alloca i32, align 4
        # store i32 %0, i32* %2, align 4
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
        raise (Exception("error: FuncSignNode getName call before simplify"))

    def simplify(self, scope=None):
        self.isSimplified = True
        self.name = self.children[0].simplifyAsName(scope).getName()  # function name

        if self.name in buildinFunctions:
            raise Exception("error: {} already a built-in function".format(self.name))

        toDelete = []  # delete useless Ternodes ('(' ')' ',' variable)
        for c in self.children[1:]:
            if isinstance(c, TypeSpecFuncNode):
                self.types.append(c.simplify(scope))
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
        self.returnStatements = []
        self.newNames = []

    def getName(self):
        if self.isSimplified:
            return self.name
        raise (Exception("error: FuncSignNode getName call before simplify"))

    # give a local scope
    def simplify(self, functionscope, codeBlock):
        self.isSimplified = True
        self.name = self.children[0].simplifyAsName(functionscope).getName()

        if self.name in buildinFunctions:
            raise Exception("error: {} already a built-in function".format(self.name))

        toDelete = []  # delete useless Ternodes ('(' ')' ',' variable)
        for c in self.children[1:]:
            if isinstance(c, TypeSpecFuncNode):
                self.types.append(c.simplify(functionscope))
            elif isinstance(c, VarNode):
                self.varNames.append(c)
            else:
                toDelete.append(c)

        # insert variables of signature in functionscope
        for i in range(len(self.types)):
            self.varNames[i].simplifyAsName(functionscope)
            self.varNames[i].parent = codeBlock
            self.varNames[i].setType(self.types[i])
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
        return localScope

    def toLLVM(self):
        args = ""
        for i in range(len(self.types)):
            args += self.types[i].toLLVM()
            self.newNames.append(varGen.getNewVar(varGen))
            args += " " + self.newNames[i] + ", "
        args = args[:-2]
        curCode = self.name + "(" + args + ")"
        return curCode


class CodeBlockNode(ScopeNode):

    def __init__(self, maxChildren, ast, symboltable=None):
        ASTNode.__init__(self, 'CodeBlock', maxChildren, ast)
        self.returnStatements = []  # full return statements
        self.endCode = False  # if code behind the while loop is reachable

    def simplify(self, scope):
        self.symbolTable = scope

        funcSyntax = self.children[1]
        funcSyntax.simplify(scope)
        self.returnStatements += funcSyntax.returnStatements

        # delete first and last node ('{' and '}')
        self.AST.delNode(self.children[2])
        self.AST.delNode(self.children[0])
        del self.children[2]
        del self.children[0]

        # is endCode if functionSyntax is endCode
        self.endCode = funcSyntax.endCode
        self.returnStatements = funcSyntax.returnStatements
        # steal children of funcSyntax
        self.children = funcSyntax.children
        for c in self.children:
            c.parent = self
        funcSyntax.children = []
        self.AST.delNode(funcSyntax)

        return self.returnStatements

    def getSymbolTable(self):
        return self.symbolTable

    def toLLVM(self):
        code = "\n"
        for child in self.children:
            code += child.toLLVM() + "\n"
        return code


class ValueNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Value', maxChildren, ast)

    def simplify(self, scope):
        if len(self.children) == 1:
            retNode = self.children[0].simplify(scope)
            if retNode is not self.children[0]:
                self.AST.delNode(self.children[0])
            self.children = []
        else:
            #*value
            retNode = self.children[1].simplify(scope)
            if retNode is not self.children[1]:
                self.AST.delNode(self.children[1])
            self.children = []
            if not isinstance(retNode.getType(), POINTER):
                raise Exception("Dereferencing non-pointer")
            retNode.deref += 1

        self.AST.printDotDebug(str(self.getCount()) + "value" + ".dot")
        self.AST.printDotDebug(str(self.getCount()) + "Value.dot")
        return retNode

    def toLLVM(self):
        return self.value


class LvalueNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Lvalue', maxChildren, ast)

    def simplify(self, scope):
        if len(self.children) == 1:
            retNode = self.children[0].simplify(scope)
        elif len(self.children) == 2:
            retNode = self.children[1].simplify(scope)
            if not isinstance(retNode.getType(), POINTER):
                raise Exception("error: dereferencing non-pointer")
                # printError("error: dereferencing non-pointer")
                return
            retNode.deref += 1
        else:
            retNode = self.children[2].simplify(scope)  # * and & cancel eachother in '*&'

        if retNode in self.children:
            self.children.remove(retNode)
        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        self.AST.printDotDebug(str(self.getCount()) + "Lvalue.dot")
        return retNode


class RvalueNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Rvalue', maxChildren, ast)

    def simplify(self, scope):
        retNode = None
        if len(self.children) == 1:
            retNode = self.children[0].simplify(scope)
        elif len(self.children) == 2:
            retNode = self.children[1].simplify(scope)  # simplify lvalue node
            retNode.type = REFERENCE(retNode.getType())
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


class FuncSyntaxNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncSyntax', maxChildren, ast)
        self.returnStatements = []
        self.endCode = False

    def simplify(self, scope):
        new_children = []
        for c in self.children:
            if self.endCode:
                self.AST.delNode(c)
            elif isinstance(c, FuncStatNode) or isinstance(c, FuncDefNode):
                tmp = c.simplify(scope)
                if tmp is not None:
                    new_children.append(tmp)
                if tmp is not c:
                    self.AST.delNode(c)
                if isinstance(tmp, ReturnStatNode):
                    self.returnStatements.append(tmp)
                    self.endCode = True
            elif isinstance(c, CodeBlockNode):
                # create new scope for CodeBlock
                localScope = SymbolTable(scope)
                returnStat = c.simplify(localScope)
                self.endCode = c.endCode
                new_children.append(c)
            elif isinstance(c, LoopNode):
                # needs new scope
                localScope = SymbolTable(scope)
                node = c.simplify(localScope)
                self.returnStatements += node.returnStatements
                self.endCode = node.endCode
                new_children.append(node)
                if node is not c:
                    self.AST.delNode(c)
            elif isinstance(c, TerNode):
                self.AST.delNode(c)
                continue
            else:
                print("Forgot something in FuncSyntax simplify: ", type(c))
        self.children = new_children
        self.AST.printDotDebug(str(self.getCount()) + "FuncSyntax.dot")
        return self


class FuncStatNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncStat', maxChildren, ast)

    def simplify(self, scope):
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
        Type.__init__(self)

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: ArOpNode getType called before simplify")

    def simplify(self, scope=None):
        node = self.children[0].simplify(scope)
        if node is not self.children[0]:
            self.AST.delNode(self.children[0])
        self.AST.printDotDebug(str(self.getCount()) + "ArOpNode.dot")
        self.children = []
        return node


class ProdNode(ArOpNode):

    def __init__(self, maxChildren, ast):
        ArOpNode.__init__(self, maxChildren, ast)
        ArOpNode.__init__(self, maxChildren, ast)
        self.value = 'Product'
        self.multiplication = True
        self.left = None
        self.right = None
        self.returnVar = None

    def isMultiplication(self):
        return self.multiplication

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: ProdNode getType called before simplify")

    def simplify(self, scope=None):
        self.isSimplified = True
        oldLeft = self.children[0]
        newLeft = oldLeft.simplify(scope)
        if len(self.children) == 1:
            self.AST.delNode(oldLeft)
            self.children = []
            self.AST.printDotDebug(str(self.getCount()) + "Prod.dot")
            self.type = newLeft.getType()
            return newLeft

        self.multiplication = (self.children[1].value == '*')

        oldRight = self.children[2]
        newRight = oldRight.simplify(scope)

        self.AST.delNode(self.children[1])  # delete TerNode +/-
        del self.children[1]
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

        # check left and right types:
        if not compareTypes(self.left, self.right):
            raise Exception("error: trying to multiply two different types: "
                            "{} and {}".format(self.left.getType(), self.right.getType()))
        self.type = self.left.getType()
        return self

    def toLLVM(self):
        self.returnVar = varGen.getNewVar(varGen)
        code = ""
        l = self.left.toLLVM()
        r = self.right.value  # het type mag niet nog is getoond worden
        if isinstance(self.left, VarNode):
            code += self.left.toLLVM(True)
            l = self.left.getType().toLLVM() + " " + self.left.returnVar
        if isinstance(self.right, VarNode):
            code += self.right.toLLVM(True)
            r = self.right.returnVar
        if isinstance(self.left, FuncNode) or isinstance(self.left, ArOpNode):
            code += self.left.toLLVM()
            l = self.left.getType().toLLVM() + " " + self.left.returnVar
        if isinstance(self.right, FuncNode) or isinstance(self.right, ArOpNode):
            code += self.right.toLLVM()
            r = self.right.returnVar
        if self.isMultiplication():
            op = "mul"
        else:
            op = "sdiv"
        code += self.returnVar + " = " + op + " " + l + ", " + r + "\n"
        return code


class AddNode(ArOpNode):

    def __init__(self, maxChildren, ast):
        ArOpNode.__init__(self, maxChildren, ast)
        self.value = "Addition"
        self.left = None
        self.right = None
        self.returnVar = None  # hulpVar to return
        self.add = True

    def isAddition(self):
        return self.add

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: AddNode getType called before simplify")

    def simplify(self, scope=None):
        self.isSimplified = True
        oldLeft = self.children[0]
        newLeft = oldLeft.simplify(scope)
        if len(self.children) == 1:
            if newLeft is not oldLeft:
                self.AST.delNode(oldLeft)
            self.children = []
            self.type = newLeft.getType()
            self.AST.printDotDebug(str(self.getCount()) + "AddRuleA" + ".dot")
            return newLeft

        self.add = (self.children[1].value == '+')
        oldRight = self.children[2]
        newRight = oldRight.simplify(scope)

        self.AST.delNode(self.children[1])  # delete TerNode +/-
        del self.children[1]
        if newLeft is not oldLeft:
            self.AST.delNode(oldLeft)
            self.children[0] = newLeft
        if newRight is not oldRight:
            self.AST.delNode(oldRight)
            self.children[1] = newRight
        self.left = self.children[0]
        self.right = self.children[1]

        # check left and right types:
        if not compareTypes(self.left, self.right):
            raise Exception("error: trying to add two different types: "
                            "{} and {}".format(self.left.getType(), self.right.getType()))
        self.type = self.left.getType()

        self.AST.printDotDebug(str(self.getCount()) + "Addnode.dot")
        return self

    def toLLVM(self, load = False):
        self.returnVar = varGen.getNewVar(varGen)
        code = ""
        l = self.left.toLLVM()
        r = self.right.value  # het type mag niet nog is getoond worden
        if isinstance(self.left, VarNode):
            code += self.left.toLLVM(True)
            l = self.left.getType().toLLVM() + " " + self.left.returnVar
        if isinstance(self.right, VarNode):
            code += self.right.toLLVM(True)
            r = self.right.returnVar
        if isinstance(self.left, FuncNode) or isinstance(self.left, ArOpNode):
            code += self.left.toLLVM()
            l = self.left.getType().toLLVM() + " " + self.left.returnVar
        if isinstance(self.right, FuncNode) or isinstance(self.right, ArOpNode):
            code += self.right.toLLVM()
            r = self.right.returnVar
        if self.isAddition():
            op = "add"
        else:
            op = "sub"
        code += self.returnVar + " = " + op + " " + l + ", " + r + "\n"
        return code


class IdentNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Ident', maxChildren, ast)


class AtomNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Atom', maxChildren, ast)

    def simplify(self, scope):
        if len(self.children) > 1:
            # rule: (ArOpNode)
            retNode = self.children[1].simplify(scope)
            if retNode is not self.children[1]:
                self.AST.delNode(self.children[1])
            self.AST.delNode(self.children[0])
            self.AST.delNode(self.children[2])
        else:
            retNode = self.children[0].simplify(scope)
            if retNode is not self.children[0]:
                self.AST.delNode(self.children[0])
        self.children = []
        self.AST.printDotDebug(str(self.getCount()) + "AtomNode" + ".dot")
        self.AST.printDotDebug(str(self.getCount()) + "Atom.dot")
        return retNode


class ReturnStatNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'ReturnStat', maxChildren, ast)
        Type.__init__(self, VOID())
        self.returnVal = None

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
                printError("ReturnStatNode forgot something: {}".format(type(node)))
            self.type = node.getType()


        self.AST.printDotDebug(str(self.getCount()) + "ReturnStat.dot")
        return self

    def toLLVM(self):
        code = "ret "
        for child in self.children:
            if isinstance(child, FuncNode) or isinstance(child, ArOpNode):
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
        self.isSimplified = True

        # VarDecl simplify adds variable to node
        varDecl = self.children[0].simplify(scope)  # VarDeclNode
        assignRight = self.children[1].simplify(scope)  # AssignRightNode
        if assignRight is not self.children[1]:
            self.AST.delNode(self.children[1])
            self.children[1] = assignRight

        # check if left and right have the same type:
        if not compareTypes(varDecl, assignRight):
            if isinstance(varDecl.getType(), POINTER) and isinstance(assignRight.getType(), REFERENCE):
                if varDecl.getType().getBase() != assignRight.getType().getBase():
                    raise Exception("error: types don't match in var definition: "
                                    "{} and {}".format(varDecl.getType().getBase(), assignRight.getType()))
            else:
                if not (isinstance(varDecl.getType(), ARRAY) and isinstance(assignRight.getType(), ARRAY)):
                    raise Exception("error: types don't match in var definition: "
                                    "{} {} and {}".format(varDecl.getType(), varDecl.getName(), assignRight.getType()))

        if isinstance(self.children[0].getType(), ARRAY) and isinstance(self.children[1].getType(), ARRAY):
            if self.children[0].getType().array != self.children[1].getType().array:   # check if right array is long enough
                printError("{} != {}".format(type(self.children[0].getType().array),type(self.children[1].getType().array)))
                raise Exception("error: assigning two elements of different lenghts: {}[{}] and [{}]"
                                .format(self.children[0].getName(), self.children[0].getType().array, self.children[1].getType().array))

            elif isinstance(self.children[0].getType(), ARRAY) and isinstance(self.children[1].getType(), ARRAY):
                if isinstance(self.children[1], VarNode):
                    raise Exception("error: invalid initialisation: array and variable array")

        self.AST.printDotDebug(str(self.getCount()) + "vardef.dot")
        return self

    def toLLVM(self):
        node = self.children[1]
        code = self.children[0].toLLVM(False)
        var = self.children[1].toLLVM()
        if isinstance(node, VarNode):
            code += node.toLLVM(True)
            var = node.getType().toLLVM() + " " + node.returnVar
        elif isinstance(node, FuncNode):
            code += node.toLLVM()
            var = node.returnType.toLLVM() + " " + node.returnVar
        elif isinstance(node, ArOpNode):
            code += node.toLLVM()
            var = node.getType().toLLVM() + " " + node.returnVar
        #else een litnode
        # store i32 0, i32* %1
        code += "store " + var + ", " + self.children[0].type.toLLVM() + "* " + \
                self.children[0].var.toLLVM() + node.getType().getAlign() + "\n"
        return code


class GenDefNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenDef', maxChildren, ast)

    def simplify(self, scope):
        retNode = self.children[0].simplify(scope)
        self.children = []
        return retNode


class VarDeclNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'VarDecl', maxChildren, ast)
        Type.__init__(self)
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
        self.isSimplified = True
        if len(self.children) == 2:
            # no array
            self.size = 1
            self.type = self.children[0].simplify(scope)
            self.var = self.children[1].simplifyAsName(scope)
        else:
            self.size = int(self.children[3].value)
            self.type = ARRAY(self.children[0].simplify(scope))
            self.var = self.children[1].simplifyAsName(scope)

            self.type.array = int(self.children[3].value)
            self.AST.delNode(self.children[2])  # '('
            self.AST.delNode(self.children[3])  # Number
            self.AST.delNode(self.children[4])  # ')'

            if self.size < 0:
                raise Exception("error: array size is negative")

        self.AST.delNode(self.children[0])
        self.AST.delNode(self.children[1])
        self.children = []
        self.value = str(self.type) + " " + str(self.var)

        scope.insertVariable(self.getName(), self.getType(), self)
        return self

    def buildSymbolTable(self, symbolTable):
        if not symbolTable.insertVariable(self.var.value, self.type):
            raise Exception("error: {} already defined/declared in local scope".format(self.var.value))

    def toLLVM(self, init=True):
        type = self.getType()
        # %1 = alloca i32, align 4
        code = self.var.toLLVM() + " = alloca " + self.type.toLLVM() + type.getAlign() + "\n"
        # if init = True, initialize standard on 0
        if init and not isinstance(type, POINTER):
            waarde = 0
            if isinstance(type, FLOAT):
                waarde = 0.0
            code += "store " + self.type.toLLVM() + " "+str(waarde)+", " + self.type.toLLVM() + "* " + \
                    self.var.toLLVM() + type.getAlign() + "\n"
        return code


class FuncNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Func', maxChildren, ast)
        Type.__init__(self, INT())
        self.name = None
        self.arguments = []
        self.returnVar = None  # hulpvar om waarde te returnen
        self.record = None  # node to func definition

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: FuncNode getType called before simplify")

    def getName(self):
        if self.isSimplified:
            return self.name
        raise Exception("error: FuncNode getName called before simplify")

    def simplify(self, scope):
        self.isSimplified = True

        if isinstance(self.children[0], PrintfNode):
            printf = self.children[0].simplify(scope)
            self.children.remove(printf)
            self.AST.delNode(self)
            self.children = []
            return printf

        self.name = self.children[0].simplifyAsName(scope).getName()

        for c in self.children[1:]:
            if isinstance(c, ValueNode):
                self.arguments.append(c.simplify(scope))

        toDelete = [item for item in self.children[1:] if item not in self.arguments]
        for c in toDelete:
            self.AST.delNode(c)
        self.children = [self.children[0]]
        self.children += self.arguments

        # check if exist in scope:
        value = scope.search(self.name)
        if value is None:
            raise Exception("error: function {} called before declaration".format(self.name))
        if value.isVar():
            raise Exception("error: {} is a variable not a function".format(self.name))
        value.isUsed = True
        self.record = value
        self.type = self.record.getType()
        self.AST.printDotDebug(str(self.getCount()) + "func.dot")
        self.value = self.name + '(' + ')'
        return self

    def toLLVM(self, load = True):
        self.returnVar = varGen.getNewVar(varGen)
        self.returnType = self.getType()
        code = ""
        args = ""
        type = ""
        for arg in self.arguments:
            if isinstance(arg, VarNode):
                code += arg.toLLVM(True)
                type = arg.getType()
                args += arg.getType().toLLVM() + " " + arg.returnVar + ", "
            else:
                args += arg.toLLVM() + ", "
        args = args[:-2]

        stat = code + self.returnVar + " = call " + self.getType().toLLVM() + " "
        stat = stat + "@" + self.name + "(" + args + ")\n"  # symboltable.gettype
        if isinstance(self.getType(), POINTER):
            code = ""
            tmp2 = self.returnVar
            type = self.getType().getBase()
            for niv in range(self.deref-1):
                tmp = varGen.getNewVar(varGen)
                code += tmp + " = load " + type.toLLVM() + ", " + type.toLLVM() + "* " + tmp2 + type.getAlign() + "\n"
                type = type.getBase()
                tmp2 = tmp
            self.returnVar = tmp
            self.returnType = type
            for niv in range(self.deref - 1):
                self.returnType = self.returnType.getBase()
        return stat + code


class GenDeclNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenDecl', maxChildren, ast)

    def simplify(self, scope=None):
        # only children need to simplify
        retNode = self.children[0].simplify(scope)
        self.children = []
        return retNode


class FuncDeclNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FuncDecl', maxChildren, ast)
        self.fsign = None

    def setType(self, type):  # set return type
        self.type = type

    def simplify(self, scope):
        if isinstance(self.children[0], TerNode):
            # TerNode will have void as value
            self.setType(VOID())
        else:
            self.setType(self.children[0].simplify(scope))  # first child is TypeSpecNode
        self.children[1].simplify(scope)  # simplify funcSign
        self.fsign = self.children[1]

        self.buildSymbolTable(scope)
        return self

    def buildSymbolTable(self, symbolTable):
        string = "BST: Funcdecl: " + str(self.type) + " " + self.fsign.name + "("
        if len(self.fsign.types) >= 1:
            string += str(self.fsign.types[0])
        if len(self.fsign.types) > 1:
            for a in self.fsign.types[1:]:
                string += ", " + str(a)
        string += ")"

        symbolTable.declareFunction(self.fsign.name, self.type, self.fsign.types, self)
        return symbolTable

    def toLLVM(self):
        curCode = "declare " + self.type.toLLVM() + " @" + self.fsign.toLLVM()
        return curCode


class CondExpNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'CondExp', maxChildren, ast)
        self.expression = None
        self.left = None
        self.right = None
        self.returnVar = None

    def simplify(self, scope=None):
        self.expression = self.children[1].value
        self.value = self.expression
        self.AST.delNode(self.children[1])
        del self.children[1]
        tmpLeft = self.children[0].simplify(scope)
        tmpRight = self.children[1].simplify(scope)
        if tmpLeft is not self.children[0]:
            self.AST.delNode(self.children[0])
            self.children[0] = tmpLeft
        if tmpRight is not self.children[1]:
            self.AST.delNode(self.children[1])
            self.children[1] = tmpRight
        self.left = tmpLeft
        self.right = tmpRight
        return self

    def toLLVM(self):
        self.returnVar = varGen.getNewVar(varGen)
        code = ""
        l = self.left.toLLVM()
        r = self.right.value  # het type mag niet nog is getoond worden
        if isinstance(self.left, VarNode):
            code += self.left.toLLVM(True)
            l = self.left.getType().toLLVM() + " " + self.left.returnVar
        if isinstance(self.right, VarNode):
            code += self.right.toLLVM(True)
            r = self.right.returnVar
        if isinstance(self.left, FuncNode) or isinstance(self.left, ArOpNode):
            code += self.left.toLLVM()
            l = self.left.getType().toLLVM() + " " + self.left.returnVar
        if isinstance(self.right, FuncNode) or isinstance(self.right, ArOpNode):
            code += self.right.toLLVM()
            r = self.right.returnVar
        op = opTypes[self.value]
        # %6 = icmp eq i32 1, %5
        code += self.returnVar + " = icmp " + op + " " + l + ", " + r + "\n"
        return code


class LoopNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'LoopNode', maxChildren, ast)

    # give local scope
    def simplify(self, scope):
        retNode = self.children[0].simplify(scope)  # return while or ifelseLoop
        self.children = []
        return retNode


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
            printError("Forgot something in while simplify: " + str(type(self.block)))

        self.AST.delNode(self.children[0])
        self.AST.delNode(self.children[1])
        self.AST.delNode(self.children[3])
        del self.children[3]
        del self.children[1]
        del self.children[0]
        return self

    def toLLVM(self):
        lbl1 = VarGen.getNewLabel(varGen)
        lbl2 = VarGen.getNewLabel(varGen)
        lbl3 = VarGen.getNewLabel(varGen)
        code = ""
        code += "br label %" + lbl3 + "\n"
        code += lbl3 + ":\n"
        code += self.cond.toLLVM()
        code += "br i1 " + self.cond.returnVar + ", label %" + lbl1 + ", label %" + lbl2 + "\n\n"  # br i1 %6, label %label1, label %label2

        code += lbl1 + ":\n" + self.block.toLLVM() + "\n"
        code += "br label %" + lbl3 + "\n"
        code += lbl2 + ":\n"

        return code


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

    def toLLVM(self):
        code = ""
        code += self.cond.toLLVM()
        lbl1 = VarGen.getNewLabel(varGen)
        lbl2 = VarGen.getNewLabel(varGen)
        code += "br i1 " + self.cond.returnVar + ", label %" + lbl1 + ", label %" + lbl2 + "\n\n"  # br i1 %6, label %label1, label %label2

        code += lbl1 + ":\n" + self.ifBlock.toLLVM() + "\n"

        el = ""
        if self.elseBlock is not None:
            el = self.elseBlock.toLLVM()
        code += lbl2 + ":\n" + el + "\n"

        return code


# CHILDREN THAT ARE NOT PARENTS = LEAFS
class TerNode(ASTNode):  # leafs

    def __init__(self, value, ast, pos):
        if value == '"':
            value = '\\"'
        ASTNode.__init__(self, value, 0, ast)
        # ASTNode.__init__(self, 'TerNode', 0, ast)
        self.child = True
        self.pos = pos

    def simplify(self, scope=None):
        return self.value

    def toLLVM(self):
        return self.value


class VarNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        # TerNode.__init__(self, value, ast, pos)
        ASTNode.__init__(self, 'Variable Name', maxChildren, ast)
        Type.__init__(self, VOID())
        self.name = None
        self.record = None
        self.returnVar = None
        self.returnType = None

    def getName(self):
        if self.isSimplified:
            return self.name
        raise Exception("error: VarNode getName called before simplify")


    def getType(self):  # linken met symbol table
        if self.isSimplified:
            return self.type
        raise Exception("error: VarNode getType called before simplify")

    def checkDeclaration(self, scope):
        value = scope.search(self.getName())

        if value is None:
            raise Exception("Variable {} used before declaration".format(self.getName()))
        if not value.isVar():
            raise Exception("{} is a function not a variable".format(self.getName()))
        self.type = value.getType()
        value.isUsed = True
        self.record = value

    # simplify as function name
    def simplifyAsName(self,scope):
        self.isSimplified = True
        self.name = self.children[0].simplify(scope)
        self.value = self.name
        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        return self

    def simplify(self, scope):
        self.isSimplified = True
        self.name = self.children[0].simplify(scope)
        self.value = self.name
        record = scope.search(self.name)
        if record is None:
            raise Exception("{} not yet declared".format(self.name))
        if not record.isVar():
            raise Exception("{} called as var but is function".format(self.name))

        self.type = record.getType()

        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        return self

    def toLLVM(self, load=False):
        # type = self.getType().toLLVM()
        symbolTable = self.getSymbolTable()
        record = symbolTable.search(self.getName())
        if record is None:
            raise Exception("error: VarNode has no record in symbolTable")
        type = record.getType().toLLVM()
        self.returnVar = varGen.getNewVar(varGen)
        self.returnType = self.getType()

        if load:  # %6 = load i32, i32* %2, align 4
            if isinstance(self.getType(), REFERENCE):
                self.returnVar = "%" + self.value
                return "" # want heeft geen load nodig
            elif isinstance(self.getType(), POINTER) and self.deref:
                code = ""
                tmp2 = "%" + self.value
                type = self.getType()
                for niv in range(self.deref):
                    tmp = varGen.getNewVar(varGen)
                    code += tmp + " = load " + type.toLLVM() + ", " + type.toLLVM() + "* " + tmp2 + type.getAlign() + "\n"
                    type = type.getBase()
                    tmp2 = tmp
                self.returnVar = tmp
                self.returnType = self.getType()
                for niv in range(self.deref-1):
                    self.returnType = self.returnType.getBase()
                return code
            else:
                return self.returnVar + " = load " + type + ", " + type + "* %" + self.value + self.getType().getAlign() + "\n"
        else:
            return "%" + self.value  # %6


class LitNode(ASTNode, Type):

    def __init__(self, maxChildren, ast, _type=VOID()):
        ASTNode.__init__(self, "LIT", maxChildren, ast)
        Type.__init__(self, _type)

    def getValue(self):
        return self.value

    def simplify(self, scope=None):
        retNode = self.children[0].simplify(scope)
        self.value = self.children[0].value
        self.setType(self.children[0].getType())
        self.children.remove(retNode)
        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        return retNode

class numberNode(TerNode):

    def __init__(self, value, ast, pos):
        TerNode.__init__(self, value, ast, pos)

    def simplify(self, scope):
        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        return self

class IntNode(TerNode, Type):

    def __init__(self, value, ast, pos):
        Type.__init__(self, INT())
        TerNode.__init__(self, value, ast, pos)

    def simplify(self, scope=None):
        toDelete = self.children
        for c in toDelete:
            self.AST.delNode(c)
        self.children = []
        return self

    def toLLVM(self, value = False):
        if value:
            return self.value
        return self.type.toLLVM() + " " + self.value


class FloatNode(TerNode, Type):

    def __init__(self, value, ast, pos):
        Type.__init__(self, FLOAT())
        TerNode.__init__(self, value, ast, pos)

    def simplify(self, scope=None):
        toDelete = self.children
        for c in toDelete:
            self.AST.delNode(c)
        self.children = []
        return self

    def floatToLLVMHex(self, float):
        # fl = str(hex(unpack('<Q', pack('<d', float(self.value)))[0])).upper()  # llvm wants double hexa value
        single_precision_rep = pack('>f', float)
        single_precision_val = unpack(">f", single_precision_rep)[0]
        double_val = pack('>d', single_precision_val)
        double_hex = "0x" + double_val.hex()
        return double_hex

    def toLLVM(self, value = False):
        # python float = c double
        fl = str(self.floatToLLVMHex(float(self.value)))
        if value:
            return fl
        return self.type.toLLVM() + " " + fl


class CharNode(TerNode, Type):

    def __init__(self, value, ast, pos):
        Type.__init__(self, CHAR())
        TerNode.__init__(self, value, ast, pos)

    def simplify(self, scope=None):
        toDelete = self.children
        for c in toDelete:
            self.AST.delNode(c)
        self.children = []
        return self

    def toLLVM(self, value = False):
        if len(self.value) == 2:
            raise Exception("error: empty character constant")
        c = str(ord(self.value[1]))
        if value:
            return c
        return self.type.toLLVM() + " " + c


# type/pointer/reference/literal nodes

class TypeSpecNode(Type, ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'TypeSpecNode', maxChildren, ast)
        Type.__init__(self, VOID())

    def setType(self, childType):
        self.type = childType

    def simplify(self, scope=None):
        type = self.children[0].simplify(scope)
        self.setType(type)
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

    def simplify(self, scope=None):
        # self.isSimplified = True
        self.setType(self.children[0].simplify(scope))
        self.value = self.type
        self.AST.delNode(self.children[0])
        self.children = []

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

    def simplify(self, scope=None):
        self.type = toType(self.children[0].value)
        self.AST.delNode(self.children[0])
        self.children = []
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

    def simplify(self, scope=None):
        self.setType(self.children[0].simplify(scope))
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

    def simplify(self, scope=None):
        if isinstance(self.children[0], TerNode):
            # first child is 'void'
            self.setType(VOID())
        else:
            self.setType(self.children[0].simplify(scope))  # first child is the type
            # second child holds "*"
        return self.type

    def toLLVM(self):
        return self.type.toLLVM() + " " + self.value


# includes:
class StdioNode(TerNode):
    def __init__(self, value, ast, pos):
        TerNode.__init__(self, '#include <stdio>', ast, pos)
        ast.stdio = True    #depricated?

    def simplify(self, scope):
        # add printf(char* format,...)
        # add scanf(const char* format,...)
        scope.defineFunction("printf",INT(), [POINTER(CHAR())], self)
        scope.defineFunction("scanf", INT(), [POINTER(CHAR())], self)
        return self

    def toLLVM(self):
        code = "declare i32 @printf(i8*, ...)\ndeclare i32 @scanf(i8*, ...)\n\n"
        return code

class NameNode(TerNode):
    def __init__(self, value, ast, pos):
        TerNode.__init__(self, value, ast, pos)
        self.name = value

    def getName(self):
        return self.name

    def simplify(self, scope):
        return self.name

class NumberNode(TerNode):
    def __init__(self, value, ast, pos):
        TerNode.__init__(self, value, ast, pos)

    def getValue(self):
        return self.name

    def simplify(self, scope):
        return self.name


class PrintfNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'printf', maxChildren, ast)
        Type.__init__(self, INT())  # default return value of a function is integer
        self.format = None
        self.argList = None
        self.name = "printf"
        self.returnVar = None
        self.strings = None

    def getStrings(self):
        return self.strings

    def getFormat(self):
        if self.isSimplified:
            return self.format
        raise Exception("printf getFormat() called before simplify")

    def getArgList(self):
        if self.isSimplified:
            return self.argList
        raise Exception("printf getArgList() called before simplify")

    def getName(self):
        return "printf"

    def setType(self, type):  # set return type
        pass

    def getType(self):
        return INT()

    # give scope where function is defined
    def simplify(self, scope):
        self.isSimplified = True
        toDelete = []
        newChildren = []
        for c in self.children:
            if isinstance(c, TerNode):
                toDelete.append(c)
            elif isinstance(c, PrintFormatNode):
                c.simplify(scope)
                newChildren.append(c)
            elif isinstance(c, IoArgListNode):
                node = c.simplify(scope)
                if node is not c:
                    toDelete.append(c)
                newChildren.append(node)
                self.argList = node
            else:
                node = c.simplify(scope)
                if node is not c:
                    toDelete.append(c)
                newChildren.append(node)
        self.format = newChildren[0]
        self.children = newChildren
        for c in toDelete:
            self.AST.delNode(c)

        self.checkInput()
        return self

    def checkInput(self):
        #check if all inputs are correct
        format = self.children[0].getFormat()    #printformat node
        inputValues = self.children[1].getInputTypes()

        pass


    def toLLVM(self):
        self.strings = self.format.toLLVM() + "\n"#get strings
        self.returnVar = varGen.getNewVar(varGen)
        type = self.getType().toLLVM()
        code = ""
        if self.argList is not None:
            code += self.argList.toLLVM(True)
        stat = self.returnVar + " = call " + type + " "
        code += stat + "(i8*, ...) @printf(i8* getelementptr inbounds ("+self.format.returnType+", "+self.format.returnType+"* " + \
               "@"+self.format.returnVar +", i32 0, i32 0)"
        if self.argList is not None:
            code += self.argList.toLLVM(False)
        code += ")\n"
        return code



class PrintFormatNode(ASTNode):
    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'printformat', maxChildren, ast)
        self.returnVar = None
        self.returnType = None

    def simplify(self, scope):
        toDelete = []
        newChildren = []
        for c in self.children:
            if isinstance(c, TerNode):
                toDelete.append(c)
            else:
                c.simplify(scope)
                newChildren.append(c)

        for d in toDelete:
            self.AST.delNode(d)
        self.children = newChildren
        return self

    def getFormat(self):
        format = []
        for c in self.children:
            if isinstance(c, FormatCharPrintNode):
                format.append(c.getType())
        return format

    def toLLVM(self):
        # @.str = private unnamed_addr constant [21 x i8] c"hey, een char %c, %i\00", align 1
        strings = "c\""
        self.returnVar = "."+varGen.getNewVar(varGen)[1:]
        count = 1 # om wille van \00 einde
        for child in self.children:
            strings += child.toLLVM()
            count += child.length
        strings += "\\00"
        # -2 voor "c"" en -2 voor "\00
        self.returnType = "[" + str(count) + " x i8]"
        return "@" + self.returnVar + " = private unnamed_addr constant " + self.returnType + " " + strings + "\", align 1\n"



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
                printError("IoArgListNode: unexpected node: {}".format(type(c)))

        self.children = newChildren
        for d in toDelete:
            self.AST.delNode(d)
        return self

    def getInputTypes(self):
        pass


    def toLLVM(self, cast = False):
        code = ""
        if cast:
            for c in self.children:
                if isinstance(c, VarNode) or isinstance(c, FuncNode):
                    code += c.toLLVM(True)
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
                if isinstance(self.children[i], VarNode) or isinstance(self.children[i], FuncNode):
                    if isinstance(self.children[i].getType(), FLOAT):
                        code += ", double " + self.returnVars[self.children[i]]
                    else:
                        code += ", i32 " + self.returnVars[self.children[i]]
                else:
                    if isinstance(self.children[i].getType(), FLOAT):
                        code += ", double " + self.children[i].toLLVM(True)
                    else:
                        code += ", i32 " + self.children[i].toLLVM(True)
        return code



class StringNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'StringNode', maxChildren, ast)
        Type.__init__(self, ARRAY(CHAR()))
        self.length = None

    def getString(self):
        if self.isSimplified:
            return self.value
        raise Exception("error: StringNode getString called before simplify()")

    def simplify(self, scope):
        self.isSimplified = True
        self.value = ""
        i=0 # want python leest python string OPNIEUW in als python string...
        while i < len(self.children):
            if self.children[i].value == '\\':
                if self.children[i+1].value != '\\':
                    self.value += pythonStrings[self.children[i+1].value]
                    i += 2
                    continue
                i += 1
            self.value += self.children[i].value
            i += 1

        for c in self.children:
            self.AST.delNode(c)
        self.children = []

        return self

    def toLLVM(self):
        new = ""
        count = 0
        stuk = self.getString()
        if stuk == "":
            return llvmStrings['']
        for i in range(len(stuk)):
            stukje = stuk[i]
            try:
                new += llvmStrings[stukje]
                count += 1
            except(KeyError):
                count += 1
                new += stukje
        self.length = count
        return new






class FormatCharPrintNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'FormatChar', maxChildren, ast)
        Type.__init__(self, VOID())
        self.width = 0
        self.length = 0

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: FormatCharPrintNode getType called before simplify")

    def getWidth(self):
        if self.isSimplified:
            return self.width
        raise Exception("error: FormatCharPrintNode getWidth called before simplify")

    def simplify(self, scope):
        self.isSimplified = True
        self.value = self.children[0].value[0] + self.children[0].value[-1]
        if len(self.children[0].value) > 2:
            self.width = int(self.children[0].value[1:-1])

        if self.value == "%c":
            self.type = CHAR()
        elif self.value == "%s":
            self.type = ARRAY(CHAR())
        elif self.value == "%i":
            self.type = INT()
        elif self.value == "%d":
            self.type = INT()
        elif self.value == "%f":
            self.type = FLOAT()
        else:
            raise Exception("error: unknown format specifier {}".format(self.value))

        self.AST.delNode(self.children[0])
        self.children = []
        return self

    def toLLVM(self):
        width = str(self.getWidth())
        if width == '0':
            width = ""
        code = str(self.value[:1]) + width + str(self.value[-1:])
        self.length = len(code)
        return code

class ArrayNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Array', maxChildren, ast)
        Type.__init__(self, VOID())
        self.length = 1

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: ArrayNode getType called before simplify")

    def getLenght(self):
        if self.isSimplified:
            return self.length
        raise Exception("error: ArrayPrintNode getLength called before simplify")

    def simplify(self,scope):
        self.isSimplified = True
        toDelete = []
        newChildren = []
        for c in self.children:
            if isinstance(c, TerNode):
                toDelete.append(c)
            else:
                node = c.simplify(scope)
                if node is not c:
                    self.AST.delNode(c)
                newChildren.append(node)
                node.parent = self

        for d in toDelete:
            self.AST.delNode(d)

        if len(newChildren) > 0:
            self.type = newChildren[0].getType()
        for c in newChildren:
            if c.getType() != self.type:
                raise Exception("error: types in array don't match: {} and {}".format(self.type, c.getType()))

        self.length = len(newChildren)
        self.type = ARRAY(self.type)
        self.type.array = self.length
        self.children = newChildren
        return self

class ArrayElementNode(VarNode):

    def __init__(self, maxChildren, ast):
        VarNode.__init__(self, maxChildren, ast)
        self.value = "Array Element"
        self.number = 0

    def getNumber(self):
        if self.isSimplified:
            return self.number
        raise Exception("error: ArrayElement getNumber called before simplify")

    def simplify(self, scope):
        self.isSimplified = True
        nameSet = False
        toDelete = []
        newChildren = []
        node = self.children[0].simplify(scope)
        self.name = node.getName()
        #check if varnode is array
        if not (isinstance(node.getType(), POINTER)):
            raise Exception("error: used [] on non-array")

        self.type = node.getType().getBase()

        self.number = self.children[2].simplify(scope)  #VarNode/functionNode/LitNode

        if self.number is not self.children[2]:
            self.AST.delNode(self.children[2])

        #check if self.number returns/is a integer
        if not isinstance(self.number.getType(), INT):
            raise Exception("error: didn't use integer or return integer for accessing array element")


        self.children[2] = self.number
        self.value = str(self.name) + "[" + str(self.number.value) + "]"

        self.AST.delNode(self.children[3])
        self.AST.delNode(self.children[1])

        self.children.remove(self.children[3])
        self.children.remove(self.children[1])
        return self
