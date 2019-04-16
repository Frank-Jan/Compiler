"""
symbol table:
insert
search(ID)/search(NAME)
layout: ID|NAME|TYPE|ACCESS
ID: unique
parent table reference
call parent
//error: throw exception
"""


class Record:
    def __init__(self, _type):
        self.type = _type

    def isVar(self):
        return True

    def getType(self):
        return self.type

    def __eq__(self, other):
        if(other.isVar):
            return self.type == other.type
        return False

    def __str__(self):
        return "Var Type: " + str(self.type)


# functionRecord holds functions with the same name i.e. both "int function()" and "int function(int)"
class FunctionRecord(Record):
    def __init__(self, returnType, argumentList):
        super().__init__(returnType)
        self.argumentList = argumentList  # holds all argument lists

    def isVar(self):
        return False

    def __eq__(self, other):
        if not other.isVar:
            if other.type == self.type:
                return self.argumentList == other.argumentList
        return False

    def __str__(self):
        return "Fun Type: " + self.type + "\t| Arguments: \t" + str(self.argumentList)

class SymbolTable:
    def __init__(self, parent = None):
        self.parent = parent    #parent symbol table
        self.table = dict()

    # add new variable/function
    # returns False if variable already exists in scope
    def insertVariable(self, name, _type):
        if not self.existLocal(name):
            self.table[name] = Record(_type)
            return True
        return False #name already exists

    # argumentList contains only types i.e. ["int", "float"]
    def insertFunction(self, name, returnType, argumentList):
        value = self.getLocal(name)
        if value is None:
            self.table[name] = FunctionRecord(returnType, argumentList)
            return True
        elif value.isVar():
            return False  # name already taken by a variable
        else:
            return value.insert(returnType, argumentList)

    # searches for symbol with the correct name
    def search(self, name):
        value = self.getLocal(name)
        if value is None:
            # search in parent scope
            if self.parent is None or self.parent is self:
                return None
            else:
                return self.parent.search(name)
        else:
            return value

    def getParent(self):
        return self.parent

    # return new symbol table with parent self
    def openScope(self, listVariables = None):
        s = SymbolTable(self)
        if listVariables is None:
            return s
        for varTuple in listVariables:
            s.insertVariable(varTuple[1], varTuple[0])
        return SymbolTable(self)

    def closeScope(self):
        return self.parent

    def isRoot(self):
        return self.parent is None or self.parent is self

    # checks if name already exists in local scope
    def existLocal(self, name):
        return self.table.get(name) is not None

    # returns key, value of a given name. returns None if it doesn't exists in local scope
    def getLocal(self, name):
        return self.table.get(name)

    def __str__(self):
        string = "SYMBOLTABLE:\t" + str(id(self))
        string += "\nPARENT:\t\t\t" + str(id(self.parent))
        for key, value in self.table.items():
            string += "\n" + str(key) + "\t|" + str(value)
        return string
