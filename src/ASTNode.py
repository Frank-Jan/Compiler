import copy
from src.Types import *
from src.SymbolTable import SymbolTable
from src.VarGen import *
from struct import *

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
        # Base simplify will only call simplify(scope) on all children
        print("Base simplify for: ", type(self))
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
        print("Simplify AssignNode")
        if len(self.children) != 2:
            printError("AssignNode doesn't have 2 children: ", len(self.children))
        self.left = self.children[0].simplify(scope)
        self.right = self.children[1].simplify(scope)  # assignRight wil return funcNode or ...
        self.AST.delNode(self.children[0])
        self.AST.delNode(self.children[1])
        self.children[0] = self.left
        self.children[1] = self.right
        self.left.parent = self
        self.right.parent = self

        # check if left and right have the same type:
        if self.left.getType() != self.right.getType():
            if isinstance(self.left.getType(), REFERENCE):
                if self.left.getType().getBase() != self.right.getType():
                    raise Exception("error: assigning two different types: "
                                    "{} and {}".format(self.left.getType().getBase(), self.right.getType()))
            else:
                raise Exception("error: assigning two different types: "
                                "{} and {}".format(self.left.getType(), self.right.getType()))

            # if isinstance(self.left.getType(), REFERENCE):
            #    if self.left.getType().getBase() != self.right.getType():
            #         raise Exception("error: assigning two different types: "
            #                 "{} and {}".format(self.left.getType(),self.right.getType()))

        self.AST.printDotDebug(str(self.getCount()) + "Assign.dot")
        return self

    def toLLVM(self):
        code = self.right.toLLVM()
        self.returnVar = VarGen.getNewVar(varGen)
        symbolTable = self.getSymbolTable()
        record = symbolTable.search(self.left.value)
        if record is None:
            raise Exception("error: VarNode has no record in symbolTable")
        type = record.getType().toLLVM()
        code += "store " + type + " " + self.right.returnVar + ", " + type + "* " + self.left.toLLVM()  # store i32 %8, i32* %2, align 4
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
        print("Simplify AssignRightNode")
        node = self.children[1].simplify(scope)
        if node is not self.children[1]:
            self.AST.delNode(self.children[1])
        self.AST.delNode(self.children[0])
        self.children = []

        self.type = node.getType()
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
        print("Simplify: FuncDefNode")
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
        scope.defineFunction(self.getName(), self.getType(), self.fsign.types)

        self.returnTypes = self.children[2].simplify(functionScope)  # simplify code block

        # check if returnstatements are correct:
        if self.type != VOID() and len(self.block.returnStatements) == 0:
            # expected return statements:
            raise Exception("error: Expected return statements")

        for r in self.block.returnStatements:
            if r.getType() != self.getType():
                raise Exception("error: Wrong return type in function: returns: {}, expected {}"
                                .format(str(r.getType()), str(self.getType())))

        self.AST.printDotDebug(str(self.getCount()) + "FuncDef.dot")
        return self

    def buildSymbolTable(self, scope):
        functionScope = SymbolTable(scope)
        self.fsign.buildSymbolTable(functionScope)
        self.block.buildSymbolTable(functionScope)
        return scope

    def toLLVM(self):
        curCode = "define " + llvmTypes[str(self.getType())] + " @" + self.fsign.toLLVM() + "{\n"
        code = ""
        returnVars = []
        for i in range(len(self.fsign.types)):
            var = self.fsign.newNames[i]
            orVar = self.fsign.varNames[i].toLLVM()
            type = self.fsign.types[i].toLLVM()
            code += orVar + " = alloca " + type + ", align 4\n"
            code += "store " + type + " " + var + ", " + type + "* " + orVar + ", align 4\n"

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
        print("Simplify FuncSignNode")
        self.isSimplified = True
        self.name = self.children[0].simplifyAsName()  # function name

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
        print("Simplify FuncSignDefNode")
        self.isSimplified = True
        self.name = self.children[0].simplifyAsName()

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
            self.varNames[i].parent = codeBlock
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
        print("Simplify ValueNode")
        retNode = self.children[0].simplify(scope)
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
            retNode = self.children[0].simplify(scope)
        elif len(self.children) == 2:
            retNode = self.children[1].simplify(scope)
            if not isinstance(retNode.getType(), POINTER):
                printError("error: dereferencing non-pointer")
                return None
            retNode.type = retNode.getType().getBase()
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
        print("Simplify RvalueNode")
        retNode = None
        if len(self.children) == 1:
            retNode = self.children[0].simplify(scope)
        elif len(self.children) == 2:
            retNode = self.children[1].simplify(scope)  # simplify lvalue node
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
        self.endCode = False

    def simplify(self, scope):
        print("Simplify FuncSyntaxNode")
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
                printError("Forgot something in FuncSyntax simplify: ", type(c))
        self.children = new_children
        self.AST.printDotDebug(str(self.getCount()) + "FuncSyntax.dot")
        return self


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

    def getType(self):
        if self.isSimplified:
            return self.type
        raise Exception("error: ArOpNode getType called before simplify")

    def simplify(self, scope=None):
        print("Simplify ArOpNode")
        node = self.children[0].simplify(scope)
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
        print("Simplify ProdNode")
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

        # check left and right types:
        if self.left.getType() != self.right.getType():
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


