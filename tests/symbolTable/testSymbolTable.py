from src.SymbolTable import SymbolTable

def testAccepted():
    table = SymbolTable()

    #tests on inserts and searches
    assert(table.insert("i", ["int"]))

    key, value = table.search("i")
    assert(value == ["i", ["int"]])
    assert(not table.insert("i", ["float"]))
    assert(table.insert("func", ["function", "int"]))
    key, value = table.search("not in table")
    assert(key is None and value is None)

    #tests on sub tables
    subTable = table.openScope()
    assert(subTable.getParent() == table)
    key, value = subTable.getLocal("i")
    assert(key is None and value is None)
    key, value = subTable.search("i")
    assert(value == ["i", ["int"]])
    assert(not subTable.existLocal("i"))
    assert(table.existLocal("i"))
    assert(subTable.insert("i", ["float"]))
    assert(subTable.existLocal("i"))
    assert(table.isRoot())
    assert(not subTable.isRoot())


def testAll():
    print("Testing symboltable...")
    testAccepted()