grammar c_subset_tokens;
//
//tokens {VOID, CHAR, FLOAT, INT}

VOID : 'void';
CHAR : 'char';
FLOAT : 'float';
INT : 'int';



// Mandatory

//Loops
IF : 'if';
ELSE : 'else';
WHILE : 'while';
RETURN : 'return';

//Optional
FOR : 'for';
CONST : 'const';
BREAK : 'break';
CONTINUE : 'continue';
SWITCH : 'switch';
CASE : 'case';
DEFAULT : 'default';

Digit : [0-9] ;
    
Char : ('\'' ( [a-z] | [A-Z] | [0-9] | ' ') '\'');

//Viable name compositions
NAME : ([a-z] | [A-Z] | '_')([a-z] | [A-Z] | '_' | [0-9])*;

//includes
INCLUDESTDIO : '#include <stdio.h>';
