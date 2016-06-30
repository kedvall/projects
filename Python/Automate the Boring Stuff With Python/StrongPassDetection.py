#! python3

# Program that check if a password is strong. A strong password:
# - Has at least 8 characters
# - Contains upper and lowercase letters
# - Has at least one digit

def StrengthCheck(password):
	spaceRegex = re.compile(r'\s+')
	spaceCheck = spaceRegex.findall(password)
	if spaceCheck != []:
		print('Spaces are not allowed. Please remove all spaces.')
		return None

	lengthRegex = re.compile(r'\w{8:}')
	lengthCheck = lengthRegex.findall(password)
	if lengthCheck == []:
		print('Passwords must be at least 8 characters long.')
		return None

	upperRegex = re.compile(r'[A-Z]+')
	upperCheck = upperRegex.findall(password)
	if upperCheck == []:
		print('Passwords must contain at least 1 uppercase letter.')
		return None

	lowerRegex = re.compile(r'[a-z]+')
	lowerCheck = lowerRegex.findall(password)
	if upperCheck == []:
		print('Passwords must contain at least 1 lowercase letter')
		return None