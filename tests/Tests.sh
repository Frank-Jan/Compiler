#!/usr/bin/env bash

# This shell script is used to generate the grammar with Antlr
# and run all c-files to generate llvm-files and mips-files (asm)
java -jar ./lib/antlr-4.7.2-complete.jar -visitor -o src -Dlanguage=Python3 grammars/c_subset.g4

python3 ./compiler.py ./tests/files/1_types.c
lli ./tests/files/1_types.ll

python3 ./compiler.py ./tests/files/2_import.c
lli ./tests/files/2_import.ll

python3 ./compiler.py ./tests/files/3_reservedWords.c
lli ./tests/files/3_reservedWords.ll

python3 ./compiler.py ./tests/files/4_localGlobal.c
lli ./tests/files/4_localGlobal.ll

python3 ./compiler.py ./tests/files/5_comments.c
lli ./tests/files/5_comments.ll

python3 ./compiler.py ./tests/files/6_operations.c
lli ./tests/files/6_operations.ll

python3 ./compiler.py ./tests/files/7_functions.c
lli ./tests/files/7_functions.ll

python3 ./compiler.py ./tests/files/8_arrays.c
lli ./tests/files/8_arrays.ll
