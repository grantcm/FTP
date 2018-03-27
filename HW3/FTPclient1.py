import sys
import socket
import os
import re

commands = ['quit','get','connect']
eol=os.linesep
connected=0
validconnect = ['USER anonymous\r\n','PASS guest@\r\n','SYST\r\n','TYPE I\r\n']
port=8000

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

#Helper function to print errors
def printError(error):			
	print("ERROR -- %s" % error)

#Parser the command from the input line
def commandParser(line):
	global connected, port
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
		connected=1
		port = 8000
	elif(command == 'get'):
		if not isPathname(line[1]):
			printError("pathname")
			return 0
	elif(command == 'quit'):
		sys.stdout.write("QUIT accepted, terminating FTP client%s" % eol)
		sys.stdout.write("QUIT\r\n")
		quit()	
	if connected == 0:
		printError("expecting CONNECT")
		return 0
	return 1

#Executes the command, performing appropriate output to stdout when necessary
def executeCommand(commandobj):
	global port
	command = commandobj[0].lower()
	if command == 'connect':
		args = commandobj[1].split()
		sys.stdout.write("CONNECT accepted for FTP server at host %s and port %s%s" % (args[0],args[1],eol))
		for line in validconnect:
			sys.stdout.write(line)
	elif command == 'get':
		sys.stdout.write("GET accepted for %s%s" % (commandobj[1], eol))
		my_ip = socket.gethostbyname(socket.gethostname()).replace('.',',')
		portstr = str(int(port/256))+","+str(port%256)
		sys.stdout.write("PORT %s,%s\r\n" % (my_ip, portstr))
		port+=1
		sys.stdout.write("RETR %s\r\n" % commandobj[1])

	return

#Reads in each line and calls helper functions
for line in sys.stdin:
	sys.stdout.write(line)
	command = line.rstrip(eol)
	commandobj = command.split(None,1)
	if commandParser(commandobj):
		executeCommand(commandobj)
	
