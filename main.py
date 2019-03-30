import sys
from antlr4 import *
from src.grammars.c_subsetLexer import c_subsetLexer
from src.grammars.c_subsetParser import c_subsetParser
from src.Listener import Listener

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = c_subsetLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = c_subsetParser(stream)
    tree = parser.expression()
    print(tree.getToken(1,0))



if __name__ == '__main__':
    main(sys.argv)