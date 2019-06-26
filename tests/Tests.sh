#!/usr/bin/env bash

# This shell script is used to generate the grammar with Antlr
# and run all c-files to generate llvm-files and mips-files (asm)

echo creating grammar
java -jar ./lib/antlr-4.7.2-complete.jar -visitor -o src -Dlanguage=Python3 grammars/c_subset.g4

echo test 1: types
python3 ./compiler.py ./tests/files/1_types.c
lli ./tests/files/1_types.ll

echo test 2: import
python3 ./compiler.py ./tests/files/2_import.c
lli ./tests/files/2_import.ll

echo test 3: reservedWords
python3 ./compiler.py ./tests/files/3_reservedWords.c
lli ./tests/files/3_reservedWords.ll

echo test 4: localGlobal
python3 ./compiler.py ./tests/files/4_localGlobal.c
lli ./tests/files/4_localGlobal.ll

echo test 5: comments
python3 ./compiler.py ./tests/files/5_comments.c
lli ./tests/files/5_comments.ll

echo test 6: operations
python3 ./compiler.py ./tests/files/6_operations.c
lli ./tests/files/6_operations.ll

echo test 7: functions
python3 ./compiler.py ./tests/files/7_functions.c
lli ./tests/files/7_functions.ll

echo test8: arrays
python3 ./compiler.py ./tests/files/8_arrays.c
lli ./tests/files/8_arrays.ll
