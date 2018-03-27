#The approach to this problem was to make several methods that verified the types of data input. 
#They are isString, isValidChar, isValidCommand, and isValidArgument.
#Each method verifies that the passed parameter matches the expected types outlined in the assignment.
#The other methods are used to parse the input line into its respective parts: the command and the argument.
#This token is then used to verify whether or not it is a correct command.

import sys
import shutil
import os.path
import socket

commands = {'user':'string','pass':'string','type':'AI','syst':'none','noop':'none','quit':'none','port':'host-port','retr':'string'}
errorcodes = {'command':'500 Syntax error, command unrecognized.\r\n',
		'parameter':'501 Syntax error in parameter.\r\n',
		'sequence':'503 Bad sequence of commands.\r\n',
		'notloggedin':'530 Not logged in.\r\n',
		'retr': '550 File not found or access denied.\r\n'}
successcodes = {'retr':'150 File status okay.\r\n',
		'command':'200 Command OK.\r\n',
		'type': '200 Type set to %s.\r\n',
		'port':'200 Port command successful (%s).\r\n',
		'syst':'215 UNIX Type: L8.\r\n',
		'pass':'230 Guest login OK.\r\n',
		'retrdone':'250 Requested file action completed.\r\n', 
		'user':'331 Guest access OK, send password.\r\n',
		'quit':'221 Goodbye.\r\n',
		'data':'425 Can not open data connection.\r\n'}
ready = '220 COMP 431 FTP server ready.\r\n'
retrpath = 'retr_files'
commandpos = 0
argumentpos = 1
originalpos = 2
outputflags = [0,0,0]
command_history = []
file_copy_name = 'file'
file_copy_count = 1
port = 0
userflag = 0
passflag = 1
portflag = 2

buffersize = 2048

client_port = 0
client_hostname=0

#Tokenizes the input by parsing into a command and argument
def tokenize(a):
	command = []
	argument = []
	commandParsed = 0
	passWhitespace = 0
	argumentParsed = 0
	commandword = ''
	for index, character in enumerate(a):
		if not commandParsed:
			if not character.isspace():
				command += character
				continue
			commandParsed = 1
			commandword = ''.join(command)
		if not passWhitespace:
			if character.isspace():
				continue
			passWhitespace = 1
		if not argumentParsed:
			if character == '\n' or character == '\r':
				break;	
			argument += character
			continue
	return [commandword.lower(), ''.join(argument), a]

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
			continue
		elif not isValidChar(character):
			return 0
		index+=1
	return 1

#Check for valid characters by converting to ascii code and then assuring it isn't one of the banned characters
def isValidChar(a):
	intform = ord(a)
	return intform!= 10 and intform!=13 and 0 <= intform < 128

#Checks if the command is valid by looking it up in the dictionary of commands
def isValidCommand(command):
	if not command in commands:
		generateErrorMessage('command')
		return 0
	return 1

#Checks if the string is a valid number
def isValidNumber(number):
	for digit in number:
		asciiNumber = ord(digit)
		if not 48 <= asciiNumber <= 57:
			return 0
	if 0 <= int(number) <= 255:
		return 1
	return 0

#Returns the top of the command history
def top():
	if command_history:
		return command_history[-1]
	return 0

#Checks if the port arguments are valid and creates host address and port number
def isValidPortArgument(argument):
	port_arguments = argument.split(',')
	global client_port, client_hostname
	if len(port_arguments)!=6:
		return 0
	for pos in range (0,4):
		value = port_arguments[pos]
		if not isValidNumber(value):
			return 0
	for pos in range(4,6):
		value = port_arguments[pos]
		if not isValidNumber(value):
			return 0
	client_port = int(port_arguments[4]) * 256 + int(port_arguments[5])
	client_hostname = '.'.join(port_arguments[0:4])
	return 1

#Checks if a path leads to a valid file
def checkPath(path):
	if path[:1] == '/':
		return os.path.isfile(path[1:])
	return os.path.isfile(path)
		
#Generates an error message for the parameter code
def generateErrorMessage(code):
	global client_socket
	msg = errorcodes.get(code,"Invalid error code")
	sys.stdout.write(msg)
	client_socket.send(msg.encode())

def generateSuccessMessage(code, var = 0):
	global client_socket
	if var == 0:
		msg = successcodes.get(code,"Invalid code")
		client_socket.send(msg.encode())
	else:
		msg = (successcodes.get(code,"Invalid code") % var)
		client_socket.send(msg.encode())
	sys.stdout.write(msg)

