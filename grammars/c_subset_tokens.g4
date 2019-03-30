grammar c_subset_tokens;
tokens {Void, Char, Float, Int}
Void : 'void';
Char : 'char';
Float : 'float';
Int : 'int';

// Mandatory
//types
typeSpec //typeSpecifier, type is reserved keyword!!!
    : Void
    | Char
    | Float
    | Int
    ;



//loops
If : 'if';
Else : 'else';
While : 'while';
Return : 'return';

Vari : ([a-z] | [A-Z]) ([a-z] | [A-Z] | [0-9])*;
FuncSubDecl : ([a-z] | [A-Z]) ([a-z] | [A-Z] | [0-9])* '(' ')';
Funci : ([a-z] | [A-Z]) ([a-z] | [A-Z] | [0-9])* ('()' | '(' Args  ')');
Args: Vari ( ',' Vari)*;

//Optional
For : 'for';
Const : 'const';
Break : 'break';
Continue : 'continue';
Switch : 'switch';
Case : 'case';
Default : 'default';




