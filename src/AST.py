from src.ASTNode import *

DEBUG = False

class AST:

    def __init__(self):
        self.nodes = []
        self.id = 0
        self.currentNode = 0
        self.root = None   #ScopeNode (should be from Listener.enterCSyntax())
        self.stdio = False

    def __iter__(self):
        nodes = [self.nodes[0]]  # python-list is a stack

        leftnodes = []
        node = self.nodes[0]  # append = push

        while not len(nodes) == 0:  # while not all nodes are simplified
            node = nodes.pop()  # take last node

            leftnodes.append(node)

            if node.isLeaf():  # if child
                continue

            for child in reversed(node.children):  # traverse childs in reversed order (left-derivation)_
                nodes.append(child)
        self.nodes = leftnodes
        return self

    def __next__(self):
        self.currentNode += 1
        if self.currentNode > len(self.nodes):
            self.currentNode = 0
            raise StopIteration
        return self.nodes[self.currentNode - 1]

    def simplify(self):
        if self.root is not None:
            self.root.simplify()
        self.check()    #final check

    def check(self):
        #TODOremove unused functions
        #TODO: remove unused variables
        #check if used functions are defined
        for node in self.nodes:
            if isinstance(node, ScopeNode):
                #has scope: delete unused items:
                table = node.getSymbolTable()
                for name,record in table.table.items():
                    if record.isUsed and not record.isVar():
                        if record.definition is None:
                            raise Exception("error: function {} is used but not defined".format(name))



    def addNode(self, ASTnode, pos=None):
        prevNode = None
        for i in reversed(range(len(self.nodes))):
            prevNode = self.nodes[i]
            if not prevNode.isLeaf() and not prevNode.hasMaxChildren():
                break
        if pos is None:
            for i in range(len(prevNode.children)):
                if prevNode.children[i] == None:
                    pos = i
                    break
        if pos is None:
            return

        if not prevNode.isLeaf():
            prevNode.children[pos] = ASTnode
            ASTnode.parent = prevNode
        self.nodes.append(ASTnode)

    def getSymbolTable(self):
        return self.root.getSymbolTable()

    def delNode(self, ASTnode):
        if ASTnode.children is not None:
            for child in ASTnode.children:
                self.delNode(child) #delete children to
        if ASTnode in self.nodes:
            self.nodes.remove(ASTnode)

    def printDotDebug(self, filename):
        global DEBUG
        if DEBUG:
            self.printDot(filename)

    def printDot(self, filename):
        f = open(filename, "w")
        graph = "digraph G { \n" \
                "rankdir = TB \n"

        states = ""

        for node in self.nodes:
            node.id = self.id
            self.id += 1

        for node in self.nodes:
            if node.isLeaf():

                states += "\"" + str(node) + "\" " + "[color = \"red\"]\n" + "[label=\"" + str(node.value) + " " + str(type(node)) + "\"]"
            else:
                states += "\"" + str(node) + "\"\n" + "[label=\"" + str(node.value) + "\"]"

            for subnode in node.children:
                graph += "\"" + str(node) + "\" -> \"" + str(subnode) + "\"\n"

        graph += states + '}'
        f.write(graph)
        f.close()
