grammar c_subset;

import c_subset_tokens;

cppSyntax
    : (generalStatement)* EOF;

functionSyntax
    : (functionStatement | codeBlock | loop)*
    ;

generalStatement
    : generalDeclaration ';'
    | generalDefinition
    | include
    ;

functionStatement
    : (variableDeclaration
        | variableDefinition
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
                | arithmicOperation
                )
    | RETURN
    ;

include
    : INCLUDE (('<' LIBNAME '>') | ('"' LIBNAME '"') )
    ;


variableDeclaration
    : typeSpec variable //normal variables and pointers
    | typeSpec variable '['Digit+']'    //arrays
    ;

functionDeclaration
    : typeSpec functionSignature
    ;

generalDeclaration
    : variableDeclaration
    | functionDeclaration
    ;

variableDefinition
    : typeSpec variable '=' (identifier | arithmicOperation)
    ;

functionDefinition
    : typeSpec functionSignature codeBlock
    ;

generalDefinition
    : functionDefinition
    ;

assignment
    : variable '=' (literal | identifier | arithmicOperation) ;

//arithmic expressions
arithmicOperation
    : prod '+' add
    | prod
    ;

add
    : prod ('+' add)
    | prod ('-' add)
    | prod
    ;

prod
    : atom ('*' prod)
    | atom ('/' prod)
    | atom
    ;

atom
    : identifier
    | '(' arithmicOperation ')'
    ;

//conditional expressions
conditionalExpression
    :   identifier '>' identifier
    |   identifier '<' identifier
    |   identifier '==' identifier
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
      ELSE (functionStatement ';' | codeBlock)
    ;


//code block
codeBlock
    :   '{' functionSyntax '}'
    ;


//Identifier
identifier // id is a reserved keyword!!!
    : dereference
    | reference
    | variable
    | function
    | literal
    ;

dereference
    : '*' (variable | function | reference | dereference)
    ;

reference
    : '&' (variable | dereference)
    ;

function
    : NAME '(' ')'
    | NAME ('(' (identifier)(',' identifier)* ')')
    ;

functionSignature
    : NAME '(' ')'
    | NAME ('(' (typeSpec | typeSpec variable | typeSpec '&' | typeSpec '&' variable)
                (','(typeSpec | typeSpec variable | typeSpec '&' | typeSpec '&' variable) )*
            ')')
    ;

variable
    : NAME
    ;

literal
    : Char
    | integer
    | float_
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

typeSpecPointer
    : typeSpecBase '*'
    | typeSpecPointer '*'
    ;

typeSpec
    : typeSpecBase
    | typeSpecPointer
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
