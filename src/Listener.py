from src.grammars.c_subsetListener import *
import src.AST.init as ast
from antlr4 import *


# This class defines a complete listener for a parse tree produced by c_subsetParser.
class Listener(c_subsetListener):

    def __init__(self):
        self.AST = ast.AST()

    # GET AST FUNCTION
    def getAST(self):
        return self.AST

    # ADDS TERMINALS TO AST
    def addTerminals(self, children, pos):
        if children is None:
            return

        for i in range(len(children)):
            if isinstance(children[i], TerminalNode):
                node = ast.TerNode(children[i].symbol.text, self.AST, pos)
                if not (ast.toType(node.value) is None):
                    node.isType = True
                self.AST.addNode(node, i)

    # Enter a parse tree produced by c_subsetParser#cppSyntax.
    def enterCSyntax(self, ctx: c_subsetParser.CSyntaxContext):
        children = 0
        if not (ctx.children is None):
            children = len(ctx.children)
        node = ast.RootNode("Root", children, self.AST)
        self.AST.nodes.append(node)
        self.AST.root = node
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#functionSyntax.
    def enterFunctionSyntax(self, ctx: c_subsetParser.FunctionSyntaxContext):
        numberChildren = 0
        if not (ctx.children is None):
            numberChildren = len(ctx.children)
        self.AST.addNode(ast.FuncSyntaxNode(numberChildren, self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#generalStatement.
    def enterGeneralStatement(self, ctx: c_subsetParser.GeneralStatementContext):
        self.AST.addNode(ast.GenStatNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#functionStatement.
    def enterFunctionStatement(self, ctx: c_subsetParser.FunctionStatementContext):
        self.AST.addNode(ast.FuncStatNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#returnStatement.
    def enterReturnStatement(self, ctx: c_subsetParser.ReturnStatementContext):
        self.AST.addNode(ast.ReturnStatNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#variableDefinition.
    def enterVariableDefinition(self, ctx: c_subsetParser.VariableDefinitionContext):
        self.AST.addNode(ast.VarDefNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#functionDefinition.
    def enterFunctionDefinition(self, ctx: c_subsetParser.FunctionDefinitionContext):
        self.AST.addNode(ast.FuncDefNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#functionSignatureDefinition.
    def enterFunctionSignatureDefinition(self, ctx: c_subsetParser.FunctionSignatureDefinitionContext):
        self.AST.addNode(ast.FuncSignDefNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#generalVarDefinition.
    def enterGeneralVarDefinition(self, ctx:c_subsetParser.GeneralVarDefinitionContext):
        self.AST.addNode(ast.GenDefNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#generalDefinition.
    def enterGeneralDefinition(self, ctx: c_subsetParser.GeneralDefinitionContext):
        self.AST.addNode(ast.GenDefNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#variableDeclaration.
    def enterVariableDeclaration(self, ctx: c_subsetParser.VariableDeclarationContext):
        self.AST.addNode(ast.VarDeclNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx: c_subsetParser.FunctionDeclarationContext):
        self.AST.addNode(ast.FuncDeclNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#generalDeclaration.
    def enterGeneralDeclaration(self, ctx: c_subsetParser.GeneralDeclarationContext):
        self.AST.addNode(ast.GenDeclNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#assignRight.
    def enterAssignRight(self, ctx: c_subsetParser.AssignRightContext):
        self.AST.addNode(ast.AssignRightNode(self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#assignment.
    def enterAssignment(self, ctx: c_subsetParser.AssignmentContext):
        self.AST.addNode(ast.AssignNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#arithmeticOperation.
    def enterArithmeticOperation(self, ctx: c_subsetParser.ArithmeticOperationContext):
        self.AST.addNode(ast.ArOpNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#add.
    def enterAdd(self, ctx: c_subsetParser.AddContext):
        self.AST.addNode(ast.AddNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#prod.
    def enterProd(self, ctx: c_subsetParser.ProdContext):
        self.AST.addNode(ast.ProdNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#atom.
    def enterAtom(self, ctx: c_subsetParser.AtomContext):
        self.AST.addNode(ast.AtomNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#conditionalExpression.
    def enterConditionalExpression(self, ctx: c_subsetParser.ConditionalExpressionContext):
        self.AST.addNode(ast.CondExpNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#loop.
    def enterLoop(self, ctx: c_subsetParser.LoopContext):
        self.AST.addNode(ast.LoopNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#whileLoop.
    def enterWhileLoop(self, ctx: c_subsetParser.WhileLoopContext):
        self.AST.addNode(ast.WhileNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#ifelseLoop.
    def enterIfelseLoop(self, ctx: c_subsetParser.IfelseLoopContext):
        self.AST.addNode(ast.IfElseNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#codeBlock.
    def enterCodeBlock(self, ctx: c_subsetParser.CodeBlockContext):
        self.AST.addNode(ast.CodeBlockNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#value.
    def enterValue(self, ctx: c_subsetParser.ValueContext):
        self.AST.addNode(ast.ValueNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#lvalue.
    def enterLvalue(self, ctx: c_subsetParser.LvalueContext):
        self.AST.addNode(ast.LvalueNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#arrayElement.
    def enterArrayElement(self, ctx: c_subsetParser.ArrayElementContext):
        self.AST.addNode(ast.ArrayElementNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#rvalue.
    def enterRvalue(self, ctx: c_subsetParser.RvalueContext):
        self.AST.addNode(ast.RvalueNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#function.
    def enterFunction(self, ctx: c_subsetParser.FunctionContext):
        self.AST.addNode(ast.FuncNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#functionSignature.
    def enterFunctionSignature(self, ctx: c_subsetParser.FunctionSignatureContext):
        self.AST.addNode(ast.FuncSignNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#variable.
    def enterVariable(self, ctx: c_subsetParser.VariableContext):
        self.AST.addNode(ast.VarNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#literal.
    def enterLiteral(self, ctx: c_subsetParser.LiteralContext):
        self.AST.addNode(ast.LitNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#array.
    def enterArray(self, ctx: c_subsetParser.ArrayContext):
        self.AST.addNode(ast.ArrayNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#char.
    def enterChar(self, ctx: c_subsetParser.CharContext):
        self.AST.addNode(ast.CharNode(ctx.getText(), self.AST, (ctx.start.line, ctx.start.column)))
        # self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#integer.
    def enterInteger(self, ctx: c_subsetParser.IntegerContext):
        self.AST.addNode(ast.IntNode(ctx.getText(), self.AST, 0))
        # self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#float_.
    def enterFloat_(self, ctx: c_subsetParser.Float_Context):
        self.AST.addNode(ast.FloatNode(ctx.getText(), self.AST, (ctx.start.line, ctx.start.column)))
        # self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#typeSpecBase.
    def enterTypeSpecBase(self, ctx: c_subsetParser.TypeSpecBaseContext):
        node = ast.TypeSpecBaseNode(ctx.getText(), len(ctx.children), self.AST)
        node.type = ast.toType(ctx.children[0].symbol.text)  # first child is always a type
        self.AST.addNode(node)
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#typeSpecReference.
    def enterTypeSpecReference(self, ctx: c_subsetParser.TypeSpecReferenceContext):
        self.AST.addNode(ast.TypeSpecReferenceNode(ctx.getText(), len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#typeSpecPointer.
    def enterTypeSpecPointer(self, ctx: c_subsetParser.TypeSpecPointerContext):
        self.AST.addNode(ast.TypeSpecPtrNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#typeSpec.
    def enterTypeSpec(self, ctx: c_subsetParser.TypeSpecContext):
        self.AST.addNode(ast.TypeSpecNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#typeSpecFunc.
    def enterTypeSpecFunc(self, ctx: c_subsetParser.TypeSpecFuncContext):
        self.AST.addNode(ast.TypeSpecFuncNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#stdio.
    def enterStdio(self, ctx: c_subsetParser.StdioContext):
        self.AST.addNode(ast.StdioNode(ctx.getText(), self.AST, (ctx.start.line, ctx.start.column)))

    # Enter a parse tree produced by c_subsetParser#printf.
    def enterPrintf(self, ctx: c_subsetParser.PrintfContext):
        self.AST.addNode(ast.PrintfNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#scanf.
    def enterScanf(self, ctx: c_subsetParser.ScanfContext):
        self.AST.addNode(ast.ScanfNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#printFormat.
    def enterPrintFormat(self, ctx: c_subsetParser.PrintFormatContext):
        self.AST.addNode(ast.PrintFormatNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#formatChar.
    def enterFormatCharScan(self, ctx: c_subsetParser.FormatCharScanContext):
        self.AST.addNode(ast.FormatCharScanNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#formatChar.
    def enterFormatCharPrint(self, ctx: c_subsetParser.FormatCharPrintContext):
        self.AST.addNode(ast.FormatCharPrintNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#string.
    def enterString(self, ctx: c_subsetParser.StringContext):
        self.AST.addNode(ast.StringNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#ioArglist.
    def enterIoArglist(self, ctx: c_subsetParser.IoArglistContext):
        self.AST.addNode(ast.IoArgListNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#name.
    def enterName(self, ctx: c_subsetParser.NameContext):
        self.AST.addNode(ast.NameNode(ctx.getText(), self.AST, (ctx.start.line, ctx.start.column)))

    # # Enter a parse tree produced by c_subsetParser#generalVarDefinition.
    # def enterGeneralVarDefinition(self, ctx:c_subsetParser.GeneralVarDefinitionContext):
    #     self.AST.addNode(VarDefNode(len(ctx.children), self.AST))
    #     self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#arrayDeclaration.
    def enterArrayDeclaration(self, ctx: c_subsetParser.ArrayDeclarationContext):
        self.AST.addNode(ast.ArrayDeclNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#shortArrayDeclaration.
    def enterShortArrayDeclaration(self, ctx: c_subsetParser.ShortArrayDeclarationContext):
        self.AST.addNode(ast.ShortArrayDeclNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#longArrayDeclaration.
    def enterLongArrayDeclaration(self, ctx: c_subsetParser.LongArrayDeclarationContext):
        self.AST.addNode(ast.LongArrayDeclNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by c_subsetParser#arrayInitialiser.
    def enterArrayInitialiser(self, ctx: c_subsetParser.ArrayInitialiserContext):
        self.AST.addNode(ast.ArrayInitNode(len(ctx.children), self.AST))
        self.addTerminals(ctx.children, (ctx.start.line, ctx.start.column))
