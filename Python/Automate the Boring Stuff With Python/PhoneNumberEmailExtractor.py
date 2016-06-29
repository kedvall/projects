#! python3
# PhoneNumberEmailExtractor.py - Finds phone numbers and email addresses on the clipboard

import pyperclip, re

phoneRegex = re.compile(r'''(
	(\d{3}|\(\d{3}\))?				# Area code
	(\s|-|\.)?						# Seperator
	(\d{3})							# First 3 digits
	(\s|-|\.)						# Seperator
	(\d{4})							# Last 4 digits
	(\s*(ext|x|ext.)\s*(\d{2,5}))?	# Extension
	)''', re.VERBOSE)

emailRegex = re.compile(r'''(
	[a-zA-z0-9._%+-]+		# Username
	@						# @ symbol
	[a-zA-Z0-9.-]+			# Domain name
	(\.[a-zA-z]{2,4})		# Dot-something
	)''', re.VERBOSE)

# Find matches in clipbaord text
text = str(pyperclip.paste())
matches = []

for groups in phoneRegex.findall(text):
	phoneNum = '-'.join([groups[1], groups[3], groups[5]])
	if groups[8] != '':
		matches.append(phoneNum)

for groups in emailRegex.findall(text):
	matches.append(groups[0])


# TODO: Copy results to the clipboard