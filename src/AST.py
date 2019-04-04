
from src.ASTNode import *



class AST():

    def __init__(self):
        self.nodes = []
        self.id = 0

    def addNode(self, ASTnode, pos = None):
        prevNode = None
        for i in reversed(range(len(self.nodes))):
            prevNode = self.nodes[i]
            if not prevNode.isChild() and not prevNode.hasMaxChildren():
                break

        if pos == None:
            for i in range(len(prevNode.nextNodes)):
                if prevNode.nextNodes[i] == None:
                    pos = i
                    break

        if pos == None:
            raise Exception("POS IS NONE")

        if not prevNode.isChild():
            prevNode.nextNodes[pos] = ASTnode
        self.nodes.append(ASTnode)

    def printDot(self, filename):
        f = open(filename, "w")
        graph = "digraph G { \n" \
                "rankdir = TB \n"

        states = ""

        for node in self.nodes:
            node.id = self.id
            self.id += 1

        for node in self.nodes:
            if node.isChild():
                states += "\"" + str(node) + "\" " + "[color = \"red\"]\n"
            else:
                states += "\"" + str(node) + "\"\n"

            for subnode in node.nextNodes:
                graph += "\"" + str(node) + "\" -> \"" + str(subnode) + "\"\n"


        graph += states + '}'
        f.write(graph)
        f.close()