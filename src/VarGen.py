class VarGen:

    def __init__(self):
        self.name = '%var'
        self.idCounter = 0

    @staticmethod
    def getNewVar(self):
        self.idCounter += 1
        return self.name + str(self.idCounter)


