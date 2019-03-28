grammar lambda_exp;
expression : VAR | function | application;
function : 'lambda' VAR '.' expression ;
application :  '(' expression expression ')' | '(' expression ')';
VAR : [a-z]+ ;
WS : [ \r\t\n]+ -> skip ;
