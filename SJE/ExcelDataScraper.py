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
# + Have user select search column, data retrieval column, and column to paste data
# + Verify columns
# - Have user select search mode (keyword)
# - Ask user for text they want to search
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
	print(' Excel Data Scraper v1.0 '.center(50, '='))
	print('Currently in Beta... will have nice GUI soon :)')
	print()

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

# Required dictionaries, lists, and tuples
validExt = ('.xlsx', '.xlsm', '.xltx', '.xltm')
cols = {'search':'', 'copy':'', 'paste':''}

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

# Step three, user selects columns to use
getCol('search')
getCol('copy')
getCol('paste')

# Step four, verify user selected columns
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

# So far so good!
print('Done!')