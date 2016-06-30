#! python3

# This program performs the strip() method
# It will remove the characters speficied in the second arguement
# If no other argument is specified, all whitespace characters will be removed

import re

def Strip(text, stripChar=' '):
	stripRegex = re.compile(r'^(' + re.escape(stripChar) + r')+|(' + re.escape(stripChar) + r')+$' )
	print(stripRegex)
	stripTest = stripRegex.findall(text)
	print(stripTest)

Strip('HELLOTestingHELLOHELLO', 'HELLO')
