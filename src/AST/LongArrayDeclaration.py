from .ASTNode import ASTNode
from .Type import Type, POINTER, INT, VOID, ARRAY
from .VarNode import VarNode
from .TerNode import TerNode


class LongArrayDeclNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'LongArrayDecl', maxChildren, ast)
        Type.__init__(self, VOID())