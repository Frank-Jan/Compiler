# Generated from grammars/c_subset.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .c_subsetParser import c_subsetParser
else:
    from c_subsetParser import c_subsetParser

# This class defines a complete listener for a parse tree produced by c_subsetParser.
class c_subsetListener(ParseTreeListener):

    # Enter a parse tree produced by c_subsetParser#expression.
    def enterExpression(self, ctx:c_subsetParser.ExpressionContext):
        pass

    # Exit a parse tree produced by c_subsetParser#expression.
    def exitExpression(self, ctx:c_subsetParser.ExpressionContext):
        pass


