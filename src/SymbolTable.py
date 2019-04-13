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
    def __init__(self, parent = None):
        self.parent = parent    #parent symbol table
        self.table = dict()

    # add new variable/function
    # returns False if variable already exists in scope
    def insert(self, name, type):
        if(self.table)
        self.table[name] = type

    def search(self, name):
        return 0

    def getParent(self):
        return self.parent

    # return new symbol table with parent self
    def openScope(self):
        return SymbolTable(self)

    def closeScope(self):
        return self.parent
