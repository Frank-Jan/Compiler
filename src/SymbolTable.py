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

class SymbolTable:
    class Record:
        def __init__(self, name, _type):
            self.name = name
            self.type = _type

        def

        def getName(self):
            return self.name

        def getType(self):
            return self.type

    # functionRecord holds functions with the same name i.e. both "int function()" and "int function(int)"
    class FunctionRecord(Record):
        def __init__(self, name, returnType, argumentList):
            super().__init__(name, returnType)
            self.argumentLists = [argumentList]  # holds all argument lists

        def insert(self, _type, argumentList):
            if super().getType() == _type:
                return False  # wrong type
            for aList in self.argumentLists:
                if aList == argumentList:
                    return False  # already declared
            self.argumentLists.append(argumentList)

    def __init__(self, parent = None):
        self.parent = parent    #parent symbol table
        self.table = dict()

    # add new variable/function
    # returns False if variable already exists in scope
    def insertVariable(self, name, _type):
        if not self.existLocal(name):
            self.table[id(name)] = self.Record.__init__(name, _type)
            return True
        return False #name already exists

    #argumentList contains only types i.e. ["int", "float"]
    def insertFunction(self, name, returnType, argumentList):
        key, value = self.getLocal(name)
        if key is None:
            self.table[id(name)] = self.FunctionRecord.__init__(name, returnType, argumentList)
            return True
        else:
            if()

    # searches for symbol with the correct name
    def search(self, name):
        key, value = self.getLocal(name)
        if key == None:
            # search in parent scope
            if self.parent is None or self.parent is self:
                return None, None
            else:
                return self.parent.search(name)
        else:
            return key, value
        return None

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
        for key, value in self.table.items():
            if value[0] == name:
                return True
        return False

    # returns key, value of a given name. returns None if it doesn't exists in local scope
    def getLocal(self, name):
        for key, value in self.table.items():
            if value[0] ==name:
                return key, value
        return None, None