#Checks if the argument is valid for the command
def isValidArgument(token):
	command = token[commandpos]
	argument = token[argumentpos]
	original = token [originalpos]
	argumentType = commands.get(command)
	if argumentType == 'string':
		if not " " in original:
			#This is checking for the lack of space between command and argument
			generateErrorMessage('command')
			return 0
		if not isString(argument) or not argument:
			generateErrorMessage('parameter')
			return 0
		#if command == 'retr':
			#if not checkPath(argument):
			#	generateErrorMessage('retr')
			#	return 
	elif command == 'type':
		if not argument in argumentType:
			generateErrorMessage('parameter')
			return 0
	elif command == 'port':
		if not isValidPortArgument(argument):
			generateErrorMessage('parameter')
			return 0
	elif argument or ' ' in original:
		generateErrorMessage('command')
		return 0
	if not original.endswith('\r\n'):
		generateErrorMessage('parameter')
		return 0
	return 1

#Returns 1 if logged in and 0 otherwise
def isLoggedIn():
	return outputflags[userflag] and outputflags[passflag]
#Command flow is:
#	User
#	Pass
#	Any commands
#	Quit
#End
#PORT must precede a RETR command
def commandExecution(tokenizedCommand):
	global file_copy_count
	command = tokenizedCommand[commandpos].lower()
	if command == 'user':
		outputflags[userflag] = 1
		outputflags[passflag] = 0
		generateSuccessMessage('user')
		return 1
	elif command == 'pass':
		if outputflags[userflag] == 1 and top() == 'user':
			outputflags[passflag] = 1
			generateSuccessMessage('pass')
			return 1
		else:
			generateErrorMessage('sequence')
			return 0
	elif command == 'type' and isLoggedIn():
			generateSuccessMessage('type', tokenizedCommand[argumentpos])
			return 1
	elif command == 'retr' and isLoggedIn():	
		file_name = tokenizedCommand[argumentpos]
		if not checkPath(file_name):
			generateErrorMessage('retr')
			return 0 
		if outputflags[portflag] == 1:
			generateSuccessMessage('retr')
			if file_name[:1] == '/':
				file_name = file_name[1:]
			try:
				#open tcp connection to client socket
				#throw 425 Can not open data connection if can't
				#make sure the tcp connection is open
				#socket.sendfile(file_name)
				tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				tcp_connection.connect((client_hostname,client_port))
				name = open(file_name,'rb')
				tcp_connection.sendfile(name)
				name.close()
				tcp_connection.close()
				generateSuccessMessage('retrdone')
			except IOError:
				generateErrorMessage('retr')
				return 0
			except OSError:
				generateErrorMessage('data')
				return 0
			#copy to client
			outputflags[portflag] = 0
			return 1
		else:
			generateErrorMessage('sequence')
			return 0
	elif command ==	'port' and isLoggedIn():
		outputflags[portflag] = 1
		generateSuccessMessage('port', client_hostname+','+str(client_port))
		return 1
	elif command == 'syst' and isLoggedIn():
		generateSuccessMessage('syst')
		return 1
	elif command == 'quit':
		generateSuccessMessage('quit')
		return 1
		#quit()
	elif command == 'noop':
		sys.stdout.write(successcodes.get('command'))
		return 1
	if top() == 'user':
		generateErrorMessage('sequence')
		return 0
	generateErrorMessage('notloggedin')
	return 0

def main():
	global port, server_socket, client_socket
	port = int(sys.argv[1])
	if not os.path.isdir(retrpath):
		os.mkdir(retrpath)
	server_socket = socket.socket(socket.AF_INET)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((socket.gethostname(),port))
	server_socket.listen(1)
	
	while True:
		(client_socket, address) = server_socket.accept()
		sys.stdout.write(ready)
		client_socket.send(ready.encode())
		while True:
			line = client_socket.recv(buffersize).decode()
			if line == "":
				client_socket.close()
				break
			sys.stdout.write(line)
			tokenizedCommand = tokenize(line)
			if tokenizedCommand and isValidCommand(tokenizedCommand[commandpos]) and isValidArgument(tokenizedCommand):
				if commandExecution(tokenizedCommand):
					#Only append the command to the history if it has been succesfully executed
					command_history.append(tokenizedCommand[commandpos])
			if tokenizedCommand[commandpos].lower() ==  'quit':
				client_socket.close()
				break;
if __name__ == "__main__":
	main()
