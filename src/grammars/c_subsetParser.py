# Generated from grammars/c_subset.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\33")
        buf.write("F\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\3\2\3\2\3\2\5\2\24\n\2\3\2\3\2\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\3\5\3\36\n\3\3\4\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5")
        buf.write("\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7\62\n\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\5\79\n\7\7\7;\n\7\f\7\16\7>\13\7\3\7\3")
        buf.write("\7\5\7B\n\7\3\b\3\b\3\b\2\2\t\2\4\6\b\n\f\16\2\4\3\2\22")
        buf.write("\23\3\2\n\r\2E\2\23\3\2\2\2\4\35\3\2\2\2\6\37\3\2\2\2")
        buf.write("\b$\3\2\2\2\n(\3\2\2\2\f*\3\2\2\2\16C\3\2\2\2\20\24\5")
        buf.write("\4\3\2\21\24\5\6\4\2\22\24\5\b\5\2\23\20\3\2\2\2\23\21")
        buf.write("\3\2\2\2\23\22\3\2\2\2\24\25\3\2\2\2\25\26\7\3\2\2\26")
        buf.write("\3\3\2\2\2\27\30\5\16\b\2\30\31\7\22\2\2\31\36\3\2\2\2")
        buf.write("\32\33\5\16\b\2\33\34\5\f\7\2\34\36\3\2\2\2\35\27\3\2")
        buf.write("\2\2\35\32\3\2\2\2\36\5\3\2\2\2\37 \5\16\b\2 !\7\22\2")
        buf.write("\2!\"\7\4\2\2\"#\5\n\6\2#\7\3\2\2\2$%\7\22\2\2%&\7\4\2")
        buf.write("\2&\'\5\n\6\2\'\t\3\2\2\2()\t\2\2\2)\13\3\2\2\2*A\7\22")
        buf.write("\2\2+B\7\5\2\2,\61\7\6\2\2-\62\5\16\b\2./\5\16\b\2/\60")
        buf.write("\7\22\2\2\60\62\3\2\2\2\61-\3\2\2\2\61.\3\2\2\2\62<\3")
        buf.write("\2\2\2\638\7\7\2\2\64\65\5\16\b\2\65\66\7\22\2\2\669\3")
        buf.write("\2\2\2\679\5\16\b\28\64\3\2\2\28\67\3\2\2\29;\3\2\2\2")
        buf.write(":\63\3\2\2\2;>\3\2\2\2<:\3\2\2\2<=\3\2\2\2=?\3\2\2\2>")
        buf.write("<\3\2\2\2?@\7\b\2\2@B\3\2\2\2A+\3\2\2\2A,\3\2\2\2B\r\3")
        buf.write("\2\2\2CD\t\3\2\2D\17\3\2\2\2\b\23\35\618<A")
        return buf.getvalue()


