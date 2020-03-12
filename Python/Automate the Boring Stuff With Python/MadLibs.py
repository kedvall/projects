#! python3

# MadLibs.py - Play Mad Libs!

import os

# Define keyword swap function
def keywordSwap(word):
	if word.lower().startswith(('a', 'e', 'i', 'o', 'u')):
		print('Enter an ' + word.lower() + ':')
		userText = input()
	else:
		print('Enter a ' + word.lower() + ':')
		userText = input()
	return libsContent.replace(word, userText, 1)

keywords = ['ADJECTIVE', 'NOUN', 'ADVERB', 'VERB']

# Start program
print('Welcome to Mad Libs! Loading from file MadLibsStart.txt...')
print()
print()

# Find Mad Libs start file and read the content as a string separated by delimiter ' '
libsFile = open(os.path.abspath('.') + os.path.sep + 'MadLibsStart.txt')
libsContent = libsFile.read()
libsFile.close()

# Loop through all items and get user input for keywords
while True:
	if any(keyword in libsContent for keyword in keywords):
		for index in keywords:
			if (libsContent.find(index)) != -1:
				libsContent = keywordSwap(index)
	else:
		break

# Print and export new Mad Libs to text file
print(libsContent)

newLibs = open(os.path.abspath('.') + os.path.sep + 'NewMadLibs.txt', 'w')
newLibs.write(libsContent + '\n')
newLibs.close()