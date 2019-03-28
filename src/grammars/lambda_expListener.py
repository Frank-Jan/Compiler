# Generated from grammars/lambda_exp.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .lambda_expParser import lambda_expParser
else:
    from lambda_expParser import lambda_expParser

# This class defines a complete listener for a parse tree produced by lambda_expParser.
class lambda_expListener(ParseTreeListener):

    # Enter a parse tree produced by lambda_expParser#expression.
    def enterExpression(self, ctx:lambda_expParser.ExpressionContext):
        pass

    # Exit a parse tree produced by lambda_expParser#expression.
    def exitExpression(self, ctx:lambda_expParser.ExpressionContext):
        pass


    # Enter a parse tree produced by lambda_expParser#function.
    def enterFunction(self, ctx:lambda_expParser.FunctionContext):
        pass

    # Exit a parse tree produced by lambda_expParser#function.
    def exitFunction(self, ctx:lambda_expParser.FunctionContext):
        pass


    # Enter a parse tree produced by lambda_expParser#application.
    def enterApplication(self, ctx:lambda_expParser.ApplicationContext):
        pass

    # Exit a parse tree produced by lambda_expParser#application.
    def exitApplication(self, ctx:lambda_expParser.ApplicationContext):
        pass


