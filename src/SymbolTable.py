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
    def __init__(self, name, _type):
        self.name = name
        self.type = _type
        self.isVar = True

    def isVar(self):
        return self.isVar

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def __eq__(self, other):
        return (other.name == self.name and self.type == other.type and self.isVar == other.isVar)

    def __str__(self):
        return "Variable: name: " + str(self.name) + "\t| Type: " + str(self.type)


# functionRecord holds functions with the same name i.e. both "int function()" and "int function(int)"
class FunctionRecord(Record):
    def __init__(self, name, returnType, argumentList):
        super().__init__(name, returnType)
        self.argumentLists = [argumentList]  # holds all argument lists
        self.isVar = False

    def insert(self, _type, argumentList):
        if super().getType() == _type:
            return False  # wrong type
        for aList in self.argumentLists:
            if aList == argumentList:
                return False  # already declared
        self.argumentLists.append(argumentList)
        return True

    def __str__(self):
        return "Function name: " + self.name + "\t| Return Type: " + self.type

class SymbolTable:
    def __init__(self, parent = None):
        self.parent = parent    #parent symbol table
        self.table = dict()


    # add new variable/function
    # returns False if variable already exists in scope
    def insertVariable(self, name, _type):
        if not self.existLocal(name):
            self.table[id(name)] = Record(name, _type)
            return True
        return False #name already exists

    # argumentList contains only types i.e. ["int", "float"]
    def insertFunction(self, name, returnType, argumentList):
        value = self.getLocal(name)
        if value is None:
            self.table[id(name)] = FunctionRecord(name, returnType, argumentList)
            return True
        else:
            if value.isVar():
                return False    # name already taken by a variable
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
    def openScope(self):
        return SymbolTable(self)

    def closeScope(self):
        return self.parent

    def isRoot(self):
        return self.parent is None or self.parent is self

    # checks if name already exists in local scope
    def existLocal(self, name):
        return self.table.get(id(name)) is not None

    # returns key, value of a given name. returns None if it doesn't exists in local scope
    def getLocal(self, name):
        return self.table.get(id(name))

    def __str__(self):
        string = "SYMBOLTABLE:\t" + str(id(self))
        string += "\nPARENT:\t\t\t" + str(id(self.parent))
        for key, value in self.table.items():
            string += "\n" + str(key) + "\t|" + str(value)
        return string
