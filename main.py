import sys
from antlr4 import *
from c_subsetLexer import c_subsetLexer
from c_subsetParser import c_subsetParser
from c_subsetListener import c_subsetListener

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = c_subsetLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = c_subsetParser(stream)
    tree = parser.expression()


if __name__ == '__main__':
    main(sys.argv)