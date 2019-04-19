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
    | INCLUDESTDIO
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
    : RETURN    ( conditionalExpression
                | function
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
    : (typeSpec | VOID) variable '(' ')' codeBlock
    | (typeSpec | VOID) variable ('(' (typeSpecFunc variable)
                (','(typeSpecFunc variable) )*
            ')') codeBlock
    ;

generalDefinition
    : functionDefinition
    | variableDefinition ';'
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
    | prod
    ;

add
    : (atom | prod) ('+' add)
    | (atom | prod) ('-' add)
    | atom
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
     (ELSE IF '('conditionalExpression')' (functionStatement ';' | codeBlock))*
      (ELSE (functionStatement ';' | codeBlock))?
    ;


//code block
codeBlock
    :   '{' functionSyntax '}'
    ;


//Identifier
//identifier // id is a reserved keyword!!!
//    : dereference
//    | reference
//    | variable
//    | function
//    | literal
//    ;
//
//dereference_right
//    : dereference_left
//    | '*' function
//    | '*' dereference_right
//    ;

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
