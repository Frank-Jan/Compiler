from src.ASTNode import *


class AST:

    def __init__(self):
        self.nodes = []
        self.id = 0
        self.currentNode = 0
        self.root = None   #ScopeNode (should be from Listener.enterCSyntax())

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
        if not self.root is None:
            self.root.simplify()
        # nodes = []  # python-list is a stack
        #
        # nodes.append(self.nodes[0])  # append = push
        # filename = "tmp";
        # ex = ".dot"
        # i = 0
        # print("----------------------")
        # for n in nodes:
        #     print(type(n))
        # print("----------------------")
        # while not len(nodes) == 0:  # while not all nodes are simplified
        #     i += 1
        #     node = nodes[-1]  # take last node
        #     print("Simplifying nr:", i, " node: ", type(node))
        #     if node.isSimplified:  # if node is simplified: skip this one
        #         nodes.pop()
        #         continue
        #     elif node.isLeaf() or node.timeToSimplify():  # if childs are simplified parent may be simplified
        #         node.simplify()  # child node is already simplified
        #         nodes.pop()
        #
        #     for child in reversed(node.children):  # traverse childs in reversed order (left-derivation)_
        #         nodes.append(child)
        #
        #     self.printDot(filename + str(i) + ex);

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
            print("POS IS NONE")
            for node in self:
                print(node)
            return
            # raise Exception("POS IS NONE")

        if not prevNode.isLeaf():
            prevNode.children[pos] = ASTnode
            ASTnode.parent = (prevNode, pos)
        self.nodes.append(ASTnode)

    def generateSymbolTable(self):
        self.root.fillSymbolTable()
        pass

    def delNode(self, ASTnode):
        if ASTnode.children is not None:
            for child in ASTnode.children:
                self.delNode(child) #delete children to
        if ASTnode in self.nodes:
            self.nodes.remove(ASTnode)

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
                states += "\"" + str(node) + "\" " + "[color = \"red\"]\n" + "[label=\"" + str(node.value) + "\"]"
            else:
                states += "\"" + str(node) + "\"\n" + "[label=\"" + str(node.value) + "\"]"

            for subnode in node.children:
                graph += "\"" + str(node) + "\" -> \"" + str(subnode) + "\"\n"

        graph += states + '}'
        f.write(graph)
        f.close()