class c_subsetParser ( Parser ):

    grammarFileName = "c_subset.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "'='", "'()'", "'('", "','", "')'", 
                     "<INVALID>", "'void'", "'char'", "'float'", "'int'", 
                     "'if'", "'else'", "'while'", "'return'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'for'", "'const'", "'break'", 
                     "'continue'", "'switch'", "'case'", "'default'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "WS", "Void", 
                      "Char", "Float", "Int", "If", "Else", "While", "Return", 
                      "Vari", "Funci", "Args", "For", "Const", "Break", 
                      "Continue", "Switch", "Case", "Default" ]

    RULE_expression = 0
    RULE_declaration = 1
    RULE_definition = 2
    RULE_assignment = 3
    RULE_ident = 4
    RULE_funcDeclaration = 5
    RULE_typeSpec = 6

    ruleNames =  [ "expression", "declaration", "definition", "assignment", 
                   "ident", "funcDeclaration", "typeSpec" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    WS=7
    Void=8
    Char=9
    Float=10
    Int=11
    If=12
    Else=13
    While=14
    Return=15
    Vari=16
    Funci=17
    Args=18
    For=19
    Const=20
    Break=21
    Continue=22
    Switch=23
    Case=24
    Default=25

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def declaration(self):
            return self.getTypedRuleContext(c_subsetParser.DeclarationContext,0)


        def definition(self):
            return self.getTypedRuleContext(c_subsetParser.DefinitionContext,0)


        def assignment(self):
            return self.getTypedRuleContext(c_subsetParser.AssignmentContext,0)


        def getRuleIndex(self):
            return c_subsetParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)




    def expression(self):

        localctx = c_subsetParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.state = 14
                self.declaration()
                pass

            elif la_ == 2:
                self.state = 15
                self.definition()
                pass

            elif la_ == 3:
                self.state = 16
                self.assignment()
                pass


            self.state = 19
            self.match(c_subsetParser.T__0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeSpec(self):
            return self.getTypedRuleContext(c_subsetParser.TypeSpecContext,0)


        def Vari(self):
            return self.getToken(c_subsetParser.Vari, 0)

        def funcDeclaration(self):
            return self.getTypedRuleContext(c_subsetParser.FuncDeclarationContext,0)


        def getRuleIndex(self):
            return c_subsetParser.RULE_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaration" ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaration" ):
                listener.exitDeclaration(self)




    def declaration(self):

        localctx = c_subsetParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_declaration)
        try:
            self.state = 27
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 21
                self.typeSpec()
                self.state = 22
                self.match(c_subsetParser.Vari)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 24
                self.typeSpec()
                self.state = 25
                self.funcDeclaration()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefinitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeSpec(self):
            return self.getTypedRuleContext(c_subsetParser.TypeSpecContext,0)


        def Vari(self):
            return self.getToken(c_subsetParser.Vari, 0)

        def ident(self):
            return self.getTypedRuleContext(c_subsetParser.IdentContext,0)


        def getRuleIndex(self):
            return c_subsetParser.RULE_definition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefinition" ):
                listener.enterDefinition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefinition" ):
                listener.exitDefinition(self)




    def definition(self):

        localctx = c_subsetParser.DefinitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_definition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            self.typeSpec()
            self.state = 30
            self.match(c_subsetParser.Vari)
            self.state = 31
            self.match(c_subsetParser.T__1)
            self.state = 32
            self.ident()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Vari(self):
            return self.getToken(c_subsetParser.Vari, 0)

        def ident(self):
            return self.getTypedRuleContext(c_subsetParser.IdentContext,0)


        def getRuleIndex(self):
            return c_subsetParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)




    def assignment(self):

        localctx = c_subsetParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 34
            self.match(c_subsetParser.Vari)
            self.state = 35
            self.match(c_subsetParser.T__1)
            self.state = 36
            self.ident()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Vari(self):
            return self.getToken(c_subsetParser.Vari, 0)

        def Funci(self):
            return self.getToken(c_subsetParser.Funci, 0)

        def getRuleIndex(self):
            return c_subsetParser.RULE_ident

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdent" ):
                listener.enterIdent(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdent" ):
                listener.exitIdent(self)




    def ident(self):

        localctx = c_subsetParser.IdentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_ident)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            _la = self._input.LA(1)
            if not(_la==c_subsetParser.Vari or _la==c_subsetParser.Funci):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncDeclarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Vari(self, i:int=None):
            if i is None:
                return self.getTokens(c_subsetParser.Vari)
            else:
                return self.getToken(c_subsetParser.Vari, i)

        def typeSpec(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(c_subsetParser.TypeSpecContext)
            else:
                return self.getTypedRuleContext(c_subsetParser.TypeSpecContext,i)


        def getRuleIndex(self):
            return c_subsetParser.RULE_funcDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFuncDeclaration" ):
                listener.enterFuncDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFuncDeclaration" ):
                listener.exitFuncDeclaration(self)




    def funcDeclaration(self):

        localctx = c_subsetParser.FuncDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_funcDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self.match(c_subsetParser.Vari)
            self.state = 63
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [c_subsetParser.T__2]:
                self.state = 41
                self.match(c_subsetParser.T__2)
                pass
            elif token in [c_subsetParser.T__3]:
                self.state = 42
                self.match(c_subsetParser.T__3)
                self.state = 47
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                if la_ == 1:
                    self.state = 43
                    self.typeSpec()
                    pass

                elif la_ == 2:
                    self.state = 44
                    self.typeSpec()
                    self.state = 45
                    self.match(c_subsetParser.Vari)
                    pass


                self.state = 58
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==c_subsetParser.T__4:
                    self.state = 49
                    self.match(c_subsetParser.T__4)
                    self.state = 54
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                    if la_ == 1:
                        self.state = 50
                        self.typeSpec()
                        self.state = 51
                        self.match(c_subsetParser.Vari)
                        pass

                    elif la_ == 2:
                        self.state = 53
                        self.typeSpec()
                        pass


                    self.state = 60
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 61
                self.match(c_subsetParser.T__5)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeSpecContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Void(self):
            return self.getToken(c_subsetParser.Void, 0)

        def Char(self):
            return self.getToken(c_subsetParser.Char, 0)

        def Float(self):
            return self.getToken(c_subsetParser.Float, 0)

        def Int(self):
            return self.getToken(c_subsetParser.Int, 0)

        def getRuleIndex(self):
            return c_subsetParser.RULE_typeSpec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeSpec" ):
                listener.enterTypeSpec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeSpec" ):
                listener.exitTypeSpec(self)




    def typeSpec(self):

        localctx = c_subsetParser.TypeSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_typeSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << c_subsetParser.Void) | (1 << c_subsetParser.Char) | (1 << c_subsetParser.Float) | (1 << c_subsetParser.Int))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





