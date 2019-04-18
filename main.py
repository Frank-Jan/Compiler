import sys
from src.errors import *
from antlr4 import *
from src.grammars.c_subsetLexer import c_subsetLexer
from src.grammars.c_subsetParser import c_subsetParser
# from src.grammars.c_subsetListener import c_subsetListener
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
        print("Variable or Function: ", var.getType())
        if var is None:
            return -1
        else:
            return var.getType()
    if isinstance(returnStatement.returnVal, ArOpNode):
        print("Can't return arithmic operation yet")
        return "void"

def checkVarDef(node, scope):
    print(node.type.value)
    print(node.var.value)
    # left side cannot exist locally:
    print("checkvardef")
    varType = node.type.value
    varName = node.var.value
    if scope.existLocal(varName):
        printError("error: Redefinition " + varName)
        return -1

    #check if right side of definition is declared
    if isinstance(node.right, VarNode) or isinstance(node.right, FuncNode):
        #search value:
        rightSide = scope.search(node.right.value)
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

    elif isinstance(node.right, RefNode):
        rightSideNode = node.right.var
        rightSide = scope.search(rightSideNode.value)
        if rightSide is None:
            printError("error: undeclared first use " + rightSideNode.value)
            return -2
        # check if types match
        if not (varType == rightSide.getType() or varType == rightSide.getType() + "*"):
            printError("Types don't match: " + str(varType) + "|" + str(rightSide.getType()))
            return -3

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
    else:
        print("UNKNOWN:", type(node.right))
    # insert new variable
    scope.insertVariable(varName, varType)  #will always return True because it was check earlier
    return 0


def checkFuncDef(node, scope):
    # check if return type is same as given
    print(node.block.returnStats)
    for retStat in node.block.returnStats:
        if node.returnType.value != determineType(node.block.symboltable, retStat):
            #wrong return type
            print("Function wrong return type")
            return -1
    # check if function is already defined
    code = scope.defineFunction(node.name.value, node.returnType.value, node.types)
    if code == 0:
        print("Function accepted")
        return 0
    else:
        print("Function denied")
        return -2


def testFile(argv):
    print("1/3:\tLoading file")
    try:
        input_stream = FileStream(argv[1])
    except:
        print("Error loading file:\n", sys.exc_info()[0])
    try:
        lexer = c_subsetLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = c_subsetParser(stream)
        parser.buildParseTrees = True
        tree = parser.cppSyntax()
    except:
        print("Error parsing syntax:\n", sys.exc_info()[0])
        return 1

    print("2/3:\tSyntax accepted")
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
    print("3/3:\tWriting AST to AST.dot")

    scope = SymbolTable(None)
    function = None
    codeBlocks = []

    for node in ast:
        # check scopes
        if len(codeBlocks) != 0:
            codeblokje = codeBlocks[-1]
            codeblokje.scopeCounter -= 1
            if codeblokje.scopeCounter == 0:
                codeBlocks.remove(codeblokje)
                scope = scope.closeScope()

        # print(node)
        if isinstance(node, CodeBlockNode):
            scope = scope.openScope(function)
            function = None
            node.symboltable = scope
            codeBlocks.append(node)
        elif isinstance(node, VarDefNode):
            print("Define variable")
            checkVarDef(node, scope)
        elif isinstance(node, VarDeclNode):
            print("Declare variable")
            #checkVarDecl(node, scope)
        elif isinstance(node, FuncDefNode):
            print("Define function")
            checkFuncDef(node, scope)
        elif isinstance(node, FuncDeclNode):
            print("Declare function")
            scope.declareFunction(node.fsign.name.value, node.returnType.value, node.fsign.types)
        else:
            print("TODO: ", node)
    print(scope)
    return 0


if __name__ == '__main__':
    testFile(sys.argv)
