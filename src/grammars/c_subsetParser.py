# Generated from grammars/c_subset.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\25")
        buf.write("\13\4\2\t\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\2\2\3\2\2\2\2")
        buf.write("\t\2\4\3\2\2\2\4\5\7\t\2\2\5\6\7\25\2\2\6\7\7\3\2\2\7")
        buf.write("\b\7\25\2\2\b\t\7\4\2\2\t\3\3\2\2\2\2")
        return buf.getvalue()


class c_subsetParser ( Parser ):

    grammarFileName = "c_subset.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'='", "';'", "<INVALID>", "'void'", "'char'", 
                     "'float'", "'int'", "'if'", "'else'", "'while'", "'return'", 
                     "'for'", "'const'", "'break'", "'continue'", "'switch'", 
                     "'case'", "'default'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "WS", "Void", 
                      "Char", "Float", "Int", "If", "Else", "While", "Return", 
                      "For", "Const", "Break", "Continue", "Switch", "Case", 
                      "Default", "VARIABLE" ]

    RULE_expression = 0

    ruleNames =  [ "expression" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    WS=3
    Void=4
    Char=5
    Float=6
    Int=7
    If=8
    Else=9
    While=10
    Return=11
    For=12
    Const=13
    Break=14
    Continue=15
    Switch=16
    Case=17
    Default=18
    VARIABLE=19

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Int(self):
            return self.getToken(c_subsetParser.Int, 0)

        def VARIABLE(self, i:int=None):
            if i is None:
                return self.getTokens(c_subsetParser.VARIABLE)
            else:
                return self.getToken(c_subsetParser.VARIABLE, i)

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
            self.state = 2
            self.match(c_subsetParser.Int)
            self.state = 3
            self.match(c_subsetParser.VARIABLE)
            self.state = 4
            self.match(c_subsetParser.T__0)
            self.state = 5
            self.match(c_subsetParser.VARIABLE)
            self.state = 6
            self.match(c_subsetParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





