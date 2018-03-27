#!/bin/bash
PROGRAM=FTP2server.py
PATH=/afs/cs.unc.edu/project/courses/comp431-s18/students/grantcm/grade/hw1/test_results/

echo $PATH
for files in $PATH*input
do
	cd ~/
	python3 /afs/cs.unc.edu/home/jisan/Comp431/Homework2/reference_implementation.py < $files > output.txt
	python3 $PROGRAM < $files > testoutput.txt
	echo $files
	echo `diff output.txt testoutput.txt`
done
