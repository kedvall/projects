grid = [['-', '|', '|', '|', '|', '|', '|', '-'],
        ['-', '.', '.', '.', '.', '.', '.', '-'],
        ['-', '.', 'O', 'O', '.', '.', '.', '-'],
        ['-', 'O', 'O', 'O', 'O', '.', '.', '-'],
        ['-', 'O', 'O', 'O', 'O', 'O', '.', '-'],
        ['-', '.', 'O', 'O', 'O', 'O', 'O', '-'],
        ['-', 'O', 'O', 'O', 'O', 'O', '.', '-'],
        ['-', 'O', 'O', 'O', 'O', '.', '.', '-'],
        ['-', '.', 'O', 'O', '.', '.', '.', '-'],
        ['-', '.', '.', '.', '.', '.', '.', '-'],
        ['-', '|', '|', '|', '|', '|', '|', '-']]

newGrid = []

def rotateGrid(originalGrid):
	for listIndex in range(len(originalGrid[0])):
		for listNum in range(len(originalGrid)):
			newGrid.append(originalGrid[listNum][listIndex])
			print(originalGrid[listNum][listIndex], end='')
		print('')

rotateGrid(grid)
print('')
print('Done!')