grammar c_subset;

import c_subset_tokens;

cppSyntax
    : (statement ';')*
    ;

statement
    : declaration
    | definition
    | assignment
    ;

declaration
    : typeSpec variable
    | typeSpec functionSignature
    ;

definition
    : typeSpec variable '=' (arithmicExpression | identifier)
    ;

assignment
    : variable '=' arithmicExpression
    | variable '=' identifier
    ;

//arithmic expressions
arithmicExpression
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
    | '(' arithmicExpression ')'
    ;

//Identifier
identifier // id is a reserved keyword!!!
    : variable
    | function
    ;

function
    : NAME '(' ')'
    | NAME ('(' (variable)(',' variable)* ')')
    ;

functionSignature
    : NAME '(' ')'
    | NAME ('(' (typeSpec | typeSpec variable)(','(typeSpec variable | typeSpec))* ')')
    ;

variable
    : NAME
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