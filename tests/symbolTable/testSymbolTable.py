from src.SymbolTable import SymbolTable, Record, FunctionRecord

def testAccepted():
    table = SymbolTable()

    #tests on inserts and searches
    assert(table.insertVariable("i", ["int"]))

    value = table.search("i")
    assert(value == Record("i", ["int"]))
    assert(not table.insertVariable("i", "float"))
    assert(table.insertVariable("variable", "int"))
    value = table.search("not in table")
    assert(value is None)

    #tests on sub tables
    subTable = table.openScope()
    assert(subTable.getParent() == table)
    value = subTable.getLocal("i")
    assert(value is None)
    value = subTable.search("i")
    assert(not subTable.existLocal("i"))
    assert(table.existLocal("i"))
    assert(subTable.insertFunction("i", "type_i" ,["arg_i"]))
    assert(subTable.insertVariable("v", "type_v"))
    assert(subTable.existLocal("i"))
    assert(subTable.existLocal("v"))
    assert(table.isRoot())
    assert(not subTable.isRoot())
    
def testAll():
    print("Testing symboltable...")
    testAccepted()