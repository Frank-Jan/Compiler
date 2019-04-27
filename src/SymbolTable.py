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
from src.ASTNode import *
ALLSCOPES = []

class Record:
    def __init__(self, _type):
        self.type = _type
        self.llvmName = None
        self.isUsed = False
        self.declarations = []  #all nodes with declarations of this value
        self.definition = None #all nodes with definitions of this value

    def isVar(self):
        return True

    def getType(self):
        return self.type

    def __eq__(self, other):
        if other is None:
            return False
        if(other.isVar()):
            return self.type == other.type
        return False

    def __str__(self):
        return "Var:" + str(self.type)


# functionRecord holds functions with the same name i.e. both "int function()" and "int function(int)"
class FunctionRecord(Record):
    def __init__(self, returnType, argumentList , defined, node):
        super().__init__(returnType)
        self.argumentList = argumentList  # holds all argument lists
        if defined:
            self.definition = node   #node who defined him
        else:
            self.declarations.append(node)  #node who declared function


    def isVar(self):
        return False

    def isDefined(self):
        return self.defined

    def __eq__(self, other):
        if not other.isVar:
            if other.type == self.type:
                return self.argumentList == other.argumentList
        return False

    def __str__(self):
        return "Function: " + str(self.type) + "\t|\t" + str(self.argumentList)

class SymbolTable:
    def __init__(self, parent = None):
        global ALLSCOPES
        ALLSCOPES.append(self)
        self.parent = parent    #parent sy   mbol table
        self.table = dict()

    # add new variable/function
    # returns False if variable already exists in scope
    def insertVariable(self, name, _type, node=None):
        if not self.existLocal(name):
            record = Record(_type)
            self.table[name] = record
            return
        if self.parent is not None:
            raise Exception("Variable already declared or defined")

    # argumentList contains only types i.e. ["int", "float"]
    def defineFunction(self, name, returnType, argumentList, node):
        value =  self.getLocal(name)
        if value is None:
            print("\tvalue is None")
            self.table[name] = FunctionRecord(returnType, argumentList, True, node)   #define function
            return 0
        elif value.isVar():
            raise Exception("Function: {} already declared or defined as variable")
        elif value.defined:
            # functions is already defined
            raise Exception("Function: already declared in this scope")
        else:
            if self.parent == None:
                #global scope: allow multiple declarations with one definition:
                if value.type == returnType and value.argumentList == argumentList:
                    #definition same as declaration
                    value.defined = True
                    value.definition = node
                    # self.table[name] = FunctionRecord(returnType, argumentList, True, node) #define function
                    return 0
                else:
                    #declaration and definition are different
                    raise Exception("Function different signature")
            else:
                # not in global scope: no double declarations or definitions allowed
                raise Exception("Function: already declared or defined in this scope")


    def declareFunction(self, name, returnType, argumentList, node):
        print("\tSymboltable: declare function: ", returnType, " ", name, " ", argumentList)
        value = self.getLocal(name)
        if value is None:
            print("\tvalue is None")
            self.table[name] = FunctionRecord(returnType, argumentList, False, node) #declare function
            return 0
        elif value.isVar():
            print("\tvalue already var")
            raise Exception("Function: already declared or defined as variable in this scope")
            return -1 # name already defined as variable
        elif self.parent is None:
            print("\tglobal scope")
            # global scope: allow multiple declarations with one definition:
            if value.getType() == returnType and value.argumentList == argumentList:
                # declaration same as previous declarations/definition
                # already declared/defined
                value.declarations.append(node)
                return 0
            else:
                print("\tdifferent signature")
                # different function signature
                raise Exception("Function different signature")
                return -2
        elif value.defined:
            print("\tlocal scope & defined already")
            # not in global scope and function already defined
            raise Exception("Function: already defined in this scope")
            return -3
        else:
            print("\tlocal scope && not defined")
            # not in global scope and not yet defined
            # check function signature
            if value.getType() == returnType and value.argumentList == value.argumentList:
                # declaration same as previous declarations/definition
                # already declared/defined
                value.declarations.append(node)
                return 0
            else:
                # different function signature
                print("\tdifferent signature")
                raise Exception("Function: already declared with different signature")
                return -2

    #removes local record
    def remove(self, name):
        self.table.pop(name, None)

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
        for key,value in self.table.items():
            string += '\n{:<20}|{:<20}|{:<5}|{:<5}'.format(str(key), str(value),str(len(value.declarations)),str(value.definition is not None))
        return string
