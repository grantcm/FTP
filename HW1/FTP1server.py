#The approach to this problem was to make several methods that verified the types of data input. 
#They are isString, isValidChar, isValidCommand, and isValidArgument.
#Each method verifies that the passed parameter matches the expected types outlined in the assignment.
#The other methods are used to parse the input line into its respective parts: the command and the argument.
#This token is then used to verify whether or not it is a correct command.

import sys

commands = {'user':'string','pass':'string','type':'AI','syst':'none','noop':'none','quit':'none'}
errorcodes = {'command':'command', 'user':'username', 'pass':'password', 'type':'type-code', 'CRLF':'CRLF'}
commandpos = 0
argumentpos = 1
originalpos = 2
goodcommand = 'Command ok'

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
				break
			argument += character
			continue
	return [commandword, ''.join(argument), a]

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
	print(intform)
	return intform!= 10 and intform!=13 and 0 <= intform < 128

#Checks if the command is valid by looking it up in the dictionary of commands
def isValidCommand(command):
	if not command.lower() in commands:
		generateErrorMessage('command')
		return 0
	return 1

#Generates an error message for the parameter code
def generateErrorMessage(code):
	print('ERROR -- %s' % errorcodes.get(code,"Invalid error code"))

#Checks if the argument is valid for the command
def isValidArgument(token):
	command = token[commandpos].lower()
	argument = token[argumentpos]
	original = token [originalpos]
	argumentType = commands.get(command)
	if command == 'user':
		if not " " in original:
			generateErrorMessage('command')
			return
		if not isString(argument) or not argument:
			generateErrorMessage('user')
			return
	elif command == 'pass':
		if not " " in original:
			generateErrorMessage('command')
			return
		if not isString(argument) or not argument:
			generateErrorMessage('pass')
			return
	elif command == 'type':
		if not argument in argumentType:
			generateErrorMessage('type')
			return
	elif argument or ' ' in original:
		generateErrorMessage('CRLF')
		return
	if not original.endswith('\r\n'):
		generateErrorMessage('CRLF')
		return
	print(goodcommand)

#loops through stdin and determines if the input is a valid character
def main():
	command_list = sys.stdin.read().splitlines(keepends=True)
	for line in command_list:
		if '\n' in line:
			print(line, end="")
		else:
			print(line)
		tokenizedCommand = tokenize(line)
		if not tokenizedCommand:
			continue
		if not isValidCommand(tokenizedCommand[commandpos]):
			continue
		isValidArgument(tokenizedCommand)

if __name__ == "__main__":
	main()
