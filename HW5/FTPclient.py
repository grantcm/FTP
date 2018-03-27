import sys
import socket
import os
import re
import errno

commands = ['quit','get','connect']
eol=os.linesep
connected=0
failconnect = 'CONNECT failed\n'
validconnect = ['USER anonymous\r\n','PASS guest@\r\n','SYST\r\n','TYPE I\r\n']
port=0
client_socket = 0
tcp_socket = 0
retr_path = 'retr_files'
file_copy_name = 'FILE'
file_copy_count = 1

successmessage='FTP reply %s accepted. Text is: %s\n'
errormessage = 'ERROR -- %s\n'


#Checks if the parameter is an element using regex
def isElement(element):
	regex = re.compile('[a-zA-Z][a-zA-Z0-9]+')
	match = regex.match(element)
	if not match or match.end() != len(element):
		return 0
	return 1

#Checks if the parameter is a valid domain by parsing into elements
def isDomain(domain):
	for arg in domain.split('.'):
		if not isElement(arg):
			return 0
	return 1

#Checks if the parameter is a valid port number
def isPort(port):
	if not port.isnumeric() or port[0] == '0':
		return 0

	if 0 <= int(port) <= 65535:
		return 1
	return 0

#Checks if the pathname is an encodable ascii string, return false if it is not
def isPathname(string):
	try:
		string.encode('ascii')
		return True
	except UnicodeEncodeError:
		return False

#Verifies the parameter is a string using the definition from the assignment
def isString(a):
        if not a:
                return 0
        stringiterator = iter(a)
        index = 0 
        for character in stringiterator:
                #This parses escape characters from the string
                if '\\' in character:
                        if a[index:index+2] == '\\u':
                                return 0
                        next(stringiterator, None)
                elif not isValidChar(character):
                        return 0
                index+=1
        return 1

#Check for valid characters by converting to ascii code and then assuring it isn't one of the banned characters
def isValidChar(a):
        intform = ord(a)
        return intform!= 10 and intform!=13 and 0 <= intform < 128 

#Func to parse server responses
def parseServerResponse(line):
	if not line.endswith('\r\n'):
		sys.stdout.write(errormessage % "<CRLF>")
	command = line.strip('\r\n').split(None, 1)
	if len(command) != 2:
		sys.stdout.write(errormessage % 'reply-code')
	elif int(command[0]) in range(100,599):
		if isString(command[1]) and int(command[0]) in range(100,400):
			sys.stdout.write(successmessage % (command[0], command[1]))
			return 1
		elif isString(command[1]) and int(command[0]) in range(400,599):
			sys.stdout.write(successmessage % (command[0], command[1]))
			return 0
		else:
			sys.stdout.write(errormessage % 'reply-text')
	else:
		sys.stdout.write(errormessage % 'reply-code')

#Helper function to print errors
def printError(error):			
	print("ERROR -- %s" % error)

def isConnected():
	if connected == 0:
		printError("expecting CONNECT")
		return 0
	return 1

#Parser the command from the input line
def commandParser(line):
	global client_socket
	command = line[0].lower()
	if not command in commands:
		printError("request")
		return 0
	if (command == 'connect'):
		args = line[1].split()
		if len(args) == 0:
			printError("request")
		if not isDomain(args[0]):
			printError("server-host")
			return 0
		if len(args) == 1 or not isPort(args[1]):
			printError("server-port")
			return 0
	elif(command == 'get'):
		if not isConnected():
			return 0
		if not isPathname(line[1]):
			printError("pathname")
			return 0
	elif(command == 'quit'):
		if not isConnected():
			return 0
		sys.stdout.write("QUIT accepted, terminating FTP client%s" % eol)
		sys.stdout.write("QUIT\r\n")
		client_socket.send("QUIT\r\n".encode())
		response = client_socket.recv(2048).decode()
		parseServerResponse(response)
		client_socket.close()
		quit()	
	return 1

#Executes the command, performing appropriate output to stdout when necessary
def executeCommand(commandobj):
	global port, client_socket, tcp_socket, file_copy_count, file_copy_name, retr_path, connected
	command = commandobj[0].lower()
	if command == 'connect':
		args = commandobj[1].split()
		#Connect, if can't print failconnect
		#If existing connect, close current and reconnect
		#client_socket.close()

		sys.stdout.write(("CONNECT accepted for FTP server at host %s and port %s%s")  % (args[0], args[1], eol))
		if client_socket:
			client_socket.close()
		client_socket = socket.socket(socket.AF_INET)
		try:
			client_socket.connect((args[0], int(args[1])))
			connected = 1
		except OSError:
			sys.stdout.write(failconnect)
			connected = 0
			return 
		response = client_socket.recv(2048).decode()
		parseServerResponse(response)
		#sys.stdout.write("CONNECT accepted for FTP server at host %s and port %s%s"
		#%  (args[0],args[1],eol))
		for line in validconnect:
			sys.stdout.write(line)
			client_socket.send(line.encode())
			response = client_socket.recv(2048).decode()
			parseServerResponse(response)
			#Write to the server and write response to stdout
	elif command == 'get':
		sys.stdout.write("GET accepted for %s%s" % (commandobj[1], eol))
		my_ip = socket.gethostbyname(socket.gethostname()).replace('.',',')
		portstr = str(int(port/256))+","+str(port%256)
		#Send sequence of commands to server
		#Process both responses before continuing
		#Before sending port, create a socket specifying port number used in command
		#If cannot create, write "GET failed, FTP-data port not allocated."
		#TODO add error catch
		try:
			client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			client_tcp.bind((socket.gethostname(), port))
			client_tcp.listen(1)
		except OSError:
			sys.stdout.write("GET failed, FTP-data port not allocated.")
			return
	
		sys.stdout.write("PORT %s,%s\r\n" % (my_ip, portstr))
		client_socket.send(("PORT %s,%s\r\n" % (my_ip, portstr)).encode())
		response = client_socket.recv(2048).decode()
		parseServerResponse(response)
		port+=1
		sys.stdout.write("RETR %s\r\n" % commandobj[1])
		client_socket.send(("RETR %s\r\n" % commandobj[1]).encode())
		response = client_socket.recv(2048).decode()
		if parseServerResponse(response):
			while True:
				server_tcp, addr = client_tcp.accept()
				data = server_tcp.recv(2048)
				fileName = retr_path+'/'+file_copy_name + str(file_copy_count)
				with open(fileName,'w') as f:
					f.write(data.decode())
				f.close()
				file_copy_count+=1
		
			server_tcp.close()

		client_tcp.close()
		

	return

#Reads in each line and calls helper functions
def main():
	global port, client_socket
	port = int(sys.argv[1])
	if not os.path.isdir(retr_path):
		os.mkdir(retr_path)
	
	for line in sys.stdin:	
		sys.stdout.write(line)
		command = line.rstrip(eol)
		commandobj = command.split(None,1)
		if commandParser(commandobj):
			executeCommand(commandobj)

if __name__ == "__main__":
	main()
