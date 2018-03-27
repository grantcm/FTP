import sys

sys.stdout.write("220 COMP 431 FTP server ready.\r\n")
print("FTP reply 220 accepted.  Text is : COMP 431 FTP server ready.")
sys.stdout.write("331 Guest access OK, send password.\r\n")
print("FTP reply 331 accepted.  Text is : Guest access OK, send password.")
sys.stdout.write("230Guest login OK.\r\n")
print("ERROR -- reply-code")
sys.stdout.write("Port command successful (152.2.131.205,8080).\r\n")
print("ERROR -- reply-code")
sys.stdout.write("650 File status okay.\r\n")
print("ERROR -- reply-code")
sys.stdout.write("220 COMP 431 FTP server ready.\n")
print("ERROR -- <CRLF>")
sys.stdout.write("220 COMP 431 \u00ff FTP server ready.\r\n")
print("ERROR -- reply-text")

