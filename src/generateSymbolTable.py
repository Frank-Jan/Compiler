from src.errors import *
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


# def generateSymbolTables(ast):
#     ast.getSymbolTable()
#     root = ast.root
#

    # function = None
    # codeBlocks = []

    # for node in ast:
    #     # check scopes
    #     if len(codeBlocks) != 0:
    #         codeblokje = codeBlocks[-1]
    #         codeblokje.scopeCounter -= 1
    #         if codeblokje.scopeCounter == 0:
    #             codeBlocks.remove(codeblokje)
    #             scope = scope.closeScope()
    #
    #     # print(node)
    #     if isinstance(node, CodeBlockNode):
    #         scope = scope.openScope(function)
    #         function = None
    #         node.symboltable = scope
    #         codeBlocks.append(node)
    #     elif isinstance(node, VarDefNode):
    #         printError("Define variable")
    #         checkVarDef(node, scope)
    #     elif isinstance(node, VarDeclNode):
    #         printError("Declare variable")
    #         print("\tNot yet implemented")
    #         #checkVarDecl(node, scope)
    #     elif isinstance(node, FuncDefNode):
    #         printError("Define function")
    #         checkFuncDef(node, scope)
    #     elif isinstance(node, FuncDeclNode):
    #         printError("Declare function")
    #         checkFuncDecl(node, scope)
    #     else:
    #         print("TODO: ", node)
    # print(scope)
    print(scope)