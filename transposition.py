#!/usr/bin/env python
#transposition cipher cracker
from math import floor
from sys import argv, exit

def decode(myStr, myKey):
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
		print "-h,--help	Print this help."
		print "-f FILE		Take cipher text from a file named FILE."
		print "-k			Assumed key value, which is the number of columns."
		print "-m			Maximum number of column sizes to try."
		exit(0)

	i = 1
	key = 1
	maxKey = 1
	ciph = ""
	while i < len(argv):
		if argv[i] == "-f": #if a file given
			with open(argv[i+1], "r") as f:
				ciph = f.read()

			i += 2
		elif argv[i] == "-k": #if key value given
			key = int(argv[i+1])
			i +=2
		elif argv[i] == "-m": #if max value given
			maxKey = int(argv[i+1])
			i += 2
		else: #if argument by itself, it is ciphertext
			if not ciph: #if ciph is not defined, grab argument for its value
				ciph = argv[i]

			i += 1

if len(ciph) < 4:
	print "Must have cipher text more than 4 characters."
	exit(-2)

if key > 1:
	start = key
	maxKey = key
else:
	start = 2
	if maxKey < 2:
		maxKey = len(ciph) / 2

for myKey in range(start,maxKey+1):
	print "Plain text with key %d" % myKey
	print "=" * 20
	print(decode(ciph, myKey)), "\n"
