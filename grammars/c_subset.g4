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
    : RETURN    ( function
                | literal
                | variable
                | arithmeticOperation
                )
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

variableDeclaration
    : typeSpec variable //normal variables and pointers
    | typeSpec variable '['Digit+']'    //arrays
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
    : WHILE '(' conditionalExpression ')'   (functionStatement ';' | codeBlock)
    ;

ifelseLoop
    : IF '('conditionalExpression')' (functionStatement ';' | codeBlock)
      (ELSE (functionStatement ';' | codeBlock))?
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
    | '*' lvalue
    | '*' '&' lvalue
    ;

rvalue
    : function
    | literal
    | '&' lvalue
    | arithmeticOperation
    ;

function
    : variable '(' ')'
    | variable ('(' (value)(',' value)* ')')
    ;

functionSignature
    : variable '(' ')'
    | variable ('(' (typeSpecFunc variable?)
                (','(typeSpecFunc variable?) )*
            ')')
    ;

variable
    : NAME
    ;

literal
    : char
    | integer
    | float_
    ;
char
    : Char
    ;

integer
    : Digit+
    | '-'Digit+
    ;
    
float_  //'_'added because conflict with target language (python3) 
    : (Digit+) '.' (Digit*)
    | '-.' (Digit)
    | '.' (Digit+)
    | '-' (Digit+) '.' (Digit*)
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

//Things to skip:
WS
   : [ \t\r\n] -> skip
   ;

MultiLineComment
    : '/*' .*? '*/' -> skip
    ;

SingleLineComment
    : '/''/' .*? '\n' -> skip
    ;
