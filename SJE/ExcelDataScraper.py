#! python3

#########################################################################################
# ExcelDataScraper.py 																	#
# Written by Kanyon Edvall																#						
#									 													#
# This program allows you to traverse any excel sheet and find data of interest 	   	#
# There are currently two search modes: 											   	#
# 	1. Keyword search: Finds relevant data based on proximity to a keyword or keywords 	#
#	2. Exact search: Finds relevant data based on an exact match 						#
# Keyword search uses Regex expressions to find context of keywords and allows the 		#
# 	user to select which context options they want to search for 						#
#	Ex. Keyword: pn may return Context: pn, PN, P/N, P-N, Pn, P N, etc. 				#
#########################################################################################

# This program will have a GUI counterpart... Not done quite yet
# For now CLI only 

# Program Needs (keyword first):
# + Have user select file
# + Have user select sheet
# + Have user select search mode (keyword or exact)
#		Keyword generates a regex and finds many permutations
#		Exact searches for an exact match of the search term
# + Have user select colInRow or keywordOffset match mode
#		colInRow pulls data from another column in the current row on successful match
#		keyword offset copies data from the same row and column based on an offset or pattern
# + Have user select offset or pattern
# + Have user select search column, data retrieval column, and column to paste data
# + Verify columns
# + Ask user for text they want to search for
# - Generate broad Regex using text
# - Use above Regex to find context and possible permutations of keyword
# - Ask user to select which results they want to include in their search
# - Perform row by row search of SEARCHCOL
# - Enumerate results as they occur, copying EXTRACTDATA to DESTIN
# - Optionally write message in cells with no data
# - Display current row of SEARCHOL / total (progress)
# - Display message when data extraction is finished

# Functions
def clear():
	os.system('cls')
	print(' Excel Data Scraper v1.0 '.center(80, '='))
	print('Currently in Beta... will have nice GUI soon :)')
	print()

def getTerm():
	# Ask user for text they want to search for
	print('Enter text to search for. Put a period (.) between letters to allow for variation matching')
	print('Ex: p.n may return pn, PN, P/N, P-N, Pn, P N, etc. May be multiple words')
	print('Search Term: ', end='')
	searchTerm = input()

def getCol(colType):
	# Get column data from user
	while True:
		# Print custom prompt
		if colType == 'search':
			print('Which column would you like to search?')
		elif colType == 'copy':
			print('Which column would you like to copy from when given criteria is met?')
		else:
			print('Which column would you like to copy the selected data to?')

		# Print generic prompt
		print('Column: ', end='')
		userInput = input().upper()

		# Verify user actually input something correctly
		if not userInput.isalpha():
			clear()
			print('Column must be a letter or letters (Ex C, or AB)')
			print()
		else:
			try:
				cols[colType] = column_index_from_string(userInput)
				break
			except ValueError:
				clear()
				print('Value out of range. Range is from A to XFD')
				print()
	# User input successful and verified, print selection
	clear()
	print('Column ' + userInput + ' selected as ' + colType + ' column.')
	print()

# Required dictionaries, lists, tuples, and other variables
validExt = ('.xlsx', '.xlsm', '.xltx', '.xltm')
cols = {'search':'', 'copy':'', 'paste':''}
searchMode = matchMode = searchTerm = ''

# Import necessary modules and greet user
import openpyxl, os, re, pyperclip, sys
from openpyxl.cell import get_column_letter, column_index_from_string
clear()

# First step, user enters path to Excel file to be scraped
while True:
	# Get file path from user
	print('Enter path to Excel file including file extension')
	print('\tEx. C:\\Users\\intern\\data.xlsx')
	#print('Path (Press Enter to quit): ', end='')
	#filePath = input()
	print(r'Path (Press Enter to quit): C:\Users\intern\Documents\test.xlsx')
	filePath = r'C:\Users\intern\Documents\test.xlsx' # For quick testing

	# Check if Enter is pressed and quit if true
	if filePath == '':
		sys.exit()
	
	# Cleanup user input... NEVER trust the user to do it right
	elif not filePath.endswith('.xlsx'):
		print('\tStandard Excel extension (.xlsx) not found, append it? (Y/N) ', end='')
		userInput = input()
		if userInput.lower().startswith('y'):
			filePath += '.xlsx'

	# Check that extension is valid and file actually exists
	if not filePath.endswith(validExt):
			clear()
			print('File format not supported. Supported formats are: .xlsx, .xlsm, .xltx, and .xltm')
			print()
	else:
		if not os.path.exists(filePath):
			clear()
			print('\tFile not found at ' + filePath + '. Please try again')
			print()
		else:			
			wb = openpyxl.load_workbook(filePath)
			wbName = os.path.basename(filePath)
			break
clear()
print('\tFile found. Loading ' + wbName + '...')
print()

# Step two, user enters sheet name
while True:
	# Get sheet name from user
	print('Enter the name of the Excel sheet (Type List Sheets to see all available sheets)')
	print('Sheet Name (or press Enter for Active Sheet): ', end='')
	userInput = input()

	# Check input for errors or special phrases
	if userInput.lower() == 'list sheets':
		clear()
		print('Available sheets for ' + wbName + ': ', end='')
		print(', '.join(wb.get_sheet_names()))
		print()
	elif userInput == '':
		sheet = wb.active
		break
	else:
		try:
			sheet = wb.get_sheet_by_name(userInput)
			break
		except KeyError:
			clear()
			print(userInput + ' not found in ' + wbName)
			print()
clear()
print('\t' + sheet.title + ' selected.')
print()

