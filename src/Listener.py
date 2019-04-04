# Generated from grammars/c_subset.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .c_subsetParser import c_subsetParser
else:
    from c_subsetParser import c_subsetParser

# This class defines a complete listener for a parse tree produced by c_subsetParser.
class c_subsetListener(ParseTreeListener):

    # Enter a parse tree produced by c_subsetParser#cppSyntax.
    def enterCppSyntax(self, ctx:c_subsetParser.CppSyntaxContext):
        pass

    # Exit a parse tree produced by c_subsetParser#cppSyntax.
    def exitCppSyntax(self, ctx:c_subsetParser.CppSyntaxContext):
        pass


    # Enter a parse tree produced by c_subsetParser#functionSyntax.
    def enterFunctionSyntax(self, ctx:c_subsetParser.FunctionSyntaxContext):
        pass

    # Exit a parse tree produced by c_subsetParser#functionSyntax.
    def exitFunctionSyntax(self, ctx:c_subsetParser.FunctionSyntaxContext):
        pass


    # Enter a parse tree produced by c_subsetParser#generalStatement.
    def enterGeneralStatement(self, ctx:c_subsetParser.GeneralStatementContext):
        pass

    # Exit a parse tree produced by c_subsetParser#generalStatement.
    def exitGeneralStatement(self, ctx:c_subsetParser.GeneralStatementContext):
        pass


    # Enter a parse tree produced by c_subsetParser#functionStatement.
    def enterFunctionStatement(self, ctx:c_subsetParser.FunctionStatementContext):
        pass

    # Exit a parse tree produced by c_subsetParser#functionStatement.
    def exitFunctionStatement(self, ctx:c_subsetParser.FunctionStatementContext):
        pass


    # Enter a parse tree produced by c_subsetParser#returnStatement.
    def enterReturnStatement(self, ctx:c_subsetParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by c_subsetParser#returnStatement.
    def exitReturnStatement(self, ctx:c_subsetParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by c_subsetParser#include.
    def enterInclude(self, ctx:c_subsetParser.IncludeContext):
        pass

    # Exit a parse tree produced by c_subsetParser#include.
    def exitInclude(self, ctx:c_subsetParser.IncludeContext):
        pass


    # Enter a parse tree produced by c_subsetParser#variableDeclaration.
    def enterVariableDeclaration(self, ctx:c_subsetParser.VariableDeclarationContext):
        pass

    # Exit a parse tree produced by c_subsetParser#variableDeclaration.
    def exitVariableDeclaration(self, ctx:c_subsetParser.VariableDeclarationContext):
        pass


    # Enter a parse tree produced by c_subsetParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx:c_subsetParser.FunctionDeclarationContext):
        pass

    # Exit a parse tree produced by c_subsetParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx:c_subsetParser.FunctionDeclarationContext):
        pass


    # Enter a parse tree produced by c_subsetParser#generalDeclaration.
    def enterGeneralDeclaration(self, ctx:c_subsetParser.GeneralDeclarationContext):
        pass

    # Exit a parse tree produced by c_subsetParser#generalDeclaration.
    def exitGeneralDeclaration(self, ctx:c_subsetParser.GeneralDeclarationContext):
        pass


    # Enter a parse tree produced by c_subsetParser#variableDefinition.
    def enterVariableDefinition(self, ctx:c_subsetParser.VariableDefinitionContext):
        pass

    # Exit a parse tree produced by c_subsetParser#variableDefinition.
    def exitVariableDefinition(self, ctx:c_subsetParser.VariableDefinitionContext):
        pass


    # Enter a parse tree produced by c_subsetParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:c_subsetParser.FunctionDefinitionContext):
        pass

    # Exit a parse tree produced by c_subsetParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:c_subsetParser.FunctionDefinitionContext):
        pass


    # Enter a parse tree produced by c_subsetParser#generalDefinition.
    def enterGeneralDefinition(self, ctx:c_subsetParser.GeneralDefinitionContext):
        pass

    # Exit a parse tree produced by c_subsetParser#generalDefinition.
    def exitGeneralDefinition(self, ctx:c_subsetParser.GeneralDefinitionContext):
        pass


    # Enter a parse tree produced by c_subsetParser#assignment.
    def enterAssignment(self, ctx:c_subsetParser.AssignmentContext):
        pass

    # Exit a parse tree produced by c_subsetParser#assignment.
    def exitAssignment(self, ctx:c_subsetParser.AssignmentContext):
        pass


    # Enter a parse tree produced by c_subsetParser#arithmicOperation.
    def enterArithmicOperation(self, ctx:c_subsetParser.ArithmicOperationContext):
        pass

    # Exit a parse tree produced by c_subsetParser#arithmicOperation.
    def exitArithmicOperation(self, ctx:c_subsetParser.ArithmicOperationContext):
        pass


    # Enter a parse tree produced by c_subsetParser#add.
    def enterAdd(self, ctx:c_subsetParser.AddContext):
        pass

    # Exit a parse tree produced by c_subsetParser#add.
    def exitAdd(self, ctx:c_subsetParser.AddContext):
        pass


    # Enter a parse tree produced by c_subsetParser#prod.
    def enterProd(self, ctx:c_subsetParser.ProdContext):
        pass

    # Exit a parse tree produced by c_subsetParser#prod.
    def exitProd(self, ctx:c_subsetParser.ProdContext):
        pass


    # Enter a parse tree produced by c_subsetParser#atom.
    def enterAtom(self, ctx:c_subsetParser.AtomContext):
        pass

    # Exit a parse tree produced by c_subsetParser#atom.
    def exitAtom(self, ctx:c_subsetParser.AtomContext):
        pass


    # Enter a parse tree produced by c_subsetParser#conditionalExpression.
    def enterConditionalExpression(self, ctx:c_subsetParser.ConditionalExpressionContext):
        pass

    # Exit a parse tree produced by c_subsetParser#conditionalExpression.
    def exitConditionalExpression(self, ctx:c_subsetParser.ConditionalExpressionContext):
        pass


    # Enter a parse tree produced by c_subsetParser#loop.
    def enterLoop(self, ctx:c_subsetParser.LoopContext):
        pass

    # Exit a parse tree produced by c_subsetParser#loop.
    def exitLoop(self, ctx:c_subsetParser.LoopContext):
        pass


    # Enter a parse tree produced by c_subsetParser#whileLoop.
    def enterWhileLoop(self, ctx:c_subsetParser.WhileLoopContext):
        pass

    # Exit a parse tree produced by c_subsetParser#whileLoop.
    def exitWhileLoop(self, ctx:c_subsetParser.WhileLoopContext):
        pass


    # Enter a parse tree produced by c_subsetParser#ifelseLoop.
    def enterIfelseLoop(self, ctx:c_subsetParser.IfelseLoopContext):
        pass

    # Exit a parse tree produced by c_subsetParser#ifelseLoop.
    def exitIfelseLoop(self, ctx:c_subsetParser.IfelseLoopContext):
        pass


    # Enter a parse tree produced by c_subsetParser#codeBlock.
    def enterCodeBlock(self, ctx:c_subsetParser.CodeBlockContext):
        pass

    # Exit a parse tree produced by c_subsetParser#codeBlock.
    def exitCodeBlock(self, ctx:c_subsetParser.CodeBlockContext):
        pass


    # Enter a parse tree produced by c_subsetParser#identifier.
    def enterIdentifier(self, ctx:c_subsetParser.IdentifierContext):
        pass

    # Exit a parse tree produced by c_subsetParser#identifier.
    def exitIdentifier(self, ctx:c_subsetParser.IdentifierContext):
        pass


    # Enter a parse tree produced by c_subsetParser#dereference.
    def enterDereference(self, ctx:c_subsetParser.DereferenceContext):
        pass

    # Exit a parse tree produced by c_subsetParser#dereference.
    def exitDereference(self, ctx:c_subsetParser.DereferenceContext):
        pass


    # Enter a parse tree produced by c_subsetParser#reference.
    def enterReference(self, ctx:c_subsetParser.ReferenceContext):
        pass

    # Exit a parse tree produced by c_subsetParser#reference.
    def exitReference(self, ctx:c_subsetParser.ReferenceContext):
        pass


    # Enter a parse tree produced by c_subsetParser#function.
    def enterFunction(self, ctx:c_subsetParser.FunctionContext):
        pass

    # Exit a parse tree produced by c_subsetParser#function.
    def exitFunction(self, ctx:c_subsetParser.FunctionContext):
        pass


    # Enter a parse tree produced by c_subsetParser#functionSignature.
    def enterFunctionSignature(self, ctx:c_subsetParser.FunctionSignatureContext):
        pass

    # Exit a parse tree produced by c_subsetParser#functionSignature.
    def exitFunctionSignature(self, ctx:c_subsetParser.FunctionSignatureContext):
        pass


    # Enter a parse tree produced by c_subsetParser#variable.
    def enterVariable(self, ctx:c_subsetParser.VariableContext):
        pass

    # Exit a parse tree produced by c_subsetParser#variable.
    def exitVariable(self, ctx:c_subsetParser.VariableContext):
        pass


    # Enter a parse tree produced by c_subsetParser#literal.
    def enterLiteral(self, ctx:c_subsetParser.LiteralContext):
        pass

    # Exit a parse tree produced by c_subsetParser#literal.
    def exitLiteral(self, ctx:c_subsetParser.LiteralContext):
        pass


    # Enter a parse tree produced by c_subsetParser#integer.
    def enterInteger(self, ctx:c_subsetParser.IntegerContext):
        pass

    # Exit a parse tree produced by c_subsetParser#integer.
    def exitInteger(self, ctx:c_subsetParser.IntegerContext):
        pass


    # Enter a parse tree produced by c_subsetParser#typeSpecPointer.
    def enterTypeSpecPointer(self, ctx:c_subsetParser.TypeSpecPointerContext):
        pass

    # Exit a parse tree produced by c_subsetParser#typeSpecPointer.
    def exitTypeSpecPointer(self, ctx:c_subsetParser.TypeSpecPointerContext):
        pass


    # Enter a parse tree produced by c_subsetParser#typeSpec.
    def enterTypeSpec(self, ctx:c_subsetParser.TypeSpecContext):
        pass

    # Exit a parse tree produced by c_subsetParser#typeSpec.
    def exitTypeSpec(self, ctx:c_subsetParser.TypeSpecContext):
        pass


    # Enter a parse tree produced by c_subsetParser#typeSpecBase.
    def enterTypeSpecBase(self, ctx:c_subsetParser.TypeSpecBaseContext):
        pass

    # Exit a parse tree produced by c_subsetParser#typeSpecBase.
    def exitTypeSpecBase(self, ctx:c_subsetParser.TypeSpecBaseContext):
        pass


