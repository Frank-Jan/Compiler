grammar c_subset_parser_rules;

expression
    : declaratie ';' 
    | definitie ';' 
    | identifier '=' expression ';'
    | operation

function
    : 'lambda' VARIABLE '.' expression
    ;

application
    : '(' expression expression ')' | '(' expression ')'
    ;

VARIABLE
    : [a-z] [a-zA-Z0-9]*
    ;

WS
   : [ \t\r\n] -> skip
   ;
