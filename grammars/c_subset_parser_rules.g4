grammar c_subset_parser_rules;

expression
    : 'int' VARIABLE '=' VARIABLE ';'
    ;


//application
//    : '(' VARIABLE ')' | '(' VARIABLE ')'
//    ;

VARIABLE
    : [a-z] [a-zA-Z0-9]*
    ;

WS
   : [ \t\r\n] -> skip
   ;
