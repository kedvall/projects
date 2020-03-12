#! python3

# Program that check if a password is strong. A strong password:
# - Has at least 8 characters
# - Contains upper and lowercase letters
# - Has at least one digit

import re

def StrengthCheck(password):
	helpRegex = re.compile(r'^help$', re.I)
	helpCheck = helpRegex.findall(password)
	if helpCheck != []:
		print('''
A strong password:\n
- Has at least 8 characters\n
- Contains upper and lowercase letters\n
- Has at least one digit''')
		return False

	spaceRegex = re.compile(r'\s+')
	spaceCheck = spaceRegex.findall(password)
	if spaceCheck != []:
		print('Spaces are not allowed. Please remove all spaces.')
		return False

	lengthRegex = re.compile(r'\w{8,}')
	lengthCheck = lengthRegex.findall(password)
	if lengthCheck == []:
		print('Passwords must be at least 8 characters long.')
		return False

	upperRegex = re.compile(r'[A-Z]+')
	upperCheck = upperRegex.findall(password)
	if upperCheck == []:
		print('Passwords must contain at least 1 uppercase letter.')
		return False

	lowerRegex = re.compile(r'[a-z]+')
	lowerCheck = lowerRegex.findall(password)
	if lowerCheck == []:
		print('Passwords must contain at least 1 lowercase letter')
		return False

	digitRegex = re.compile(r'\d+')
	digitCheck = digitRegex.findall(password)
	if digitCheck == []:
		print('Passwords must contain at least 1 digit.')
		return False

	return True

# Start of program
# Prompt user for password and check against criteria
print('-----------------------------------------')
print('| Welcome to password strength checker! |')
print('| Enter help for password criteria.     |')
print('-----------------------------------------')
print()

while True:
	print('Enter password to check password strength: ', end='')
	password = input()
	if StrengthCheck(password):
		print()
		print('Good job, your password meets all criteria! Check another? ', end='')
		ans = input()
		if not ans.lower().startswith('y'):
			break
	print()

	
