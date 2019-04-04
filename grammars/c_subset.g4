grammar c_subset;

import c_subset_tokens;

cppSyntax
    : (generalStatement)*
    ;

functionSyntax
    : (functionStatement | codeBlock | loop)*
    ;

generalStatement
    : generalDeclaration ';'
    | generalDefinition
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
    ;

variableDeclaration
    : typeSpec variable
    ;

functionDeclaration
    : typeSpec functionSignature
    ;

generalDeclaration
    : variableDeclaration
    | functionDeclaration
    ;

variableDefinition
    : typeSpec variable '=' (identifier | arithmicOperation) ';'
    ;

functionDefinition
    : typeSpec functionSignature codeBlock
    ;

generalDefinition
    : functionDefinition
    ;

assignment
    : variable '=' identifier
    | variable '=' arithmicOperation
    ;

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
    : '*' (variable | function | reference)
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
    : Integer
    | Float
    | Char
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
