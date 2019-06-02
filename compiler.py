import sys
import copy
from antlr4 import *
from src.grammars.c_subsetLexer import c_subsetLexer
from src.grammars.c_subsetParser import c_subsetParser
from src.Listener import Listener
import src.AST.init as AST
from src.LLVMErrorListener import MyErrorListener
import src.llvm2mips.llvmToMips as mips
import src.llvm.LLVM as LLVM

# from src.DebugListener import DebugListener


def testFile(argv):
    try:
        file = argv[1]
        input_stream = FileStream(file)
        original = str(input_stream)
        text = copy.deepcopy(original)

        # quick solve for spacing
        replace = False
        for i in range(len(text)):
            c = text[i]
            if c == '"':
                if replace:
                    replace = False
                else:
                    replace = True
            elif replace and c == ' ':
               text = text[:i] + '\w' + text[i+1:]

        text_file = open(file, "w")
        text_file.write(text)
        text_file.close()

        input_stream = FileStream(file)

        text_file = open(file, "w")
        text_file.write(original)
        text_file.close()
    except Exception as e:
        print("\033[1;31;48m", "Error loading file:\n", e)
        exit(1)

    try:
        lexer = c_subsetLexer(input_stream)

        lexer._listeners = [MyErrorListener()]

        stream = CommonTokenStream(lexer)
        parser = c_subsetParser(stream)

        # parser.addErrorListener(errorListener)
        parser.buildParseTrees = True
        try:
            tree = parser.cSyntax()
            if parser._syntaxErrors > 0:
                exit(1)
        except Exception as e:
            print("Parser error: somewhere: {}", e)
            exit(1)
    except Exception as e:
        print("\033[1;31;48m", "Error parsing syntax:\n", e)
        exit(2)

    try:

        listener = Listener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        ast = listener.getAST()
    except Exception as e:
        print("\033[1;31;48m", e)
        exit(3)

    try:
        ast.printDot("derivationTree.dot")
        ast.simplify()
        ast.printDot("AST.dot")
    except Exception as e:
        # raise e
        print("\033[1;31;48m", e)
        exit(4)

    # ast.printDot("derivationTree.dot")
    # ast.simplify()
    # ast.printDot("AST.dot")

    llFile = argv[1].replace(".c", ".ll")

    f = open(llFile, "w+")
    text = ""

    ll = ast.root.toLLVM()
    for obj in ll:
        text += str(obj)

    f.write(text)

    try:
        # give llvm code ll to mipsbuilder:
        mipsbuilder = mips.GlobalBuilder(ll)
        mipsbuilder.build()
        asmFile = argv[1].replace(".c", ".asm")
        mipsbuilder.mipsToFile(asmFile)
    except Exception as e:
        # raise e
        print("\033[1;31;48m", e)
        exit(5)

    return 0


if __name__ == '__main__':
    sys.exit(testFile(sys.argv))
