class Arg:

    def __init__(self, type, ogName, tempName, lit = False):
        self.type = type #van type TYPES
        self.ogName = ogName
        self.tempName = tempName
        self.lit = lit