from src.grammars.c_subsetListener import *
from src.AST import *
from antlr4 import *


# This class defines a complete listener for a parse tree produced by c_subsetParser.
class Listener(c_subsetListener):

    def __init__(self):
        self.AST = AST()

    # GET AST FUNCTION
    def getAST(self):
        return self.AST

    # ADDS TERMINALS TO AST
    def addTerminals(self, children, pos):
        if children is None:
            return

        for i in range(len(children)):
            if isinstance(children[i], TerminalNode):
                node = TerNode(children[i].symbol.text, self.AST, pos)
                if not(toType(node.value) is None):
                    node.isType = True
                self.AST.addNode(node, i)

    # Enter a parse tree produced by c_subsetParser#cppSyntax.
    def enterCSyntax(self, ctx: c_subsetParser.CSyntaxContext):
        children = 0
        if not (ctx.children is None):
            children = len(ctx.children)
        node = RootNode("Root", children, self.AST)
        self.AST.nodes.append(node)
        self.AST.root = node
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#cppSyntax.
    def exitCSyntax(self, ctx: c_subsetParser.CSyntaxContext):
        pass

    # Enter a parse tree produced by c_subsetParser#functionSyntax.
    def enterFunctionSyntax(self, ctx: c_subsetParser.FunctionSyntaxContext):
        numberChildren = 0
        if not (ctx.children is None):
            numberChildren = len(ctx.children)
        self.AST.addNode(FuncSyntaxNode(numberChildren, self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#functionSyntax.
    def exitFunctionSyntax(self, ctx: c_subsetParser.FunctionSyntaxContext):
        pass

    # Enter a parse tree produced by c_subsetParser#generalStatement.
    def enterGeneralStatement(self, ctx: c_subsetParser.GeneralStatementContext):
        self.AST.addNode(GenStatNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#generalStatement.
    def exitGeneralStatement(self, ctx: c_subsetParser.GeneralStatementContext):
        pass

    # Enter a parse tree produced by c_subsetParser#functionStatement.
    def enterFunctionStatement(self, ctx: c_subsetParser.FunctionStatementContext):
        self.AST.addNode(FuncStatNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#functionStatement.
    def exitFunctionStatement(self, ctx: c_subsetParser.FunctionStatementContext):
        pass

    # Enter a parse tree produced by c_subsetParser#returnStatement.
    def enterReturnStatement(self, ctx: c_subsetParser.ReturnStatementContext):
        self.AST.addNode(ReturnStatNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#returnStatement.
    def exitReturnStatement(self, ctx: c_subsetParser.ReturnStatementContext):
        pass

    # Enter a parse tree produced by c_subsetParser#variableDefinition.
    def enterVariableDefinition(self, ctx: c_subsetParser.VariableDefinitionContext):
        self.AST.addNode(VarDefNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#variableDefinition.
    def exitVariableDefinition(self, ctx: c_subsetParser.VariableDefinitionContext):
        pass

    # Enter a parse tree produced by c_subsetParser#functionDefinition.
    def enterFunctionDefinition(self, ctx: c_subsetParser.FunctionDefinitionContext):
        self.AST.addNode(FuncDefNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#functionDefinition.
    def exitFunctionDefinition(self, ctx: c_subsetParser.FunctionDefinitionContext):
        pass

    # Enter a parse tree produced by c_subsetParser#functionSignatureDefinition.
    def enterFunctionSignatureDefinition(self, ctx:c_subsetParser.FunctionSignatureDefinitionContext):
        self.AST.addNode(FuncSignDefNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#functionSignatureDefinition.
    def exitFunctionSignatureDefinition(self, ctx:c_subsetParser.FunctionSignatureDefinitionContext):
        pass

    # Enter a parse tree produced by c_subsetParser#generalDefinition.
    def enterGeneralDefinition(self, ctx: c_subsetParser.GeneralDefinitionContext):
        self.AST.addNode(GenDefNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#generalDefinition.
    def exitGeneralDefinition(self, ctx: c_subsetParser.GeneralDefinitionContext):
        pass

    # Enter a parse tree produced by c_subsetParser#variableDeclaration.
    def enterVariableDeclaration(self, ctx: c_subsetParser.VariableDeclarationContext):
        self.AST.addNode(VarDeclNode(len(ctx.children), self.AST))

        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#variableDeclaration.
    def exitVariableDeclaration(self, ctx: c_subsetParser.VariableDeclarationContext):
        pass

    # Enter a parse tree produced by c_subsetParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx: c_subsetParser.FunctionDeclarationContext):
        self.AST.addNode(FuncDeclNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx: c_subsetParser.FunctionDeclarationContext):
        pass

    # Enter a parse tree produced by c_subsetParser#generalDeclaration.
    def enterGeneralDeclaration(self, ctx: c_subsetParser.GeneralDeclarationContext):
        self.AST.addNode(GenDeclNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#generalDeclaration.
    def exitGeneralDeclaration(self, ctx: c_subsetParser.GeneralDeclarationContext):
        pass

    # Enter a parse tree produced by c_subsetParser#assignRight.
    def enterAssignRight(self, ctx:c_subsetParser.AssignRightContext):
        self.AST.addNode(AssignRightNode(self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#assignRight.
    def exitAssignRight(self, ctx:c_subsetParser.AssignRightContext):
        pass

    # Enter a parse tree produced by c_subsetParser#assignment.
    def enterAssignment(self, ctx: c_subsetParser.AssignmentContext):
        self.AST.addNode(AssignNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#assignment.
    def exitAssignment(self, ctx: c_subsetParser.AssignmentContext):
        pass

    # Enter a parse tree produced by c_subsetParser#arithmeticOperation.
    def enterArithmeticOperation(self, ctx: c_subsetParser.ArithmeticOperationContext):
        self.AST.addNode(ArOpNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#arithmeticOperation.
    def exitArithmeticOperation(self, ctx: c_subsetParser.ArithmeticOperationContext):
        pass

    # Enter a parse tree produced by c_subsetParser#add.
    def enterAdd(self, ctx: c_subsetParser.AddContext):
        self.AST.addNode(AddNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#add.
    def exitAdd(self, ctx: c_subsetParser.AddContext):
        pass

    # Enter a parse tree produced by c_subsetParser#prod.
    def enterProd(self, ctx: c_subsetParser.ProdContext):
        self.AST.addNode(ProdNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#prod.
    def exitProd(self, ctx: c_subsetParser.ProdContext):
        pass

    # Enter a parse tree produced by c_subsetParser#atom.
    def enterAtom(self, ctx: c_subsetParser.AtomContext):
        self.AST.addNode(AtomNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#atom.
    def exitAtom(self, ctx: c_subsetParser.AtomContext):
        pass

    # Enter a parse tree produced by c_subsetParser#conditionalExpression.
    def enterConditionalExpression(self, ctx: c_subsetParser.ConditionalExpressionContext):
        self.AST.addNode(CondExpNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#conditionalExpression.
    def exitConditionalExpression(self, ctx: c_subsetParser.ConditionalExpressionContext):
        pass

    # Enter a parse tree produced by c_subsetParser#loop.
    def enterLoop(self, ctx: c_subsetParser.LoopContext):
        self.AST.addNode(LoopNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#loop.
    def exitLoop(self, ctx: c_subsetParser.LoopContext):
        pass

    # Enter a parse tree produced by c_subsetParser#whileLoop.
    def enterWhileLoop(self, ctx: c_subsetParser.WhileLoopContext):
        self.AST.addNode(WhileNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#whileLoop.
    def exitWhileLoop(self, ctx: c_subsetParser.WhileLoopContext):
        pass

    # Enter a parse tree produced by c_subsetParser#ifelseLoop.
    def enterIfelseLoop(self, ctx: c_subsetParser.IfelseLoopContext):
        self.AST.addNode(IfElseNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#ifelseLoop.
    def exitIfelseLoop(self, ctx: c_subsetParser.IfelseLoopContext):
        pass

    # Enter a parse tree produced by c_subsetParser#codeBlock.
    def enterCodeBlock(self, ctx: c_subsetParser.CodeBlockContext):
        self.AST.addNode(CodeBlockNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#codeBlock.
    def exitCodeBlock(self, ctx: c_subsetParser.CodeBlockContext):
        pass

    # Enter a parse tree produced by c_subsetParser#value.
    def enterValue(self, ctx:c_subsetParser.ValueContext):
        self.AST.addNode(ValueNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))
        pass

    # Exit a parse tree produced by c_subsetParser#value.
    def exitValue(self, ctx:c_subsetParser.ValueContext):
        pass

    # Enter a parse tree produced by c_subsetParser#lvalue.
    def enterLvalue(self, ctx:c_subsetParser.LvalueContext):
        self.AST.addNode(LvalueNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))
        pass

    # Exit a parse tree produced by c_subsetParser#lvalue.
    def exitLvalue(self, ctx:c_subsetParser.LvalueContext):
        pass

    # Enter a parse tree produced by c_subsetParser#rvalue.
    def enterRvalue(self, ctx:c_subsetParser.RvalueContext):
        self.AST.addNode(RvalueNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))
        pass

    # Exit a parse tree produced by c_subsetParser#rvalue.
    def exitRvalue(self, ctx:c_subsetParser.RvalueContext):
        pass

    # Enter a parse tree produced by c_subsetParser#function.
    def enterFunction(self, ctx: c_subsetParser.FunctionContext):
        self.AST.addNode(FuncNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#function.
    def exitFunction(self, ctx: c_subsetParser.FunctionContext):
        pass

    # Enter a parse tree produced by c_subsetParser#functionSignature.
    def enterFunctionSignature(self, ctx: c_subsetParser.FunctionSignatureContext):
        self.AST.addNode(FuncSignNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#functionSignature.
    def exitFunctionSignature(self, ctx: c_subsetParser.FunctionSignatureContext):
        pass

    # Enter a parse tree produced by c_subsetParser#variable.
    def enterVariable(self, ctx: c_subsetParser.VariableContext):
        self.AST.addNode(VarNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#variable.
    def exitVariable(self, ctx: c_subsetParser.VariableContext):
        pass

    # Enter a parse tree produced by c_subsetParser#literal.
    def enterLiteral(self, ctx: c_subsetParser.LiteralContext):
        self.AST.addNode(LitNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#literal.
    def exitLiteral(self, ctx: c_subsetParser.LiteralContext):
        pass

    # Enter a parse tree produced by c_subsetParser#char.
    def enterChar(self, ctx:c_subsetParser.CharContext):
        self.AST.addNode(CharNode(ctx.getText(), self.AST, (ctx.start.line, ctx.start.column)))
        #self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#char.
    def exitChar(self, ctx:c_subsetParser.CharContext):
        pass

    # Enter a parse tree produced by c_subsetParser#integer.
    def enterInteger(self, ctx: c_subsetParser.IntegerContext):
        self.AST.addNode(IntNode(ctx.getText(), self.AST, 0))
        # self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#integer.
    def exitInteger(self, ctx: c_subsetParser.IntegerContext):
        pass

    # Enter a parse tree produced by c_subsetParser#float_.
    def enterFloat_(self, ctx: c_subsetParser.Float_Context):
        self.AST.addNode(FloatNode(ctx.getText(), self.AST, (ctx.start.line, ctx.start.column)))
        #self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#float_.
    def exitFloat_(self, ctx: c_subsetParser.Float_Context):
        pass

    # Enter a parse tree produced by c_subsetParser#typeSpecBase.
    def enterTypeSpecBase(self, ctx:c_subsetParser.TypeSpecBaseContext):
        node = TypeSpecBaseNode(ctx.getText(), len(ctx.children), self.AST)
        node.type = toType(ctx.children[0].symbol.text) #first child is always a type
        self.AST.addNode(node)
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#typeSpecBase.
    def exitTypeSpecBase(self, ctx:c_subsetParser.TypeSpecBaseContext):
        pass

    # Enter a parse tree produced by c_subsetParser#typeSpecReference.
    def enterTypeSpecReference(self, ctx:c_subsetParser.TypeSpecReferenceContext):
        self.AST.addNode(TypeSpecReferenceNode(ctx.getText(), len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#typeSpecReference.
    def exitTypeSpecReference(self, ctx:c_subsetParser.TypeSpecReferenceContext):
        pass

    # Enter a parse tree produced by c_subsetParser#typeSpecPointer.
    def enterTypeSpecPointer(self, ctx: c_subsetParser.TypeSpecPointerContext):
        self.AST.addNode(TypeSpecPtrNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#typeSpecPointer.
    def exitTypeSpecPointer(self, ctx: c_subsetParser.TypeSpecPointerContext):
        pass

    # Enter a parse tree produced by c_subsetParser#typeSpec.
    def enterTypeSpec(self, ctx: c_subsetParser.TypeSpecContext):
        self.AST.addNode(TypeSpecNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#typeSpec.
    def exitTypeSpec(self, ctx: c_subsetParser.TypeSpecContext):
        pass

    # Enter a parse tree produced by c_subsetParser#typeSpecFunc.
    def enterTypeSpecFunc(self, ctx:c_subsetParser.TypeSpecFuncContext):
        self.AST.addNode(TypeSpecFuncNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#typeSpecFunc.
    def exitTypeSpecFunc(self, ctx:c_subsetParser.TypeSpecFuncContext):
        pass



    # Enter a parse tree produced by c_subsetParser#stdio.
    def enterStdio(self, ctx:c_subsetParser.StdioContext):
        self.AST.addNode(StdioNode(ctx.getText(), self.AST, (ctx.start.line, ctx.start.column)))
        pass

    # Exit a parse tree produced by c_subsetParser#stdio.
    def exitStdio(self, ctx:c_subsetParser.StdioContext):
        pass

    # Enter a parse tree produced by c_subsetParser#printf.
    def enterPrintf(self, ctx: c_subsetParser.PrintfContext):
        self.AST.addNode(VarDefNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))
        pass

    # Exit a parse tree produced by c_subsetParser#printf.
    def exitPrintf(self, ctx: c_subsetParser.PrintfContext):
        pass

    # Enter a parse tree produced by c_subsetParser#ioArglist.
    def enterIoArglist(self, ctx: c_subsetParser.IoArglistContext):
        self.AST.addNode(VarDefNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#ioArglist.
    def exitIoArglist(self, ctx: c_subsetParser.IoArglistContext):
        pass

    # Enter a parse tree produced by c_subsetParser#ioArg.
    def enterIoArg(self, ctx: c_subsetParser.IoArgContext):
        self.AST.addNode(VarDefNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#ioArg.
    def exitIoArg(self, ctx: c_subsetParser.IoArgContext):
        pass

    # # Enter a parse tree produced by c_subsetParser#format_.
    # def enterFormat_(self, ctx: c_subsetParser.Format_Context):
    #     self.AST.addNode(VarDefNode(len(ctx.children), self.AST))
    #     self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))
    #
    # # Exit a parse tree produced by c_subsetParser#format_.
    # def exitFormat_(self, ctx: c_subsetParser.Format_Context):
    #     pass

    # Enter a parse tree produced by c_subsetParser#string_input.
    def enterString_input(self, ctx: c_subsetParser.String_inputContext):
        self.AST.addNode(VarDefNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#string_input.
    def exitString_input(self, ctx: c_subsetParser.String_inputContext):
        pass

    # Enter a parse tree produced by c_subsetParser#width.
    def enterWidth(self, ctx: c_subsetParser.WidthContext):
        self.AST.addNode(VarDefNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Exit a parse tree produced by c_subsetParser#width.
    def exitWidth(self, ctx: c_subsetParser.WidthContext):
        pass

    # Enter a parse tree produced by c_subsetParser#name.
    def enterName(self, ctx: c_subsetParser.NameContext):
        self.AST.addNode(NameNode(ctx.getText(), self.AST, (ctx.start.line, ctx.start.column)))
        pass

    # Exit a parse tree produced by c_subsetParser#name.
    def exitName(self, ctx: c_subsetParser.NameContext):
        pass