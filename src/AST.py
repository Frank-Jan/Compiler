
from src.ASTNode import *



class AST():

    def __init__(self):
        self.nodes = []
        self.id = 0

    def simplify(self):
        # prevNode = None
        nodes = [self.nodes[0]]
        for node in nodes:
            i = 0
            while i < len(node.nextNodes):
                node.nextNodes[i].simplify(node, i)
                if not node.nextNodes[i].simplified:
                    continue
                else:
                    nodes.append(node.nextNodes[i])
                    i += 1

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
            print("POS IS NONE")
            return
            #raise Exception("POS IS NONE")

        if not prevNode.isChild():
            prevNode.nextNodes[pos] = ASTnode
        self.nodes.append(ASTnode)

    def delNode(self, ASTNode):
        try:
            nextNodes = ASTNode.nextNodes #check voor copy
            self.nodes.remove(ASTNode)
            return nextNodes
        except:
            return


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