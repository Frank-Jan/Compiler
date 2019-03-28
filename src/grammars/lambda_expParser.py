# Generated from grammars/lambda_exp.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\b")
        buf.write("\36\4\2\t\2\4\3\t\3\4\4\t\4\3\2\3\2\3\2\5\2\f\n\2\3\3")
        buf.write("\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\5")
        buf.write("\4\34\n\4\3\4\2\2\5\2\4\6\2\2\2\35\2\13\3\2\2\2\4\r\3")
        buf.write("\2\2\2\6\33\3\2\2\2\b\f\7\7\2\2\t\f\5\4\3\2\n\f\5\6\4")
        buf.write("\2\13\b\3\2\2\2\13\t\3\2\2\2\13\n\3\2\2\2\f\3\3\2\2\2")
        buf.write("\r\16\7\3\2\2\16\17\7\7\2\2\17\20\7\4\2\2\20\21\5\2\2")
        buf.write("\2\21\5\3\2\2\2\22\23\7\5\2\2\23\24\5\2\2\2\24\25\5\2")
        buf.write("\2\2\25\26\7\6\2\2\26\34\3\2\2\2\27\30\7\5\2\2\30\31\5")
        buf.write("\2\2\2\31\32\7\6\2\2\32\34\3\2\2\2\33\22\3\2\2\2\33\27")
        buf.write("\3\2\2\2\34\7\3\2\2\2\4\13\33")
        return buf.getvalue()


class lambda_expParser ( Parser ):

    grammarFileName = "lambda_exp.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'lambda'", "'.'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "VAR", "WS" ]

    RULE_expression = 0
    RULE_function = 1
    RULE_application = 2

    ruleNames =  [ "expression", "function", "application" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    VAR=5
    WS=6

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VAR(self):
            return self.getToken(lambda_expParser.VAR, 0)

        def function(self):
            return self.getTypedRuleContext(lambda_expParser.FunctionContext,0)


        def application(self):
            return self.getTypedRuleContext(lambda_expParser.ApplicationContext,0)


        def getRuleIndex(self):
            return lambda_expParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)




    def expression(self):

        localctx = lambda_expParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_expression)
        try:
            self.state = 9
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [lambda_expParser.VAR]:
                self.enterOuterAlt(localctx, 1)
                self.state = 6
                self.match(lambda_expParser.VAR)
                pass
            elif token in [lambda_expParser.T__0]:
                self.enterOuterAlt(localctx, 2)
                self.state = 7
                self.function()
                pass
            elif token in [lambda_expParser.T__2]:
                self.enterOuterAlt(localctx, 3)
                self.state = 8
                self.application()
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


    class FunctionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VAR(self):
            return self.getToken(lambda_expParser.VAR, 0)

        def expression(self):
            return self.getTypedRuleContext(lambda_expParser.ExpressionContext,0)


        def getRuleIndex(self):
            return lambda_expParser.RULE_function

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction" ):
                listener.enterFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction" ):
                listener.exitFunction(self)




    def function(self):

        localctx = lambda_expParser.FunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_function)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 11
            self.match(lambda_expParser.T__0)
            self.state = 12
            self.match(lambda_expParser.VAR)
            self.state = 13
            self.match(lambda_expParser.T__1)
            self.state = 14
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ApplicationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lambda_expParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(lambda_expParser.ExpressionContext,i)


        def getRuleIndex(self):
            return lambda_expParser.RULE_application

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterApplication" ):
                listener.enterApplication(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitApplication" ):
                listener.exitApplication(self)




    def application(self):

        localctx = lambda_expParser.ApplicationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_application)
        try:
            self.state = 25
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 16
                self.match(lambda_expParser.T__2)
                self.state = 17
                self.expression()
                self.state = 18
                self.expression()
                self.state = 19
                self.match(lambda_expParser.T__3)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 21
                self.match(lambda_expParser.T__2)
                self.state = 22
                self.expression()
                self.state = 23
                self.match(lambda_expParser.T__3)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





