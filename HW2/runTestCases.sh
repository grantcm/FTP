#!/bin/bash
PROGRAM=FTP2server.py
INPUT=input
TESTOUTPUT=testoutput
OUTPUT=output
FILEEND=.txt
NUM=0

if [ $# -eq 0 ]; then
	for i in `seq 1 $(ls -dq *input* | wc -l)`; do
		NUM=$i
		if [ -f $INPUT$NUM$FILEEND ]; then
			python3 $PROGRAM < $INPUT$NUM$FILEEND > $TESTOUTPUT$NUM$FILEEND
		else
			echo "Either no input script or not output script for $NUM"
		fi
		if [ -f $OUTPUT$NUM$FILEEND ]; then
			echo "diff for $TESTOUTPUT$NUM$FILEEND and $OUTPUT$NUM$FILEEND is:"
			diff $TESTOUTPUT$NUM$FILEEND $OUTPUT$NUM$FILEEND
		fi
	done
else
	python3 $PROGRAM < $INPUT$1$FILEEND > $TESTOUTPUT$1$FILEEND
	echo "diff for $TESTOUTPUT$1$FILEEND and $OUTPUT$1$FILEEND is:"
	diff $TESTOUTPUT$1$FILEEND $OUTPUT$1$FILEEND
fi
