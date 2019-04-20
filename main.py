import sys
from src.errors import *
from antlr4 import *
from src.grammars.c_subsetLexer import c_subsetLexer
from src.grammars.c_subsetParser import c_subsetParser
from src.grammars.c_subsetListener import c_subsetListener
from src.Listener import Listener
# from src.DebugListener import DebugListener
from src.SymbolTable import *
from src.ASTNode import *


#give a single returnStatement and the scope for it
def determineType(scope, returnStatement):
    if returnStatement.returnVal is None:
        return "void"
    if isinstance(returnStatement.returnVal, LitNode):    #is it a literal
        return returnStatement.returnVal.type
    if isinstance(returnStatement.returnVal, VarNode) or isinstance(returnStatement.returnVal, FuncNode):    #is it a variable
        #search for variable in scope
        var = scope.search(returnStatement.returnVal.value)
        if var is None:
            return -1
        else:
            return var.getType()
    if isinstance(returnStatement.returnVal, ArOpNode):
        print("Can't return arithmic operation yet")
        return "void"


def checkVarDef(node, scope):
    # left side cannot exist locally:
    print("checkvardef for: ", node.type.value, node.var.value)
    varType = node.type.value
    varName = node.var.value
    if scope.existLocal(varName):
        printError("error: Redefinition " + varName)
        return -1

    #check if right side of definition is declared
    if isinstance(node.right, VarNode) or isinstance(node.right, FuncNode):
        #search value:
        rightSide = scope.search(node.right.value)
        print("\tname rightside?: ", node.right.value)
        if rightSide is None:
            printError("error: undeclared first use " + node.right.value)
            return -2

        # check if types match
        if varType != rightSide.getType():
            printError("Types don't match: " + str(varType) + "|" + str(rightSide.getType()))
            return -3

    elif isinstance(node.right, IntNode) or isinstance(node.right, CharNode) or isinstance(node.right, FloatNode):
        # check if types match
        if varType != node.right.type:
            printError("Types don't match: " + str(varType) + "|" + str(node.right.type))
            return -3

    # elif isinstance(node.right, RefNode):
    #     rightSideNode = node.right.var
    #     rightSide = scope.search(rightSideNode.value)
    #     if rightSide is None:
    #         printError("error: undeclared first use " + rightSideNode.value)
    #         return -2
    #     # check if types match
    #     if not (varType == rightSide.getType() or varType == rightSide.getType() + "*"):
    #         printError("Types don't match: " + str(varType) + "|" + str(rightSide.getType()))
    #         return -3

    elif isinstance(node.right, DeRefNode):
        rightSideNode = node.right.var
        rightSide = scope.search(rightSideNode.value)
        if rightSide is None:
            printError("error: undeclared first use " + rightSideNode.value)
            return -2
        # check if types match
        if varType + "*" != rightSide.getType():
            printError("Types don't match: " + str(varType) + "|" + str(rightSide.getType()))
            return -3
    elif isinstance(node.right, ArOpNode):
        print("ArOpNode not implemented")
        return 0
    else:
        print("UNKNOWN:", type(node.right))
        return 0
    # insert new variable
    scope.insertVariable(varName, varType)  #will always return True because it was check earlier
    print("\tvardef accepted")
    return 0


def checkFuncDef(node, scope):
    print("Check func def for: ", node.returnType.value, " ", node.name.value, " ", node.types)
    # check if return type is same as given
    for retStat in node.block.returnStats:
        if node.returnType.value != determineType(node.block.symboltable, retStat):
            #wrong return type
            print("\tFunction wrong return type")
            return -1
    # check if function is already defined
    code = scope.defineFunction(node.name.value, node.returnType.value, node.types)
    if code == 0:
        print("\tFunction accepted")
        return 0
    else:
        printError("error: function definition denied")
        return -2

def checkFuncDecl(node, scope):
    print("Check func decl for: ", node.returnType.value, " ", node.fsign.name, " ", node.fsign.types)
    # check if function is already defined or declared
    code = scope.declareFunction(node.fsign.name, node.returnType.value, node.fsign.types)
    if code == 0:
        print("\tFunction accepted")
        return 0
    else:
        printError("error: function declaration denied")
        return -1


def testFile(argv):
    print("1/3: Parsing file")
    try:
        input_stream = FileStream(argv[1])
    except:
        print("Error loading file:\n", sys.exc_info()[0])
    try:
        lexer = c_subsetLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = c_subsetParser(stream)
        parser.buildParseTrees = True
        tree = parser.cSyntax()
    except:
        print("Error parsing syntax:\n", sys.exc_info()[0])
        return 1

    print("\tSyntax accepted")

    print("2/3: Creating derivation and abstract syntax tree")
    # try:
    listener = Listener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    ast = listener.getAST()
    ast.printDot("derivationTree.dot")
    ast.simplify()
    ast.printDot("AST.dot")
    # except:
    #     print("Error creating AST:\n", sys.exc_info()[0])
    #     return 1
    print("\tWritten AST to AST.dot")

    print("3/3: Creating symbol table")

    scope = SymbolTable(None)
    # generateSymbolTable(ast, scope)

    #
    # f = open("tests/test.ll", "w+")
    # text = "\n\n"
    #
    # for node in ast:
    #     if isinstance(node, FuncDeclNode) or isinstance(node, FuncDefNode):
    #         text += node.toLLVM() + "\n\n"
    #
    #
    # f.write(text)
    # print(text)

    return 0


if __name__ == '__main__':
    testFile(sys.argv)
