from tests.grammar.testAccepted import testAll as testGrammar
from tests.symbolTable.testSymbolTable import testAll as testSymbolTable

def testAll():
    print("starting tests")
    testGrammar()
    #testSymbolTable()
    print("Done...")
    return 0


def testDeclarations():
    print("not implemented yet")

if __name__ == "__main__":
    testAll()
