#!/usr/bin/env python
#transposition cipher cracker
from math import floor
from sys import argv, exit

def decode(myStr, myKey):
	"""
	Decode is the function that will decode one instance of cipher text with one specified value
	for number of columns, referred to as the key.

	myStr: The cipher text to be cracked.
	myKey: The key, or number of columns.

	Returns the decoded string in plain text as a string.
	"""

	strLen = len(myStr)
	rows = list()
	counter = 0
	i = 0
	last = 0
	leftover = strLen % myKey #num of rows with one extra character
	minNum = int(floor(float(strLen) / float(myKey)))
	while i < strLen: #construct rows
		if counter < leftover:
			i += minNum + 1
		else:
			i += minNum

		if i > strLen:
			rows.append(myStr[last:])
		else:
			rows.append(myStr[last:i])

		last = i
		counter += 1
	
	columns = list()
	i = 0
	while i < len(rows): #construct columns
		j = 0
		for char in rows[i]:
			index = j % len(rows[i])
			if index == len(columns):
				columns.append(char)
			else:
				columns[index] += char
			j += 1

		i += 1

	return "".join(columns) #return the columns joined together for the plaintext result


if len(argv) < 1:
	print "Usage: %s [CIPHER_TEXT] [-f CIPHER_TEXT_FILE] [-k KEY] [-m MAX_KEY_SIZE]" % argv[0]
	print "You must give at least one argument."
	exit(-1)
else:
	if argv[1] == "-h" or argv[1] == "--help":
		print "Usage: %s [CIPHER_TEXT] [-f CIPHER_TEXT_FILE] [-k KEY] [-m MAX_KEY_SIZE]\n" % argv[0]
		print("This script will attempt to brute force the column size key with a maximum number "
			  "of half the cipher text length and print all results by default.")
		print("You may give the cipher text as an argument, or you can specify the -f flag and "
			  "specify the name of a file containing the cipher text.\n")
		print "-h,--help			Print this help."
		print "-f,--file FILE		Take cipher text from a file named FILE."
		print "-k,--key				Assumed key value, which is the number of columns."
		print "-m,--max,--maxkey	Maximum number of column sizes to try."
		print ("-p,--phrase			A phrase you think will be in the plaintext. If found in the "
			   "plaintext, only that result will be printed. This helps make cracking faster and "
			   "output easier to read. The longer the phrase, the more accurate the prediction.")
		exit(0)

	i = 1
	key = 1
	maxKey = 1
	ciph = ""
	phrase = ""
	while i < len(argv):
		if argv[i] == "-f" or argv[i] == "--file": #if a file given
			with open(argv[i+1], "r") as f:
				ciph = f.read()

			i += 2
		elif argv[i] == "-k" or argv[i] == "--key": #if key value given
			key = int(argv[i+1])
			i +=2
		elif argv[i] == "-m" or argv[i] == "--max" or argv[i].lower() == "--maxkey": #if max value given
			maxKey = int(argv[i+1])
			i += 2
		elif argv[i] == "-p" or argv[i] == "--phrase": #if phrase given
			phrase = argv[i+1]
			i += 2
		else: #if argument by itself, it is ciphertext
			if not ciph: #if ciph is not already defined, grab argument for its value
				ciph = argv[i]

			i += 1


print "\n" #extra newline for formatting

if len(ciph) < 4:
	print "Must have cipher text more than 4 characters."
	exit(-2)

#remove newlines from cipher text because it screws things up
ciph = ciph.replace("\n", "")

if key > 1:
	start = key
	maxKey = key
else:
	start = 2
	if maxKey < 2:
		maxKey = len(ciph) / 2

if phrase:
	for myKey in range(start,maxKey+1):
		result = decode(ciph, myKey)
		if phrase in result:
			print "Match found with key of %d" % myKey
			print "=" * (24 + len(str(myKey)))
			print result
			exit(0)

	print "No matches found. To see all results, try again without specifying a phrase."
else:
	for myKey in range(start,maxKey+1):
		print "Plain text with key %d" % myKey
		print "=" * (20 + len(str(myKey)))
		print(decode(ciph, myKey)), "\n"
