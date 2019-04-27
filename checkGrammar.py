import sys
from src.errors import *
from antlr4 import *
from src.grammars.c_subsetLexer import c_subsetLexer
from src.grammars.c_subsetParser import c_subsetParser
from src.grammars.c_subsetListener import c_subsetListener
from src.Listener import Listener
from src.SymbolTable import ALLSCOPES
# from src.DebugListener import DebugListener
from src.ASTNode import *
from src.VarGen import *


BUILD_DERIVATION = True
BUILD_AST = True

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

    if not BUILD_DERIVATION:
        return 0

    print("2/3: Creating derivation and abstract syntax tree")
    # try:
    listener = Listener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    ast = listener.getAST()
    ast.printDot("derivationTree.dot")

    if not BUILD_AST:
        return 0

    ast.simplify()
    ast.printDot("AST.dot")


if __name__ == '__main__':
    testFile(sys.argv)