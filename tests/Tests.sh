#!/usr/bin/env bash

# This shell script is used to generate the grammar with Antlr
# and run all c-files to generate llvm-files and mips-files (asm)
java -jar ./lib/antlr-4.7.2-complete.jar -visitor -o src -Dlanguage=Python3 grammars/c_subset.g4
python3 ./compiler.py ./tests/files/types.c
lli ./tests/files/types.ll
#python3 ./main.py arrays.c