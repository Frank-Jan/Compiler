from src.errors import *
from src.ASTNode import *


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