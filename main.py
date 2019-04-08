import sys
from antlr4 import *
from src.grammars.c_subsetLexer import c_subsetLexer
from src.grammars.c_subsetParser import c_subsetParser
#from src.grammars.c_subsetListener import c_subsetListener
from src.Listener import Listener
# from src.DebugListener import DebugListener
from src.ASTNode import *

def main(argv):
    try:
        input_stream = FileStream(argv[1])
        lexer = c_subsetLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = c_subsetParser(stream)
        parser.buildParseTrees = True
        tree = parser.cppSyntax()
    except():
        print("Error:",sys.exc_info()[0])
        return 1
        
    print("Syntax accepted")
    listener = Listener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    ast = listener.getAST()
    ast.printDot("DT.dot")
    ast.simplify()
    ast.printDot("AST.dot")
    return 0


if __name__ == '__main__':
    main(sys.argv)
