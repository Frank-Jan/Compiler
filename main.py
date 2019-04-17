import sys
from antlr4 import *
from src.grammars.c_subsetLexer import c_subsetLexer
from src.grammars.c_subsetParser import c_subsetParser
# from src.grammars.c_subsetListener import c_subsetListener
from src.Listener import Listener
# from src.DebugListener import DebugListener
from src.SymbolTable import *
from src.ASTNode import *


def checkvardef(node, scope):
    print(node.type.value)
    print(node.var.value)
    # insert new variable
    scope.insertVariable(node.var.value, node.type.value)

    typeRight = None
    #check if right side of definition is declared
    if isinstance(node.ter, VarNode):
        print("Var node value: ", node.ter.value)
        print("Var node type:  ", node.ter.type)
        #other side is variable; check if variable exists:
        value = scope.search(node.ter.value)
        if value is None:
            #variable not yet declared
            return -1
        typeRight = value.getType()  #remember type of variable


    print("Print Node: ", node)
    print("Print type: ", node.type)
    print("Print var", node.var)
    print("Print id", node.id)
    if(isinstance(node, VarDefNode)):
        print("Print ter", node.ter, " ", type(node.ter))
        print("Print arop", node.arop)
    #check if types match
    if typeRight != node.type.value:
        print("Types don't match: ", node.type.value, "|", typeRight)


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
        #check scopes
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
            checkvardef(node, scope)
        elif isinstance(node, VarDeclNode):
            scope.insertVariable(node.var.value, node.type.value)
        elif isinstance(node, FuncDefNode):
            print(node.name.value)
            print(node.args)
            function = node.args
            scope.insertFunction(node.name.value, node.returnType.value, node.types)
        elif isinstance(node, FuncDeclNode):
            print(node.fsign.name.value)
            print(node.fsign.types)
            scope.insertFunction(node.fsign.name.value, node.returnType.value, node.fsign.types)
        else:
            print("TODO: ", node)
    print(scope)
    return 0



if __name__ == '__main__':
    testFile(sys.argv)
