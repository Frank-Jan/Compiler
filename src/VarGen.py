class VarGen:

    def __init__(self):
        self.name = 'var-'
        self.label = 'Label'
        self.idCounter = 0

    @staticmethod
    def getNewVar(self):
        self.idCounter += 1
        return self.name + str(self.idCounter)

    @staticmethod
    def getNewLabel(self):
        self.idCounter += 1
        return self.label + str(self.idCounter)


