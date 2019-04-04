from src.grammars.c_subsetListener import *
from src.AST import *
from antlr4 import *

# This class defines a complete listener for a parse tree produced by c_subsetParser.
class Listener(ParseTreeListener):

    def __init__(self):
        self.AST = AST()

    #GET AST FUNCTION
    def getAST(self):
        return self.AST

    #ADDS TERMINALS TO AST
    def addTerminals(self, children):
        for i in range(len(children)):
            if isinstance(children[i], TerminalNode):
                self.AST.addNode(TerNode(children[i].symbol.text), i)

    # Enter a parse tree produced by c_subsetParser#cppSyntax.
    def enterCppSyntax(self, ctx:c_subsetParser.CppSyntaxContext):
        node = ASTNode("Root", len(ctx.children))# root node
        self.AST.nodes.append(node)
        pass

    # Exit a parse tree produced by c_subsetParser#cppSyntax.
    def exitCppSyntax(self, ctx:c_subsetParser.CppSyntaxContext):
        pass

    # Enter a parse tree produced by c_subsetParser#functionSyntax.
    def enterFunctionSyntax(self, ctx: c_subsetParser.FunctionSyntaxContext):
        self.AST.addNode(FuncSyntaxNode(len(ctx.children)))
        self.addTerminals(ctx.children)

    # Exit a parse tree produced by c_subsetParser#functionSyntax.
    def exitFunctionSyntax(self, ctx: c_subsetParser.FunctionSyntaxContext):
        pass

    # Enter a parse tree produced by c_subsetParser#generalStatement.
    def enterGeneralStatement(self, ctx: c_subsetParser.GeneralStatementContext):
        self.AST.addNode(GenStatNode(len(ctx.children)))
        self.addTerminals(ctx.children)

    # Exit a parse tree produced by c_subsetParser#generalStatement.
    def exitGeneralStatement(self, ctx: c_subsetParser.GeneralStatementContext):
        pass

    # Enter a parse tree produced by c_subsetParser#functionStatement.
    def enterFunctionStatement(self, ctx: c_subsetParser.FunctionStatementContext):
        self.AST.addNode(FuncStatNode(len(ctx.children)))

    # Exit a parse tree produced by c_subsetParser#functionStatement.
    def exitFunctionStatement(self, ctx: c_subsetParser.FunctionStatementContext):
        pass

    # Enter a parse tree produced by c_subsetParser#returnStatement.
    def enterReturnStatement(self, ctx: c_subsetParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by c_subsetParser#returnStatement.
    def exitReturnStatement(self, ctx: c_subsetParser.ReturnStatementContext):
        pass

    # Enter a parse tree produced by c_subsetParser#variableDeclaration.
    def enterVariableDeclaration(self, ctx: c_subsetParser.VariableDeclarationContext):
        pass

    # Exit a parse tree produced by c_subsetParser#variableDeclaration.
    def exitVariableDeclaration(self, ctx: c_subsetParser.VariableDeclarationContext):
        pass

    # Enter a parse tree produced by c_subsetParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx: c_subsetParser.FunctionDeclarationContext):
        pass

    # Exit a parse tree produced by c_subsetParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx: c_subsetParser.FunctionDeclarationContext):
        pass

    # Enter a parse tree produced by c_subsetParser#generalDeclaration.
    def enterGeneralDeclaration(self, ctx: c_subsetParser.GeneralDeclarationContext):
        pass

    # Exit a parse tree produced by c_subsetParser#generalDeclaration.
    def exitGeneralDeclaration(self, ctx: c_subsetParser.GeneralDeclarationContext):
        pass

    # Enter a parse tree produced by c_subsetParser#variableDefinition.
    def enterVariableDefinition(self, ctx: c_subsetParser.VariableDefinitionContext):
        pass

    # Exit a parse tree produced by c_subsetParser#variableDefinition.
    def exitVariableDefinition(self, ctx: c_subsetParser.VariableDefinitionContext):
        pass

    # Enter a parse tree produced by c_subsetParser#functionDefinition.
    def enterFunctionDefinition(self, ctx: c_subsetParser.FunctionDefinitionContext):
        self.AST.addNode(FuncDefNode(len(ctx.children)))
        self.addTerminals(ctx.children)

    # Exit a parse tree produced by c_subsetParser#functionDefinition.
    def exitFunctionDefinition(self, ctx: c_subsetParser.FunctionDefinitionContext):
        pass

    # Enter a parse tree produced by c_subsetParser#generalDefinition.
    def enterGeneralDefinition(self, ctx: c_subsetParser.GeneralDefinitionContext):
        pass

    # Exit a parse tree produced by c_subsetParser#generalDefinition.
    def exitGeneralDefinition(self, ctx: c_subsetParser.GeneralDefinitionContext):
        pass

    # Enter a parse tree produced by c_subsetParser#assignment.
    def enterAssignment(self, ctx: c_subsetParser.AssignmentContext):
        self.AST.addNode(AssignNode(len(ctx.children)))
        self.addTerminals(ctx.children)

    # Exit a parse tree produced by c_subsetParser#assignment.
    def exitAssignment(self, ctx: c_subsetParser.AssignmentContext):
        pass

    # Enter a parse tree produced by c_subsetParser#arithmicOperation.
    def enterArithmicOperation(self, ctx: c_subsetParser.ArithmicOperationContext):
        self.AST.addNode(ArOpNode(len(ctx.children)))
        self.addTerminals(ctx.children)

    # Exit a parse tree produced by c_subsetParser#arithmicOperation.
    def exitArithmicOperation(self, ctx: c_subsetParser.ArithmicOperationContext):
        pass

    # Enter a parse tree produced by c_subsetParser#add.
    def enterAdd(self, ctx: c_subsetParser.AddContext):
        pass

    # Exit a parse tree produced by c_subsetParser#add.
    def exitAdd(self, ctx: c_subsetParser.AddContext):
        pass

    # Enter a parse tree produced by c_subsetParser#prod.
    def enterProd(self, ctx: c_subsetParser.ProdContext):
        self.AST.addNode(ProdNode(len(ctx.children)))
        self.addTerminals(ctx.children)

    # Exit a parse tree produced by c_subsetParser#prod.
    def exitProd(self, ctx: c_subsetParser.ProdContext):
        pass

    # Enter a parse tree produced by c_subsetParser#atom.
    def enterAtom(self, ctx: c_subsetParser.AtomContext):
        pass

    # Exit a parse tree produced by c_subsetParser#atom.
    def exitAtom(self, ctx: c_subsetParser.AtomContext):
        pass

    # Enter a parse tree produced by c_subsetParser#conditionalExpression.
    def enterConditionalExpression(self, ctx: c_subsetParser.ConditionalExpressionContext):
        pass

    # Exit a parse tree produced by c_subsetParser#conditionalExpression.
    def exitConditionalExpression(self, ctx: c_subsetParser.ConditionalExpressionContext):
        pass

    # Enter a parse tree produced by c_subsetParser#loop.
    def enterLoop(self, ctx: c_subsetParser.LoopContext):
        pass

    # Exit a parse tree produced by c_subsetParser#loop.
    def exitLoop(self, ctx: c_subsetParser.LoopContext):
        pass

    # Enter a parse tree produced by c_subsetParser#whileLoop.
    def enterWhileLoop(self, ctx: c_subsetParser.WhileLoopContext):
        pass

    # Exit a parse tree produced by c_subsetParser#whileLoop.
    def exitWhileLoop(self, ctx: c_subsetParser.WhileLoopContext):
        pass

    # Enter a parse tree produced by c_subsetParser#ifelseLoop.
    def enterIfelseLoop(self, ctx: c_subsetParser.IfelseLoopContext):
        pass

    # Exit a parse tree produced by c_subsetParser#ifelseLoop.
    def exitIfelseLoop(self, ctx: c_subsetParser.IfelseLoopContext):
        pass

    # Enter a parse tree produced by c_subsetParser#codeBlock.
    def enterCodeBlock(self, ctx: c_subsetParser.CodeBlockContext):
        self.AST.addNode(CodeBlockNode(len(ctx.children)))
        self.addTerminals(ctx.children)

    # Exit a parse tree produced by c_subsetParser#codeBlock.
    def exitCodeBlock(self, ctx: c_subsetParser.CodeBlockContext):
        pass

    # Enter a parse tree produced by c_subsetParser#identifier.
    def enterIdentifier(self, ctx: c_subsetParser.IdentifierContext):
        print(ctx.getText())
        pass

    # Exit a parse tree produced by c_subsetParser#identifier.
    def exitIdentifier(self, ctx: c_subsetParser.IdentifierContext):
        pass

    # Enter a parse tree produced by c_subsetParser#function.
    def enterFunction(self, ctx: c_subsetParser.FunctionContext):
        pass

    # Exit a parse tree produced by c_subsetParser#function.
    def exitFunction(self, ctx: c_subsetParser.FunctionContext):
        pass

    # Enter a parse tree produced by c_subsetParser#functionSignature.
    def enterFunctionSignature(self, ctx: c_subsetParser.FunctionSignatureContext):
        self.AST.addNode(FuncSignNode(len(ctx.children)))
        self.addTerminals(ctx.children)

    # Exit a parse tree produced by c_subsetParser#functionSignature.
    def exitFunctionSignature(self, ctx: c_subsetParser.FunctionSignatureContext):
        pass

    # Enter a parse tree produced by c_subsetParser#variable.
    def enterVariable(self, ctx: c_subsetParser.VariableContext):
        self.AST.addNode(VarNode(ctx.getText()))

    # Exit a parse tree produced by c_subsetParser#variable.
    def exitVariable(self, ctx: c_subsetParser.VariableContext):
        pass

    # Enter a parse tree produced by c_subsetParser#literal.
    def enterLiteral(self, ctx: c_subsetParser.LiteralContext):
        self.AST.addNode(LitNode(ctx.getText()))

    # Exit a parse tree produced by c_subsetParser#literal.
    def exitLiteral(self, ctx: c_subsetParser.LiteralContext):
        pass

    # Enter a parse tree produced by c_subsetParser#typeSpecBase.
    def enterTypeSpecBase(self, ctx: c_subsetParser.TypeSpecBaseContext):
        self.AST.addNode(TypeSpecBaseNode(ctx.getText()))

    # Exit a parse tree produced by c_subsetParser#typeSpecBase.
    def exitTypeSpecBase(self, ctx: c_subsetParser.TypeSpecBaseContext):
        pass

    # Enter a parse tree produced by c_subsetParser#typeSpecPointer.
    def enterTypeSpecPointer(self, ctx: c_subsetParser.TypeSpecPointerContext):
        pass

    # Exit a parse tree produced by c_subsetParser#typeSpecPointer.
    def exitTypeSpecPointer(self, ctx: c_subsetParser.TypeSpecPointerContext):
        pass

    # Enter a parse tree produced by c_subsetParser#typeSpec.
    def enterTypeSpec(self, ctx: c_subsetParser.TypeSpecContext):
        pass

    # Exit a parse tree produced by c_subsetParser#typeSpec.
    def exitTypeSpec(self, ctx: c_subsetParser.TypeSpecContext):
        pass