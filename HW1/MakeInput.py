import sys

sys.stdout.write("USER jasleen\r\n")
sys.stdout.write("uSeR jasleen\r\n")
sys.stdout.write("usr jasleen\r\n")
sys.stdout.write("USERjasleen\r\n")
sys.stdout.write("user\r\n")
sys.stdout.write("USER jasl*n\r\n")
sys.stdout.write("USER jaslee\u00a5\r\n")
sys.stdout.write("USER           jasleen\r\n")
sys.stdout.write("USER ja sl een \r\n")
sys.stdout.write("PASS 12@456\r\n")
sys.stdout.write("PASS 12*456\r\n")
sys.stdout.write("TYPE A\r\n")
sys.stdout.write("TYPE I\r\n")
sys.stdout.write("TYPE B\r\n")
sys.stdout.write("SYST\r\n")
sys.stdout.write("SYST jasleen\r\n")
sys.stdout.write("NOOP\r\n")
sys.stdout.write("NOP\r\n")
sys.stdout.write("QUIT\r\n")
sys.stdout.write("quit\r\n")
sys.stdout.write("quit \r\n")
sys.stdout.write("quit\n")
sys.stdout.write("user grant\r\n")
sys.stdout.write("pass gr\u0504\r\n")
sys.stdout.write("qui\n")
sys.stdout.write("quit\n")
sys.stdout.write("user  \r\n")
sys.stdout.write("pass  \r\n")
sys.stdout.write("quit\r")
sys.stdout.write("quit\r\n")