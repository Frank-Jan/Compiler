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

DIGIT : [0-9];
LETTER : ( [a-z] | [A-Z] );

FORMAT_CHAR : '%s' | '%i' | '%d' | '%c';

//includes
INCLUDESTDIO : '#include <stdio.h>';
