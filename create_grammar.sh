#! /bin/sh
# This shell script is used to generate the grammar with Antlr

java -jar lib/antlr-4.7.2-complete.jar -o src -Dlanguage=Python3 grammars/c_subset.g4
