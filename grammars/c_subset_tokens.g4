grammar c_subset_tokens;
//
//tokens {VOID, CHAR, FLOAT, INT}

VOID : 'void';
CHAR : 'char';
FLOAT : 'float';
INT : 'int';

pointer
    : VOID '*'
    | FLOAT '*'
    | CHAR'*'
    | INT '*'
    ;

// Mandatory
//Type specifiers
typeSpec //typeSpecifier, type is reserved keyword!!!
    : VOID
    | CHAR
    | FLOAT
    | INT
    | pointer
    ;

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

//Viable name compositions
NAME : ([a-z] | [A-Z] | '_')([a-z] | [A-Z] | '_' | [0-9])*;