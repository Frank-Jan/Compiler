# Generated from grammars/c_subset.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\25")
        buf.write("\u008e\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\3\2\3\2\3\3\3\3\3\4\3\4\3\4\3\4\3\5\3")
        buf.write("\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3\7")
        buf.write("\3\7\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3")
        buf.write("\13\3\13\3\13\3\13\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3")
        buf.write("\f\3\r\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\16\3\16\3\17")
        buf.write("\3\17\3\17\3\17\3\17\3\17\3\20\3\20\3\20\3\20\3\20\3\20")
        buf.write("\3\20\3\20\3\20\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\22")
        buf.write("\3\22\3\22\3\22\3\22\3\23\3\23\3\23\3\23\3\23\3\23\3\23")
        buf.write("\3\23\3\24\3\24\7\24\u008a\n\24\f\24\16\24\u008d\13\24")
        buf.write("\2\2\25\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f")
        buf.write("\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25\3\2\5\5")
        buf.write("\2\13\f\17\17\"\"\3\2c|\5\2\62;C\\c|\2\u008e\2\3\3\2\2")
        buf.write("\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2")
        buf.write("\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25")
        buf.write("\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3")
        buf.write("\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2")
        buf.write("\'\3\2\2\2\3)\3\2\2\2\5+\3\2\2\2\7-\3\2\2\2\t\61\3\2\2")
        buf.write("\2\13\66\3\2\2\2\r;\3\2\2\2\17A\3\2\2\2\21E\3\2\2\2\23")
        buf.write("H\3\2\2\2\25M\3\2\2\2\27S\3\2\2\2\31Z\3\2\2\2\33^\3\2")
        buf.write("\2\2\35d\3\2\2\2\37j\3\2\2\2!s\3\2\2\2#z\3\2\2\2%\177")
        buf.write("\3\2\2\2\'\u0087\3\2\2\2)*\7?\2\2*\4\3\2\2\2+,\7=\2\2")
        buf.write(",\6\3\2\2\2-.\t\2\2\2./\3\2\2\2/\60\b\4\2\2\60\b\3\2\2")
        buf.write("\2\61\62\7x\2\2\62\63\7q\2\2\63\64\7k\2\2\64\65\7f\2\2")
        buf.write("\65\n\3\2\2\2\66\67\7e\2\2\678\7j\2\289\7c\2\29:\7t\2")
        buf.write("\2:\f\3\2\2\2;<\7h\2\2<=\7n\2\2=>\7q\2\2>?\7c\2\2?@\7")
        buf.write("v\2\2@\16\3\2\2\2AB\7k\2\2BC\7p\2\2CD\7v\2\2D\20\3\2\2")
        buf.write("\2EF\7k\2\2FG\7h\2\2G\22\3\2\2\2HI\7g\2\2IJ\7n\2\2JK\7")
        buf.write("u\2\2KL\7g\2\2L\24\3\2\2\2MN\7y\2\2NO\7j\2\2OP\7k\2\2")
        buf.write("PQ\7n\2\2QR\7g\2\2R\26\3\2\2\2ST\7t\2\2TU\7g\2\2UV\7v")
        buf.write("\2\2VW\7w\2\2WX\7t\2\2XY\7p\2\2Y\30\3\2\2\2Z[\7h\2\2[")
        buf.write("\\\7q\2\2\\]\7t\2\2]\32\3\2\2\2^_\7e\2\2_`\7q\2\2`a\7")
        buf.write("p\2\2ab\7u\2\2bc\7v\2\2c\34\3\2\2\2de\7d\2\2ef\7t\2\2")
        buf.write("fg\7g\2\2gh\7c\2\2hi\7m\2\2i\36\3\2\2\2jk\7e\2\2kl\7q")
        buf.write("\2\2lm\7p\2\2mn\7v\2\2no\7k\2\2op\7p\2\2pq\7w\2\2qr\7")
        buf.write("g\2\2r \3\2\2\2st\7u\2\2tu\7y\2\2uv\7k\2\2vw\7v\2\2wx")
        buf.write("\7e\2\2xy\7j\2\2y\"\3\2\2\2z{\7e\2\2{|\7c\2\2|}\7u\2\2")
        buf.write("}~\7g\2\2~$\3\2\2\2\177\u0080\7f\2\2\u0080\u0081\7g\2")
        buf.write("\2\u0081\u0082\7h\2\2\u0082\u0083\7c\2\2\u0083\u0084\7")
        buf.write("w\2\2\u0084\u0085\7n\2\2\u0085\u0086\7v\2\2\u0086&\3\2")
        buf.write("\2\2\u0087\u008b\t\3\2\2\u0088\u008a\t\4\2\2\u0089\u0088")
        buf.write("\3\2\2\2\u008a\u008d\3\2\2\2\u008b\u0089\3\2\2\2\u008b")
        buf.write("\u008c\3\2\2\2\u008c(\3\2\2\2\u008d\u008b\3\2\2\2\4\2")
        buf.write("\u008b\3\b\2\2")
        return buf.getvalue()


class c_subsetLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    WS = 3
    Void = 4
    Char = 5
    Float = 6
    Int = 7
    If = 8
    Else = 9
    While = 10
    Return = 11
    For = 12
    Const = 13
    Break = 14
    Continue = 15
    Switch = 16
    Case = 17
    Default = 18
    VARIABLE = 19

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'='", "';'", "'void'", "'char'", "'float'", "'int'", "'if'", 
            "'else'", "'while'", "'return'", "'for'", "'const'", "'break'", 
            "'continue'", "'switch'", "'case'", "'default'" ]

    symbolicNames = [ "<INVALID>",
            "WS", "Void", "Char", "Float", "Int", "If", "Else", "While", 
            "Return", "For", "Const", "Break", "Continue", "Switch", "Case", 
            "Default", "VARIABLE" ]

    ruleNames = [ "T__0", "T__1", "WS", "Void", "Char", "Float", "Int", 
                  "If", "Else", "While", "Return", "For", "Const", "Break", 
                  "Continue", "Switch", "Case", "Default", "VARIABLE" ]

    grammarFileName = "c_subset.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


