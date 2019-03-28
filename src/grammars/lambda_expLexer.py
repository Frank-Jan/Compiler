# Generated from grammars/lambda_exp.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\b")
        buf.write("(\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3")
        buf.write("\6\6\6\36\n\6\r\6\16\6\37\3\7\6\7#\n\7\r\7\16\7$\3\7\3")
        buf.write("\7\2\2\b\3\3\5\4\7\5\t\6\13\7\r\b\3\2\4\3\2c|\5\2\13\f")
        buf.write("\17\17\"\"\2)\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t")
        buf.write("\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\3\17\3\2\2\2\5\26\3")
        buf.write("\2\2\2\7\30\3\2\2\2\t\32\3\2\2\2\13\35\3\2\2\2\r\"\3\2")
        buf.write("\2\2\17\20\7n\2\2\20\21\7c\2\2\21\22\7o\2\2\22\23\7d\2")
        buf.write("\2\23\24\7f\2\2\24\25\7c\2\2\25\4\3\2\2\2\26\27\7\60\2")
        buf.write("\2\27\6\3\2\2\2\30\31\7*\2\2\31\b\3\2\2\2\32\33\7+\2\2")
        buf.write("\33\n\3\2\2\2\34\36\t\2\2\2\35\34\3\2\2\2\36\37\3\2\2")
        buf.write("\2\37\35\3\2\2\2\37 \3\2\2\2 \f\3\2\2\2!#\t\3\2\2\"!\3")
        buf.write("\2\2\2#$\3\2\2\2$\"\3\2\2\2$%\3\2\2\2%&\3\2\2\2&\'\b\7")
        buf.write("\2\2\'\16\3\2\2\2\5\2\37$\3\b\2\2")
        return buf.getvalue()


class lambda_expLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    VAR = 5
    WS = 6

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'lambda'", "'.'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>",
            "VAR", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "VAR", "WS" ]

    grammarFileName = "lambda_exp.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


