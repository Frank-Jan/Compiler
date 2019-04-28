grammar c_subset;

import c_subset_tokens;

//woops: should be cSynthax
cSyntax
    : (generalStatement)* EOF;

functionSyntax
    : (functionStatement | functionDefinition ';'? | codeBlock | loop)*
    ;

generalStatement
    : generalDefinition ';'?
    | generalDeclaration ';'
    | generalVarDefinition ';'
    | stdio
    ;

functionStatement
    : (variableDeclaration
        | variableDefinition
        | functionDeclaration
        | assignment
        | returnStatement
        | variable
        | function
        | literal )
        ';'
    ;

returnStatement
//    : RETURN    ( function
//                | literal
//                | variable
//                | arithmeticOperation
//                )
    : RETURN value
    | RETURN
    ;


variableDefinition
    : variableDeclaration assignRight
    ;

functionDefinition
    : (typeSpec | VOID) functionSignatureDefinition codeBlock
    ;

functionSignatureDefinition
    : variable '(' ')'
    | variable '(' (typeSpecFunc variable)(','(typeSpecFunc variable) )* ')'
    ;

generalDefinition
    : functionDefinition
    ;

generalVarDefinition
    : variableDeclaration '=' literal
    ;

variableDeclaration
    : typeSpec variable //normal variables and pointers
    | typeSpec variable '['integer']'    //arrays
    ;


functionDeclaration
    : (typeSpec | VOID) functionSignature
    ;

generalDeclaration
    : variableDeclaration
    | functionDeclaration
    ;

assignRight
    : '=' value
    ;

assignment
    : lvalue assignRight
    ;

//arithmetic expressions
arithmeticOperation
    : add
    ;

add
    : (atom | prod) ('+' add)
    | (atom | prod) ('-' add)
    | prod
    ;

prod
    : atom ('*' prod)
    | atom ('/' prod)
    | atom
    ;

atom
    : function
    | literal
    | lvalue
    | '(' value ')'
    ;

//conditional expressions
conditionalExpression
    :   value '>' value
    |   value '<' value
    |   value '==' value
    ;

//loops
loop
    : whileLoop
    | ifelseLoop
    ;

whileLoop
    : WHILE '(' conditionalExpression ')'   (functionStatement | codeBlock)
    ;

ifelseLoop
    : IF '('conditionalExpression')' (functionStatement | codeBlock)
      (ELSE (functionStatement | codeBlock))?
    ;


//code block
codeBlock
    :   '{' functionSyntax '}'
    ;

value
    : lvalue
    | rvalue
    ;

lvalue
    : variable
    | arrayElement
    | '*' lvalue
    | '*' '&' lvalue
    ;

arrayElement
    : variable '['value']'
    ;

rvalue
    : function
    | literal
    | '&' lvalue
    | arithmeticOperation
    | array
    ;

array
    : '{' value (',' value)* '}'
    | '{' '}'
    ;

function
    : printf
    | scanf
    | variable '(' ')'
    | variable ('(' (value)(',' value)* ')')
    ;

functionSignature
    : variable '(' ')'
    | variable ('(' (typeSpecFunc variable?)
                (','(typeSpecFunc variable?) )*
            ')')
    ;

variable
    : name
    ;

literal
    : char
    | integer
    | float_
    ;

char
    : ('\'' ( DIGIT | LETTER ) '\'')
    ;

integer
    : DIGIT+
    | '-'DIGIT+
    ;
    
float_  //'_'added because conflict with target language (python3) 
    : (DIGIT+) '.' (DIGIT*)
    | '-.' (DIGIT)
    | '.' (DIGIT+)
    | '-' (DIGIT+) '.' (DIGIT*)
    ;    

//Type specifiers
typeSpecBase //typeSpecifier, type is reserved keyword!!!
    : CHAR
    | FLOAT
    | INT
    ;

typeSpecReference
    : typeSpecBase '&'
    | typeSpecPointer '&'
    ;

typeSpecPointer
    : typeSpecBase '*'
    | typeSpecPointer '*'
    | VOID '*'
    ;

typeSpec
    : typeSpecBase
    | typeSpecPointer
    ;

typeSpecFunc
    : typeSpecBase
    | typeSpecPointer
    | typeSpecReference
    ;

stdio
    : INCLUDESTDIO
    ;

printf
    : 'printf' '(' printFormat ioArglist? ')'
    ;

scanf
    : 'scanf' '(' value ioArglist? ')'
    ;

printFormat
    : '"' (string | formatCharPrint)* '"'
    ;
//
//scanFormat
//    : '"' (string |

formatCharScan
    : FORMAT_CHAR_SCAN
    ;

formatCharPrint
    : FORMAT_CHAR_PRINT
    ;

string
    : (~(FORMAT_CHAR_PRINT))+
    ;

ioArglist
    : ',' value ioArglist?
    ;

//format_out
//    :  string_output
//    ;
//
//format_in
//    : '%' LETTER
//    | FORMAT_CHAR
//    ;
//
//format_out
//    : '%' width LETTER
//    ;
//
//string_input
//    : '"' (LETTER | format_in)* '"'
//    ;
//
//string_output
//    : '"' (LETTER | format_out)* '"'
//    ;
//
//width
//    : DIGIT+
//    ;

//Viable name compositions
name : (LETTER | '_')(LETTER | DIGIT | '_')*;

//Things to skip:
WhiteSpace
   : [ \t\r\n] -> skip
   ;

MultiLineComment
    : '/*' .*? '*/' -> skip
    ;

SingleLineComment
    : '/''/' .*? '\n' -> skip
    ;
