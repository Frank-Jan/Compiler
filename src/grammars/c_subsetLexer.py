# Generated from grammars/c_subset.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\33")
        buf.write("\u00be\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\3\2\3\2\3\3\3\3\3\4\3\4\3\4\3\5\3")
        buf.write("\5\3\6\3\6\3\7\3\7\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t")
        buf.write("\3\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\13\3\f")
        buf.write("\3\f\3\f\3\f\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\16\3\17")
        buf.write("\3\17\3\17\3\17\3\17\3\17\3\20\3\20\3\20\3\20\3\20\3\20")
        buf.write("\3\20\3\21\5\21q\n\21\3\21\7\21t\n\21\f\21\16\21w\13\21")
        buf.write("\3\22\5\22z\n\22\3\22\7\22}\n\22\f\22\16\22\u0080\13\22")
        buf.write("\3\22\3\22\3\22\3\22\3\22\3\22\5\22\u0088\n\22\3\23\3")
        buf.write("\23\3\23\7\23\u008d\n\23\f\23\16\23\u0090\13\23\3\24\3")
        buf.write("\24\3\24\3\24\3\25\3\25\3\25\3\25\3\25\3\25\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\27\3\27\3\27\3\27\3\27\3\27\3\27")
        buf.write("\3\27\3\27\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32")
        buf.write("\2\2\33\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f")
        buf.write("\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27")
        buf.write("-\30/\31\61\32\63\33\3\2\5\5\2\13\f\17\17\"\"\4\2C\\c")
        buf.write("|\5\2\62;C\\c|\2\u00c1\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2")
        buf.write("\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2")
        buf.write("\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2")
        buf.write("\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!")
        buf.write("\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2")
        buf.write("\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3")
        buf.write("\2\2\2\3\65\3\2\2\2\5\67\3\2\2\2\79\3\2\2\2\t<\3\2\2\2")
        buf.write("\13>\3\2\2\2\r@\3\2\2\2\17B\3\2\2\2\21F\3\2\2\2\23K\3")
        buf.write("\2\2\2\25P\3\2\2\2\27V\3\2\2\2\31Z\3\2\2\2\33]\3\2\2\2")
        buf.write("\35b\3\2\2\2\37h\3\2\2\2!p\3\2\2\2#y\3\2\2\2%\u0089\3")
        buf.write("\2\2\2\'\u0091\3\2\2\2)\u0095\3\2\2\2+\u009b\3\2\2\2-")
        buf.write("\u00a1\3\2\2\2/\u00aa\3\2\2\2\61\u00b1\3\2\2\2\63\u00b6")
        buf.write("\3\2\2\2\65\66\7=\2\2\66\4\3\2\2\2\678\7?\2\28\6\3\2\2")
        buf.write("\29:\7*\2\2:;\7+\2\2;\b\3\2\2\2<=\7*\2\2=\n\3\2\2\2>?")
        buf.write("\7.\2\2?\f\3\2\2\2@A\7+\2\2A\16\3\2\2\2BC\t\2\2\2CD\3")
        buf.write("\2\2\2DE\b\b\2\2E\20\3\2\2\2FG\7x\2\2GH\7q\2\2HI\7k\2")
        buf.write("\2IJ\7f\2\2J\22\3\2\2\2KL\7e\2\2LM\7j\2\2MN\7c\2\2NO\7")
        buf.write("t\2\2O\24\3\2\2\2PQ\7h\2\2QR\7n\2\2RS\7q\2\2ST\7c\2\2")
        buf.write("TU\7v\2\2U\26\3\2\2\2VW\7k\2\2WX\7p\2\2XY\7v\2\2Y\30\3")
        buf.write("\2\2\2Z[\7k\2\2[\\\7h\2\2\\\32\3\2\2\2]^\7g\2\2^_\7n\2")
        buf.write("\2_`\7u\2\2`a\7g\2\2a\34\3\2\2\2bc\7y\2\2cd\7j\2\2de\7")
        buf.write("k\2\2ef\7n\2\2fg\7g\2\2g\36\3\2\2\2hi\7t\2\2ij\7g\2\2")
        buf.write("jk\7v\2\2kl\7w\2\2lm\7t\2\2mn\7p\2\2n \3\2\2\2oq\t\3\2")
        buf.write("\2po\3\2\2\2qu\3\2\2\2rt\t\4\2\2sr\3\2\2\2tw\3\2\2\2u")
        buf.write("s\3\2\2\2uv\3\2\2\2v\"\3\2\2\2wu\3\2\2\2xz\t\3\2\2yx\3")
        buf.write("\2\2\2z~\3\2\2\2{}\t\4\2\2|{\3\2\2\2}\u0080\3\2\2\2~|")
        buf.write("\3\2\2\2~\177\3\2\2\2\177\u0087\3\2\2\2\u0080~\3\2\2\2")
        buf.write("\u0081\u0082\7*\2\2\u0082\u0088\7+\2\2\u0083\u0084\7*")
        buf.write("\2\2\u0084\u0085\5%\23\2\u0085\u0086\7+\2\2\u0086\u0088")
        buf.write("\3\2\2\2\u0087\u0081\3\2\2\2\u0087\u0083\3\2\2\2\u0088")
        buf.write("$\3\2\2\2\u0089\u008e\5!\21\2\u008a\u008b\7.\2\2\u008b")
        buf.write("\u008d\5!\21\2\u008c\u008a\3\2\2\2\u008d\u0090\3\2\2\2")
        buf.write("\u008e\u008c\3\2\2\2\u008e\u008f\3\2\2\2\u008f&\3\2\2")
        buf.write("\2\u0090\u008e\3\2\2\2\u0091\u0092\7h\2\2\u0092\u0093")
        buf.write("\7q\2\2\u0093\u0094\7t\2\2\u0094(\3\2\2\2\u0095\u0096")
        buf.write("\7e\2\2\u0096\u0097\7q\2\2\u0097\u0098\7p\2\2\u0098\u0099")
        buf.write("\7u\2\2\u0099\u009a\7v\2\2\u009a*\3\2\2\2\u009b\u009c")
        buf.write("\7d\2\2\u009c\u009d\7t\2\2\u009d\u009e\7g\2\2\u009e\u009f")
        buf.write("\7c\2\2\u009f\u00a0\7m\2\2\u00a0,\3\2\2\2\u00a1\u00a2")
        buf.write("\7e\2\2\u00a2\u00a3\7q\2\2\u00a3\u00a4\7p\2\2\u00a4\u00a5")
        buf.write("\7v\2\2\u00a5\u00a6\7k\2\2\u00a6\u00a7\7p\2\2\u00a7\u00a8")
        buf.write("\7w\2\2\u00a8\u00a9\7g\2\2\u00a9.\3\2\2\2\u00aa\u00ab")
        buf.write("\7u\2\2\u00ab\u00ac\7y\2\2\u00ac\u00ad\7k\2\2\u00ad\u00ae")
        buf.write("\7v\2\2\u00ae\u00af\7e\2\2\u00af\u00b0\7j\2\2\u00b0\60")
        buf.write("\3\2\2\2\u00b1\u00b2\7e\2\2\u00b2\u00b3\7c\2\2\u00b3\u00b4")
        buf.write("\7u\2\2\u00b4\u00b5\7g\2\2\u00b5\62\3\2\2\2\u00b6\u00b7")
        buf.write("\7f\2\2\u00b7\u00b8\7g\2\2\u00b8\u00b9\7h\2\2\u00b9\u00ba")
        buf.write("\7c\2\2\u00ba\u00bb\7w\2\2\u00bb\u00bc\7n\2\2\u00bc\u00bd")
        buf.write("\7v\2\2\u00bd\64\3\2\2\2\13\2psuy|~\u0087\u008e\3\b\2")
        buf.write("\2")
        return buf.getvalue()


class c_subsetLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    WS = 7
    Void = 8
    Char = 9
    Float = 10
    Int = 11
    If = 12
    Else = 13
    While = 14
    Return = 15
    Vari = 16
    Funci = 17
    Args = 18
    For = 19
    Const = 20
    Break = 21
    Continue = 22
    Switch = 23
    Case = 24
    Default = 25

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "';'", "'='", "'()'", "'('", "','", "')'", "'void'", "'char'", 
            "'float'", "'int'", "'if'", "'else'", "'while'", "'return'", 
            "'for'", "'const'", "'break'", "'continue'", "'switch'", "'case'", 
            "'default'" ]

    symbolicNames = [ "<INVALID>",
            "WS", "Void", "Char", "Float", "Int", "If", "Else", "While", 
            "Return", "Vari", "Funci", "Args", "For", "Const", "Break", 
            "Continue", "Switch", "Case", "Default" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "WS", 
                  "Void", "Char", "Float", "Int", "If", "Else", "While", 
                  "Return", "Vari", "Funci", "Args", "For", "Const", "Break", 
                  "Continue", "Switch", "Case", "Default" ]

    grammarFileName = "c_subset.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


