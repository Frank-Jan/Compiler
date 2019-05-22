class Alloca:

    def __init__(self, result, type, align=4):
        self.result = result
        self.type = type
        self.align = align

    def __str__(self):
        return str(self.result) + " = alloca " + str(self.type) + ", align " + str(self.align) + "\n"


class Store:

    def __init__(self, type, val1, val2, align=4):
        self.type = type
        self.val1 = val1
        self.val2 = val2
        self.align = align

    def __str__(self):
        return "store " + str(self.type) + " " + str(self.val1) + ", " + str(self.type) + "* " + str(
            self.val2) + ", " + str(self.align) + "\n"


class Load:

    def __init__(self, result, type, var, align=4):
        self.result = result
        self.type = type
        self.var = var
        self.align = align

    def __str__(self):
        return str(self.result) + " = load " + str(self.type) + ", " + str(self.type) + "* " + str(
            self.var) + ", align " + str(self.align) + "\n"


# ARITHMETIC
########################################################################
class Arithmetic:

    def __init__(self, result, op, type, val1, val2):
        self.result = result
        self.op = op
        self.type = type
        self.val1 = val1
        self.val2 = val2

    def __str__(self):
        return str(self.result) + " = " + str(self.op) + " " + str(self.type) + " " + str(self.val1) + ", " + str(
            self.val2) + "\n"


class Add(Arithmetic):

    def __init__(self, result, type, val1, val2):
        Arithmetic.__init__(result, "add", type, val1, val2)


class Sub(Arithmetic):

    def __init__(self, result, type, val1, val2):
        Arithmetic.__init__(result, "sub", type, val1, val2)


class Mull(Arithmetic):

    def __init__(self, result, type, val1, val2):
        Arithmetic.__init__(result, "mull", type, val1, val2)


class Div(Arithmetic):

    def __init__(self, result, type, val1, val2):
        Arithmetic.__init__(result, "sdiv", type, val1, val2)
########################################################################
