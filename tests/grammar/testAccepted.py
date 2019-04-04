import sys
from antlr4 import *
from src.grammars.c_subsetLexer import c_subsetLexer
from src.grammars.c_subsetParser import c_subsetParser
from src.grammars.c_subsetListener import c_subsetListener
# from src.DebugListener import DebugListener

def test(inputFile):
    input_stream = FileStream(inputFile)
    lexer = c_subsetLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = c_subsetParser(stream)

def test_accepted():
    try:
        a = 'b'
    except():
        return False
    return True
