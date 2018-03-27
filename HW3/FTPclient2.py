import sys

successmessage='FTP reply %s accepted.  Text is : %s\n'
errormessage = 'ERROR -- %s\n'
replycodes = {'150':'File status okay.','200':'Command OK.',
		'215':'UNIX Type: L8.','220':'COMP 431 FTP server ready.',
		'230':'Guest login OK.','250':'Requested file action completed.',
		'331':'Guest access OK, send password.',
		'500':'Syntax error, command unrecognized','501':'Syntax error in parameter.',
		'503':'Bad sequence of commands.','530':'Not logged in.','550':'File not found or access denied.'}
specialcodes = ['Command OK.','Type set to I.','Type set to A.','Port command successful']


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

#For each line in, verfiy it ends in a crlf, then strip that and split on the first space. Check if the reply code is valid, then check if the text is a string
for line in sys.stdin:
	sys.stdout.write(line)
	if not line.endswith('\r\n'):
		sys.stdout.write(errormessage % "<CRLF>")
		continue
	command = line.strip('\r\n').split(None, 1)
	if len(command) != 2:
		sys.stdout.write(errormessage % 'reply-code')
	elif command[0] in replycodes:
		if isString(command[1]):
			sys.stdout.write(successmessage % (command[0], command[1]))
		else:
			sys.stdout.write(errormessage % 'reply-text')
			continue
	else:
		sys.stdout.write(errormessage % 'reply-code')
