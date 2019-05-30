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
ASCII: . | ' ' | '\n' | '\t' | ~'"';

FORMAT_CHAR_SCAN : '%s' | '%i' | '%d' | '%c' ;

FORMAT_CHAR_PRINT : '%' DIGIT* ('i'|'f'|'s'|'c') ;


//includes
INCLUDESTDIO : '#include <stdio.h>';
