import sys
from antlr4 import *
from src.grammars.c_subsetLexer import c_subsetLexer
from src.grammars.c_subsetParser import c_subsetParser
from src.Listener import Listener
import src.AST.init as AST
import src.llvm2mips.llvmToAsm as mips

# from src.DebugListener import DebugListener


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
        raise str(e)
        return 3

    try:
        ast.printDot("derivationTree.dot")
        ast.simplify()
        ast.printDot("AST.dot")
    except Exception as e:
        raise str(e)
        return 4

    # ast.printDot("derivationTree.dot")
    # ast.simplify()
    # ast.printDot("AST.dot")

    llFile = argv[1].replace(".c", ".ll")

    f = open(llFile, "w+")
    text = ""

    # for node in ast:
    #
    #     if isinstance(node, AST.FuncDeclNode) or isinstance(node, AST.FuncDefNode) or isinstance(node, AST.StdioNode):
    #         text += node.toLLVM() + "\n\n"
    #     # elif isinstance(node, IfElseNode):
    #     #     text += node.printLLVM() + "\n\n"
    #     elif isinstance(node, AST.TerNode):
    #         pass
    #     elif isinstance(node, AST.PrintfNode):
    #         text = node.getStrings() + text

    ll = ast.root.toLLVM()
    for obj in ll:
        text += str(obj)

    f.write(text)

    # give llvm code ll to mipsbuilder:
    mipsbuilder = mips.MIPSBuilder(ll)
    mipsbuilder.build()
    mipsbuilder.mipsToFile("test.asm")


    return 0


if __name__ == '__main__':
    sys.exit(testFile(sys.argv))
