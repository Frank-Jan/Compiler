import sys
from antlr4 import *
from src.grammars.c_subsetLexer import c_subsetLexer
from src.grammars.c_subsetParser import c_subsetParser
from src.grammars.c_subsetListener import c_subsetListener
# from src.DebugListener import DebugListener

def test(inputFile):
    try:
        input_stream = FileStream(inputFile)
    except():
        #Error reading file
        return 2
    try:
        lexer = c_subsetLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = c_subsetParser(stream)
    except():
        #Error parsing syntax
        return 1
    #Syntax Accepted
    return 0

def test_accepted():
    try:
        a = 'b'
    except():
        return False
    return True

def testAll():
    print("Testing grammar")
    testDeclarations()

    print("Done...")
    return 0


def testDeclarations():
    print("testDeclarations")

if __name__ == "__main__":
    testAll()
