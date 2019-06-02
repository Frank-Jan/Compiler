# Compiler
A simple-C compiler. 

## Use
* run create_grammars.sh to build the grammar
* run python3 c2llvm.py [filename] to convert the file to llvm
* there will be a file [filename].ll in the same directory as [filename].c
* there will be a file [filename].asm in the same directory as [filename].c

## Tests
* The test-script located in tests/Tests.sh will run all [filename].c files located in tests/files
* The generated .ll and .asm files will be written to the same location
* Each [filename].c resembles a feature asked from the assignment to prove it's functionality 

## Mandatory Features Implemented:
* datatype char,float,int and pointer can be used
* ifelse loops and while-loops  
* local and global variables
* comments

## Mandatory Features Not Implemented:
* None

## Optional Features Implemented:
* All paths of function body end with return statement if function doesn't return void
* Dead code 
