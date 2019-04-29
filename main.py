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
    try:
        input_stream = FileStream(argv[1])
    except:
        print("Error loading file:\n", sys.exc_info()[0])
        return 1
    try:
        lexer = c_subsetLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = c_subsetParser(stream)
        parser.buildParseTrees = True
        tree = parser.cSyntax()
    except Exception as e:
        print("Error parsing syntax:\n", sys.exc_info()[0])
        return 2

    try:
        listener = Listener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        ast = listener.getAST()
    except Exception as e:
        printError(str(e))
        return 3

    try:
        ast.printDot("derivationTree.dot")
        ast.simplify()
        ast.printDot("AST.dot")
    except Exception as e:
        printError(str(e))
        return 4

    # ast.printDot("derivationTree.dot")
    # ast.simplify()
    # ast.printDot("AST.dot")

    f = open("tests/test.ll", "w+")
    text = ""

    for node in ast:
        if isinstance(node, FuncDeclNode) or isinstance(node, FuncDefNode) or isinstance(node, StdioNode):
            text += node.toLLVM() + "\n\n"
        # elif isinstance(node, IfElseNode):
        #     text += node.toLLVM() + "\n\n"
        elif isinstance(node, TerNode):
            pass
        elif isinstance(node, PrintfNode):
            text = node.getStrings() + text

    f.write(text)

    return 0


if __name__ == '__main__':
    sys.exit(testFile(sys.argv))
