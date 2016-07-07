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
# - Have user select file
# - Have user select search column, data retrieval column, and column to paste data
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

# TODO: Add functions

# Import necessary libraries and greet user
import openpyxl, os, re, pyperclip, sys
print(' Excel Data Scraper v1.0 '.center(50, '='))
print('Currently in Beta... will have nice GUI soon :)')
print()

# First step, user enters path to Excel file to be scraped
while True:
	# Get file path from user
	print('Enter path to Excel file including file extension')
	print('\tEx. C:\\Users\\intern\\data.xlsx')
	print('Path (Press Enter to quit): ', end='')
	#filePath = r'C:\Users\intern\Documents\test.xlsx' # For quick testing
	filePath = input()

	# Check if Enter is pressed and quit if true
	if filePath == '':
		sys.exit()
	
	# Cleanup user input... NEVER trust the user to do it right
	elif not filePath.endswith('.xlsx'):
		print('\tStandard Excel extension (.xlsx) not found, append it? (Y/N) ', end='')
		ans = input()
		if ans.lower().startswith('y'):
			filePath += '.xlsx'

	# Check that the file acutally exists
	if not os.path.exists(filePath):
		print('\tFile not found at ' + filePath + '!')
		print()
		print()
	else:
		print('\tSuccess! File found at ' + filePath)
		break

print('Exited loop!')