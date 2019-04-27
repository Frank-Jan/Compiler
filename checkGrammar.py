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

if __name__ == '__main__':
    testFile(sys.argv)