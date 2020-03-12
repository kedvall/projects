grid = [['.', '.', '.', '.', '.', '.'],
        ['.', 'O', 'O', '.', '.', '.'],
        ['O', 'O', 'O', 'O', '.', '.'],
        ['O', 'O', 'O', 'O', 'O', '.'],
        ['.', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', '.'],
        ['O', 'O', 'O', 'O', '.', '.'],
        ['.', 'O', 'O', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.']]

newGrid = []

def rotateGrid(originalGrid):
	for listIndex in range(6):
		for listNum in range(9):
			newGrid.append(originalGrid[listNum][listIndex])
			print(originalGrid[listNum][listIndex], end='')
		print('')

rotateGrid(grid)
print('')
print('Done!')