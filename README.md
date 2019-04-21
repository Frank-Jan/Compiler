# Compiler
A simple-C compiler. 

## Use
* run create_grammars.sh to build the grammar
* run python3 c2llvm.py [filename] to convert the file to llvm
* there will be a file [filename].ll in the same directory as [filename].c

## Mandatory Features Implemented:
* datatype char,float,int and pointer can be used
* ifelse loops and while-loops  
* local and global variables
* comments

## Mandatory Features Not Implemented:
* the use of printf and scanf
* arrays
* in the errors the position and line are not given

## Optional Features Implemented:
* All paths if function body end with return statement if function doesn't return void 