class AddNode(ArOpNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'Add', maxChildren, ast)
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
        print("Simplify AddNode")
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

        # check left and right types:
        if self.left.getType() != self.right.getType():
            raise Exception("error: trying to add two different types: "
                            "{} and {}".format(self.left.getType(), self.right.getType()))
        self.type = self.left.getType()

        self.AST.printDotDebug(str(self.getCount()) + "Addnode.dot")
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
        print("Simplify atomNode")
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
        print("Simplify vardefnode")
        self.isSimplified = True

        # VarDecl simplify adds variable to node
        varDecl = self.children[0].simplify(scope)  # VarDeclNode
        assignRight = self.children[1].simplify(scope)  # AssignRightNode
        if assignRight is not self.children[1]:
            self.AST.delNode(self.children[1])
            self.children[1] = assignRight

        # check if types match
        if self.getType() != assignRight.getType():
            raise Exception("error: types dont match in var definition: "
                            "{} and {}".format(self.getType(), assignRight.getType()))
        self.AST.printDotDebug(str(self.getCount()) + "vardef.dot")
        return self

    def toLLVM(self):
        node = self.children[1]
        code = self.children[0].toLLVM()
        var = self.children[1].toLLVM()
        if isinstance(node, VarNode):
            code += node.toLLVM(True)
            var = node.getType().toLLVM() + " " + node.returnVar
        elif isinstance(node, FuncNode) or isinstance(node, ArOpNode):
            code += node.toLLVM()
            var = node.getType().toLLVM() + " " + node.returnVar
        # store i32 0, i32* %1
        align = 4
        if isinstance(node, CharNode):
            align = 1
        code += "store " + var + ", " + self.children[0].type.toLLVM() + "* " + \
                self.children[0].var.toLLVM() + ", align " + str(align) + "\n"
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
            self.type = self.children[0].simplify(scope)
            self.var = self.children[1]
        else:
            self.size = self.children[3].value
            self.type = self.children[0].simplify(scope)
            self.var = self.children[1]
            self.AST.delNode(self.children[2])  # '('
            self.AST.delNode(self.children[3])  # DIGIT
            self.AST.delNode(self.children[4])  # ')'

        self.AST.delNode(self.children[0])
        self.AST.delNode(self.children[1])
        self.children = []
        self.value = str(self.type) + " " + str(self.var)

        # check if declaration is possible

        scope.insertVariable(self.getName(), self.getType(), self)
        return self

    def buildSymbolTable(self, symbolTable):
        print("BST: vardecl: ", self.var.value, " ", self.type)
        if not symbolTable.insertVariable(self.var.value, self.type):
            raise Exception("error: {} already defined/declared in local scope".format(self.var.value))

    def toLLVM(self):
        print("VARDECL to LLVM")
        align = 4
        if self.type == CHAR():
            align = 1
        return self.var.toLLVM() + " = alloca " + self.type.toLLVM() + ", align " + str(
            align) + "\n"  # %1 = alloca i32, align 4


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
        self.name = self.children[0].simplifyAsName()

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
        self.AST.printDotDebug(str(self.getCount()) + "func.dot")
        return self

    def getType(self):
        return INT()  # NEEDS TO CHANGE

    def toLLVM(self):
        self.returnVar = varGen.getNewVar(varGen)
        code = ""
        args = ""
        for arg in self.arguments:
            if isinstance(arg, VarNode):
                code += arg.toLLVM(True)
                args += arg.getType().toLLVM() + " " + arg.returnVar + ", "
            else:
                args += arg.toLLVM() + ", "
        args = args[:-2]

        return code + self.returnVar + " = call " + self.getType().toLLVM() + " " + "@" + self.name + "(" + args + ")\n"  # symboltable.gettype


