grammar c_subset;
import c_subset_tokens, c_subset_parser_rules;

file
    : (expression ';')*
    ;

expression
    : (declaration | definition| assignment)
    ;

declaration
    : typeSpec Vari
    | typeSpec funcDeclaration
    ;

definition
    : typeSpec Vari '=' ident
    ;

assignment
    : Vari '=' ident
    ;

//Identifier
ident : // id is a reserved keyword!!!
    Vari | Funci;


funcDeclaration
    : funcSubDecl
    | Vari '(' (typeSpec | typeSpec Vari)(','(typeSpec Vari | typeSpec))* ')'
    ;

WS
   : [ \t\r\n] -> skip
   ;