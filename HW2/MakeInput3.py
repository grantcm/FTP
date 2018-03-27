# Description: Valid sequence with some invalid commands in it
#  1. Out of Sequence commands after user
#  2. Duplicate retr
#  3. Commands after quit
#
# WARNING: You must create your own file in the same directory called still_relative

import sys


sys.stdout.write("User kevin!!??\r\n")
sys.stdout.write("sYSt\r\n")
sys.stdout.write("pass password12345\r\n")
sys.stdout.write("tyPe A\r\n")
sys.stdout.write("sYSt\r\n")
sys.stdout.write("PorT 152,25,124,131,31,144\r\n")
sys.stdout.write("rEtr still_relative\r\n")
sys.stdout.write("rEtr still_relative\r\n")
sys.stdout.write("QUIT\r\n")

# TODO:Put commands after in input
sys.stdout.write("User kevin!!??\r\n")
sys.stdout.write("pass password12345\r\n")
