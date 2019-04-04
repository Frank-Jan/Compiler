grammar c_subset_tokens;
//
//tokens {VOID, CHAR, FLOAT, INT}

VOID : 'void';
CHAR : 'char';
FLOAT : 'float';
INT : 'int';



// Mandatory
//Type specifiers
typeSpecBase //typeSpecifier, type is reserved keyword!!!
    : VOID
    | CHAR
    | FLOAT
    | INT
    ;

typeSpecPointer
    : typeSpecBase '*'
    ;

typeSpec
    : typeSpecBase
    | typeSpecPointer
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

Integer
    : [0-9]+
    | '-'[0-9]+
    ;

Float
    : ([0-9]+) '.' ([0-9]*)
    | '-.' ([0-9]+)
    | '.' ([0-9]+)  //Doesn't accept .5?
    | '-' ([0-9]+) '.' ([0-9]*)
    ;
    
Char
    : ('\'' ( [a-z] | [A-Z] | [0-9] | ' ') '\'')
    ; 

//Viable name compositions
NAME : ([a-z] | [A-Z] | '_')([a-z] | [A-Z] | '_' | [0-9])*;
