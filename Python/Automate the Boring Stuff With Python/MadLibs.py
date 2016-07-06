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
	return userText

keywords = {'ADJECTIVE', 'NOUN', 'ADVERB', 'VERB', 'ADJECTIVE.', 'NOUN.', 'ADVERB.', 'VERB.'}

# Start program
print('Welcome to Mad Libs! Loading from file MadLibsStart.txt...')
print()
print()

# Find Mad Libs start file and read the content as a string separated by delimiter ' '
libsFile = open(os.path.abspath('.') + os.path.sep + 'MadLibsStart.txt')
libsContent = libsFile.read().split()
libsFile.close()

# Loop through all items and get user input for keywords
for index in range(len(libsContent)):
	if libsContent[index] in keywords:
		libsContent[index] = keywordSwap(libsContent[index])

# Rejoin words for export
libOutput = ' '.join(libsContent)

# Print and export new Mad Libs to text file
print(libOutput)

newLibs = open(os.path.abspath('.') + os.path.sep + 'NewMadLibs.txt', 'w')
newLibs.write(libOutput + '\n')
newLibs.close()