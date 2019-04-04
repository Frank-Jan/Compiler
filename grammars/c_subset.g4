grammar c_subset;

import c_subset_tokens;

cppSyntax
    : (generalStatement | generalStatement ';')*
    ;

functionSyntax
    : (functionStatement ';' | codeBlock | loop)*
    ;

generalStatement
    : generalDeclaration
    | generalDefinition
    ;

functionStatement
    : variableDeclaration
    | variableDefinition
    | assignment
    | returnStatement
    | variable
    | function
    | literal
    ;

returnStatement
    : RETURN    ( conditionalExpression
                | arithmicOperation
                | function
                | variable
                | literal
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
    : typeSpec variable '=' (arithmicOperation | identifier)
    ;

functionDefinition
    : typeSpec functionSignature codeBlock
    ;

generalDefinition
    : variableDefinition
    | functionDefinition
    ;

assignment
    : variable '=' arithmicOperation
    | variable '=' identifier
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
    : variable
    | function
    | literal
    ;

function
    : NAME '(' ')'
    | NAME ('(' (identifier)(',' identifier)* ')')
    ;

functionSignature
    : NAME '(' ')'
    | NAME ('(' (typeSpec | typeSpec variable)(','(typeSpec variable | typeSpec))* ')')
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
