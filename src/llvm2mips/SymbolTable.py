
class Variable:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.register = None
        self.storage = None
        self.changed = True
        self.used = []

    def setStorage(self, storage):
        self.storage = storage
        self.changed = False

    def useful(self, line):
        if len(self.used) == 0:
            return False
        return self.used[-1].line > line    # will be used later

    def nextUse(self, line):
        if not self.useful(line):
            return None
        for l in self.used:
            if l.line >= line:
                return l
        return None

class LockedVar(Variable):
    def __init__(self):
        Variable.__init__(self, None, None)

    def setStorage(self, storage):
        pass

    def useful(self, line):
        return True

    def nextUse(self, line):
        return None

class GP(LockedVar):
    def __init__(self):
        LockedVar.__init__(self)
        self.register = 28


class SP(LockedVar):
    def __init__(self):
        LockedVar.__init__(self)
        self.register = 29


class FP(LockedVar):
    def __init__(self):
        LockedVar.__init__(self)
        self.register = 30


class RA(LockedVar):
    def __init__(self):
        LockedVar.__init__(self)
        self.register = 31


class SymbolTable:

    def __init__(self, parenttable=None):
        self.parent = parenttable
        self.table = dict()

    def size(self):
        return len(self.table)

    def __len__(self):
        return self.table.__len__()

    def get(self, name, default=None):
        var = self.table.get(name, None)
        if var is not None:
            return var
        if self.parent is None:
            return default
        return self.parent.get(name, default)

    def exists(self, name):
        var = self.table.get(name, None)
        if var is not None:
            return True
        if self.parent is None:
            return False
        return self.parent.exists(name)

    def create(self, name, _type):
        var = Variable(name, _type)
        self.table[var.name] = var
        return var
