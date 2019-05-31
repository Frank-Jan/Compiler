from .ASTNode import ASTNode
from .Type import Type, POINTER, INT, VOID, ARRAY
from .VarNode import VarNode
from .TerNode import TerNode


class ShortArrayDeclNode(ASTNode, Type):

    def __init__(self, maxChildren, ast):
        ASTNode.__init__(self, 'ShortArrayDecl', maxChildren, ast)
        Type.__init__(self, VOID())