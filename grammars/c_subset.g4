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
    ;

returnStatement
    : RETURN    ( conditionalExpression
                | arithmicExpression
                | function
                | variable
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
    : typeSpec variable '=' (arithmicExpression | identifier)
    ;

functionDefinition
    : typeSpec functionSignature '{' functionSyntax '}'
    ;

generalDefinition
    : variableDefinition
    | functionDefinition
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