# Step three, user selects search mode
while True:
	print('Select search mode (keyword or exact)')
	print('Mode: ', end='')
	userInput = input().lower()

	if userInput == 'keyword':
		searchMode = 'keyword'
		break
	elif userInput == 'exact':
		searchMode = 'exact'
		break
	else:
		clear()
		print('Search mode not found: ' + userInput)
		print('Valid options are keyword or exact')
		print()
clear()
print('\tUsing ' + searchMode + ' search mode')
print()

# Step four, user selects match mode
while True:
	print('Select match mode (keywordOffset or colInRow)')
	print('Mode (Enter k or c): ', end='')
	userInput = input().lower()

	if userInput == 'keywordOffset' or userInput == 'k':
		matchMode = 'keywordOffset'
		break
	elif userInput == 'colInRow' or userInput == 'c':
		matchMode = 'colInRow'
		break
	else:
		clear()
		print('Match mode not found: ' + userInput)
		print('Valid options are keywordOffset or colInRow')
		print()
clear()
print('\tUsing ' + matchMode + ' match mode')
print()

#############################################################
# KEYWORD - Generates a Regex and finds many permutations 	#
#############################################################
if searchMode == 'keyword':
	#############################################
	# colInRow - Pull data from another column 	#
	#############################################
	if matchMode == 'colInRow':
		# Get search term
		getTerm()
		clear()

		# Step one, user selects columns to use
		getCol('search')
		getCol('copy')
		getCol('paste')

		# Step two, verify user selected columns
		while True:
			clear()
			print('Column selection: ')
			print('\tSearch column ' + get_column_letter(cols['search']) + ' for criteria (search).')
			print('\tCopy data from column ' + get_column_letter(cols['copy']) + ' on successful match (copy).')
			print('\tPaste copied data into column ' +  get_column_letter(cols['paste']) + ' (paste).')
			print()
			print('Are all columns correct? Enter yes or enter name of column you wish to change.')
			print('Column names (search, copy, or paste): ', end='')
			userInput = input().lower()

			if userInput == 'yes' or userInput == 'y':
				break
			elif userInput in cols.keys():
				print()
				getCol(userInput)
			else:
				while userInput not in cols.keys():
					print()
					print('Column name ' + userInput + ' not found.')
					print('Column names are search, copy, or paste: ', end='')
					userInput = input().lower()
				print()
				getCol(userInput)
		clear()
		# Finished getting user options
		# keyword / colInRow

	#############################################################
	# keywordOffset - Copies data from the same row and column 	#
	#	based on an offset or pattern 							#
	#############################################################
	else:
		# Get search term
		getTerm()
		clear()

		# Select offset or pattern mode
		while True:
			print('Enumerate data based on static offset or custom pattern?')
			print('Enter offset or pattern: ', end='')
			userInput = input()

			if userInput == 'offset':
				while True:
					clear()
					print('How many characters after keyword should copy begin?')
					print('Offset (spaces count): ', end='')
					offset = input()
					# Verify it's a number
					if not offset.isdigit():
						clear()
						print('Offset must be a number (Ex 42)')
						print()
					else:
						break
				break

			elif userInput == 'pattern':
				clear()
				print('Enter pattern as a Regex (sorry, no auto generation yet)')
				pattern = input()
				break

			else:
				clear()
				print(userInput + ' is not a valid option')
				print('Enter offset or pattern: ', end='')
				print()
	# Finished getting user options
	# keyword / keywordOffset / ( offset OR pattern )

#############################################################
# EXACT - Searches for an exact match of the search term 	#
#############################################################
else:
	print('Enter text to search for, may be multiple words')
	print('Search Term: ', end='')
	searchTerm = input()

	#############################################
	# colInRow - Pull data from another column 	#
	#############################################
	if matchMode == 'colInRow':
		# Get search term
		getTerm()
		clear()

		# Step one, user selects columns to use
		getCol('search')
		getCol('copy')
		getCol('paste')

		# Step two, verify user selected columns
		while True:
			clear()
			print('Column selection: ')
			print('\tSearch column ' + get_column_letter(cols['search']) + ' for criteria (search).')
			print('\tCopy data from column ' + get_column_letter(cols['copy']) + ' on successful match (copy).')
			print('\tPaste copied data into column ' +  get_column_letter(cols['paste']) + ' (paste).')
			print()
			print('Are all columns correct? Enter yes or enter name of column you wish to change.')
			print('Column names (search, copy, or paste): ', end='')
			userInput = input().lower()

			if userInput == 'yes' or userInput == 'y':
				break
			elif userInput in cols.keys():
				print()
				getCol(userInput)
			else:
				while userInput not in cols.keys():
					print()
					print('Column name ' + userInput + ' not found.')
					print('Column names are search, copy, or paste: ', end='')
					userInput = input().lower()
				print()
				getCol(userInput)
		clear()
		# Finished getting user options
		# exact / colInRow

	#############################################################
	# keywordOffset - Copies data from the same row and column 	#
	#	based on an offset or pattern 							#
	#############################################################
	else:
		# Get search term
		getTerm()
		clear()

		# Select offset or pattern mode
		while True:
			print('Enumerate data based on static offset or custom pattern?')
			print('Enter offset or pattern: ', end='')
			userInput = input()

			if userInput == 'offset':
				while True:
					clear()
					print('How many characters after keyword should copy begin?')
					print('Offset (spaces count): ', end='')
					offset = input()
					# Verify it's a number
					if not offset.isdigit():
						clear()
						print('Offset must be a number (Ex 42)')
						print()
					else:
						break
				break

			elif userInput == 'pattern':
				clear()
				print('Enter pattern as a Regex (sorry, no auto generation yet)')
				pattern = input()
				break

			else:
				clear()
				print(userInput + ' is not a valid option')
				print('Enter offset or pattern: ', end='')
				print()
	# Finished getting user options
	# exact / keywordOffset / ( offset OR pattern )