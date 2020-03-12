#! python3

# TablePrinter.py - Takes in list of strings and prints them in a right aligned table

def printTable(tableData):
	# Create a list with same number of entries as inner lists in tableData
	colWidth = [0] * len(tableData)

	# Loop through inner lists in tableData to find longest string
	for outerIndex in range(len(tableData)):
		for innerIndex in tableData[outerIndex]:
			if len(innerIndex) > colWidth[outerIndex]:
				colWidth[outerIndex] = len(innerIndex)

	# Iterate through tableData and print in right justified columns using 
	#	max string length as rjust() parameter
	for index in range(len(tableData)):
		print('-' * (colWidth[index]), end='')
	print('-' * 10)

	for listItem in range(len(tableData[0])):
		for listNumber in range(len(tableData)):
			print('| ' + tableData[listNumber][listItem].rjust(colWidth[listNumber]) + ' ', end='')
		print('|')

	for index in range(len(tableData)):
		print('-' * (colWidth[index]), end='')
	print('-' * 10)

# Start of program	
tableData = [['apples', 'oranges', 'cherries', 'banana'],
             ['Alice', 'Bob', 'Carol', 'David'],
             ['dogs', 'cats', 'moose', 'goose']]

printTable(tableData)