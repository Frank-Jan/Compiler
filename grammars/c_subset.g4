grammar c_subset;

import c_subset_tokens;

//woops: should be cSynthax
cppSyntax
    : (generalStatement)* EOF;

functionSyntax
    : (functionStatement | codeBlock | loop)*
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
        | functionDefinition
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


variableDefinition
    : typeSpec variable '=' (identifier | arithmicOperation)
    ;

functionDefinition
    : (typeSpec | VOID) NAME '(' ')' codeBlock
    | (typeSpec | VOID) NAME ('(' (typeSpec '&'? variable)
                (','(typeSpec '&'? variable) )*
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

assignment
    : variable '=' (literal | identifier | arithmicOperation) ;

//arithmic expressions
arithmicOperation
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
    | NAME ('(' (typeSpec '&'? variable?)
                (','(typeSpec '&'? variable?) )*
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

typeSpecPointer
    : typeSpecBase '*'
    | typeSpecPointer '*'
    | VOID '*'
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
