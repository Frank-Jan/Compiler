
class VarGen:

    def __init__(self):
        self.name = '%var'
        self.id = 0

    @staticmethod
    def getNewVar(self):
        return self.name + str(self.id)


