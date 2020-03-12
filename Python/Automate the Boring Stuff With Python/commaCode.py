def listToString(incommingList):
	outputString = ''

	for index in range(len(incommingList) - 1):
		outputString += str(incommingList[index]) + ', '
	outputString += 'and ' + incommingList[len(incommingList) - 1]
	return outputString

spam = ['apples', 'bananas', 'tofu', 'cats', 'dogs', 'mice', 123, 456,789, 'done!']

returnVal = listToString(spam)
print(returnVal)