import sys
from antlr4 import *
from src.grammars.c_subsetLexer import c_subsetLexer
from src.grammars.c_subsetParser import c_subsetParser
#from src.grammars.c_subsetListener import c_subsetListener
from src.Listener import Listener
# from src.DebugListener import DebugListener
from src.ASTNode import *

def testFile(argv):
    print("1/3:\tLoading file")
    try:
        input_stream = FileStream(argv[1])
    except():
        print("Error loading file:\n", sys.exc_info()[0])
    try:
        lexer = c_subsetLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = c_subsetParser(stream)
        parser.buildParseTrees = True
        tree = parser.cppSyntax()
    except():
        print("Error parsing syntax:\n", sys.exc_info()[0])
        return 1

    print("2/3:\tSyntax accepted")
    try:
        listener = Listener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        ast = listener.getAST()
    except():
        print("Error creating AST:\n", sys.exc_info()[0])
        return 1
    print("3/3:\tWriting AST to AST.dot")
    ast.printDot("derivationTree.dot")
    ast.simplify()
    ast.printDot("AST.dot")    

    return 0


if __name__ == '__main__':
    testFile(sys.argv)
