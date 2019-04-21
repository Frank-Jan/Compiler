global id = 0
class VarGen:

    def __init__(self):
        self.name = '%var'

    @staticmethod
    def getNewVar(self):
        global id
        id += 1
        return self.name + str(id)


