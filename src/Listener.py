from src.grammars.c_subsetListener import *

# This class defines a complete listener for a parse tree produced by c_subsetParser.
class Listener(c_subsetListener):

    # Enter a parse tree produced by c_subsetParser#expression.
    def enterExpression(self, ctx:c_subsetParser.ExpressionContext):
        pass

    # Exit a parse tree produced by c_subsetParser#expression.
    def exitExpression(self, ctx:c_subsetParser.ExpressionContext):
        ctx.getTokens(0)


    # Enter a parse tree produced by c_subsetParser#declaration.
    def enterDeclaration(self, ctx:c_subsetParser.DeclarationContext):
        pass

    # Exit a parse tree produced by c_subsetParser#declaration.
    def exitDeclaration(self, ctx:c_subsetParser.DeclarationContext):
        pass


    # Enter a parse tree produced by c_subsetParser#definition.
    def enterDefinition(self, ctx:c_subsetParser.DefinitionContext):
        pass

    # Exit a parse tree produced by c_subsetParser#definition.
    def exitDefinition(self, ctx:c_subsetParser.DefinitionContext):
        pass


    # Enter a parse tree produced by c_subsetParser#assignment.
    def enterAssignment(self, ctx:c_subsetParser.AssignmentContext):
        pass

    # Exit a parse tree produced by c_subsetParser#assignment.
    def exitAssignment(self, ctx:c_subsetParser.AssignmentContext):
        pass


    # Enter a parse tree produced by c_subsetParser#ident.
    def enterIdent(self, ctx:c_subsetParser.IdentContext):
        pass

    # Exit a parse tree produced by c_subsetParser#ident.
    def exitIdent(self, ctx:c_subsetParser.IdentContext):
        pass


    # Enter a parse tree produced by c_subsetParser#funcDeclaration.
    def enterFuncDeclaration(self, ctx:c_subsetParser.FuncDeclarationContext):
        pass

    # Exit a parse tree produced by c_subsetParser#funcDeclaration.
    def exitFuncDeclaration(self, ctx:c_subsetParser.FuncDeclarationContext):
        pass


    # Enter a parse tree produced by c_subsetParser#typeSpec.
    def enterTypeSpec(self, ctx:c_subsetParser.TypeSpecContext):
        pass

    # Exit a parse tree produced by c_subsetParser#typeSpec.
    def exitTypeSpec(self, ctx:c_subsetParser.TypeSpecContext):
        pass