class GenDeclNode(ASTNode):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'GenDecl', maxChildren, ast)

    def simplify(self, scope=None):
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

    def simplify(self, scope=None):
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
        print(string)

        code = symbolTable.declareFunction(self.fsign.name, self.type, self.fsign.types)
        if code == -1:
            raise Exception(
                "error: {} function already defined/declared as variable in local scope".format(self.fsign.name))
        if code == -2:
            raise Exception(
                "error: {} function already defined/declared with different signature  in local scope".format(
                    self.fsign.name))
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
        print("Simplify LoopNode")
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
        print("Simplify WhileNode")
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
        code = ""
        code += self.cond.toLLVM()
        lbl1 = VarGen.getNewLabel(varGen)
        lbl2 = VarGen.getNewLabel(varGen)
        lbl3 = VarGen.getNewLabel(varGen)
        code += "br label %" + lbl3 + "\n"
        code += lbl3 + ":\n"
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
        ASTNode.__init__(self, value, 0, ast)
        self.child = True
        self.pos = pos

    def simplify(self, scope=None):
        print("Simplify TerNode: ", self.value)
        return self.value

    def toLLVM(self):
        return self.value


class VarNode(ASTNode, Type):

    def __init__(self, value, ast, pos):
        # TerNode.__init__(self, value, ast, pos)
        ASTNode.__init__(self, value, 1, ast)
        self.name = value

    def getName(self):
        print("VarNode self name is called: ", self.name)
        return self.name

    def getType(self):  # linken met symbol table
        if self.isSimplified:
            return self.type
        raise Exception("error: VarNode getType called before simplify")

    # simplify as function name
    def simplifyAsName(self):
        for c in self.children:
            self.AST.delNode(c)
        self.children = []
        return self.name

    def simplify(self, scope):
        self.isSimplified = True
        for c in self.children:
            self.AST.delNode(c)
        self.children = []

        # check if declared or defined in symboltable:
        value = scope.search(self.value)
        if value is None:
            raise Exception("Variable {} used before declaration".format(self.name))
        if not value.isVar():
            raise Exception("{} is a function not a variable".format(self.name))
        self.type = value.getType()
        value.isUsed = True
        return self

    def toLLVM(self, load=False):
        # type = self.getType().toLLVM()
        symbolTable = self.getSymbolTable()
        record = symbolTable.search(self.getName())
        if record is None:
            raise Exception("error: VarNode has no record in symbolTable")
        type = record.getType().toLLVM()
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

    def simplify(self, scope=None):
        print("Simplify LitNode")
        retNode = self.children[0].simplify(scope)
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

    def simplify(self, scope=None):
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

    def simplify(self, scope=None):
        print("Simplify FloatNode: ", self.value)
        toDelete = self.children
        for c in toDelete:
            self.AST.delNode(c)
        self.children = []
        return self

    def toLLVM(self):
        # python float = c double
        fl = str(hex(unpack('<Q', pack('<d', float(self.value)))[0])).upper()  # llvm wants double hexa value
        return self.type.toLLVM() + " " + fl


class CharNode(TerNode, Type):

    def __init__(self, value, ast, pos):
        Type.__init__(self, CHAR())
        TerNode.__init__(self, value, ast, pos)

    def simplify(self, scope=None):
        print("Simplify CharNode: ", self.value)
        toDelete = self.children
        for c in toDelete:
            self.AST.delNode(c)
        self.children = []
        return self

    def toLLVM(self):
        if len(self.value) == 2:
            raise Exception("error: empty character constant")
        char = str(ord(self.value[1]))
        return self.type.toLLVM() + " " + char


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

    def simplify(self, scope=None):
        self.setType(self.children[0].simplify(scope))
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

    def simplify(self, scope=None):
        return self
