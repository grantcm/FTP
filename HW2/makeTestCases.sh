#!/bin/bash
# In order to add test cases, simply make a python file titled MakeInput(NUMBER).py 
# and a corresponding output file MakeOutput(NUMBER).py and then run this script

NUM=1
INPUT=MakeInput
INPUTFILE=input
OUTPUT=MakeOutput
OUTPUTFILE=output
FILEEND=.txt
PYTHONEND=.py

#if [[ $(ls -dq *Input* | wc -l) = $(ls -dq *Output* | wc -l) ]]; then

	for i in `seq 1 $(ls -dq *Input* | wc -l)`; do
		NUM=$i
		if [ -f $INPUT$NUM$PYTHONEND ]; then
			python3 $INPUT$NUM$PYTHONEND > $INPUTFILE$NUM$FILEEND
		fi
		if [ -f $OUTPUT$NUM$PYTHONEND ]; then	
			python3 $OUTPUT$NUM$PYTHONEND > $OUTPUTFILE$NUM$FILEEND
		else	
			python3 /afs/cs.unc.edu/home/jisan/Comp431/Homework2/reference_implementation.py < $INPUTFILE$NUM$FILEEND > $OUTPUTFILE$NUM$FILEEND
		fi
	done
#else
#	echo "Uneven number of Input and Output files"
#fi
