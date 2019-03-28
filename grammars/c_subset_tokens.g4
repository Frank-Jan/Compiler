grammar c_subset_tokens;

// Mandatory
//types
Type
    : Void ;
    : Char ;
    : Float ;
    : Int ;

Void : 'void';
Char : 'char';
Float : 'float';
Int : 'int';

//loops
If : 'if';
Else : 'else';
While : 'while';
Return : 'return';

//variable
VAR : (a..z) | (A..Z)) ((a..z) | (A..Z) | (0..9))*

//Optional
For : 'for';
Const : 'const';
Break : 'break';
Continue : 'continue';
Switch : 'switch';
Case : 'case';
Default : 'default';




