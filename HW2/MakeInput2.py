# Description: Valid sequence with some invalid commands in it
#  1. Out of Sequence commands
#  2. Bad Port Number
#  3. File Does Not Exist
#  4. Bad Command
#
# WARNING: You must create your own file in the same directory called relative
#

import sys

sys.stdout.write("PorT 152,25,124,131,31,144\r\n")
sys.stdout.write("User Jasleen\r\n")
sys.stdout.write("User user\r\n")
sys.stdout.write("pass password12345\r\n")
sys.stdout.write("tyPe A\r\n")
sys.stdout.write("sYSt\r\n")
sys.stdout.write("PorT 152,25,124,131,31\r\n")
sys.stdout.write("PorT 152,25,124,131,31,144\r\n")
sys.stdout.write("rEtr still/relative/does_not_exist\r\n")
sys.stdout.write("rEtr relative\r\n")
sys.stdout.write("dejar\r\n")
sys.stdout.write("QUIT\r\n")
