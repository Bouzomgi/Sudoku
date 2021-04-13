import sudokuFront
import time

def squareRank(square):
	return (len(square.existingValues) * 100) + (square.coords[0] * 10) + square.coords[1]

class EmptySquare:

	def __init__(self, row, col, quadrantIndex):
		self.coords = (row, col)
		self.quadrantIndex = quadrantIndex
		self.existingValues = dict()

	def __repr__(self):
		return f'{self.coords}: {self.existingValues.keys()}'

	__str__ = __repr__

class Sudoku:

	def __init__(self, puzzle):
		self.puzzle = puzzle
		self.sideLength = len(puzzle[0])
		self.quadrantLength = int(self.sideLength ** 0.5)

		self.visual = sudokuFront.Grid(self)

		self.rowDict = {i:[] for i in range(self.sideLength)}
		self.colDict = {i:[] for i in range(self.sideLength)}
		self.quadrantDict = {i:[] for i in range(self.sideLength)}
		self.allDict = {}

		self.emptySquares = []
		self.initEmptySquares()

	def initEmptySquares(self):
		for row in range(self.sideLength):
			for col in range(self.sideLength):
				if self.puzzle[row][col] == None:
					quadrantIndex = self.findQuadrant(row, col)
					newSquare = EmptySquare(row, col, quadrantIndex)

					self.rowDict[row].append(newSquare)
					self.colDict[col].append(newSquare)
					self.quadrantDict[quadrantIndex].append(newSquare)
					self.allDict[(row, col)] = newSquare

					self.emptySquares.append(newSquare)

		for row in range(self.sideLength):
			for col in range(self.sideLength):
				val = self.puzzle[row][col]
				if val != None:
					quadrantIndex = self.findQuadrant(row, col)

					self.editLineValue(self.rowDict[row], val, 'add')
					self.editLineValue(self.colDict[col], val, 'add')
					self.editLineValue(self.quadrantDict[quadrantIndex], val, 'add')

		self.emptySquares.sort(key = squareRank)

	def findQuadrant(self, row, col):
		quadrant = (row//self.quadrantLength, col//self.quadrantLength)
		return quadrant[0]*3 + quadrant[1]

	def isAssignmentValid(self, row, col):
		val = self.puzzle[row][col]

		if val in self.allDict[(row,col)].existingValues:
			return False
		return True

	def editLineValue(self, content, val, action):
		for i in range(len(content)):
			if action == 'add':
				if val in content[i].existingValues:
					content[i].existingValues[val] += 1
				else:
					content[i].existingValues[val] = 1

			elif action == 'remove':
				if val in content[i].existingValues:
					content[i].existingValues[val] -= 1

					if content[i].existingValues[val] == 0:
						del content[i].existingValues[val]

	def updateEmptySquareList(self, row, col, action):
		quadrantIndex = self.findQuadrant(row, col)
		val = self.puzzle[row][col]

		self.editLineValue(self.rowDict[row], val, action)
		self.editLineValue(self.colDict[col], val, action)
		self.editLineValue(self.quadrantDict[quadrantIndex], val, action)

		self.emptySquares.sort(key = squareRank)

	def solve(self, withVisual = True):
		history = []
		currSquare = self.emptySquares[-1]
		targetRow, targetCol = currSquare.coords

		while len(self.emptySquares) > 0:

			if self.puzzle[targetRow][targetCol] == None:
				self.puzzle[targetRow][targetCol] = 1

			else:
				if self.puzzle[targetRow][targetCol] == 9:
					self.puzzle[targetRow][targetCol] = None
					
					if withVisual:
						self.visual.updateScreen()

					currSquare = history.pop()
					targetRow, targetCol = currSquare.coords
					self.emptySquares.append(currSquare)

					self.updateEmptySquareList(targetRow, targetCol, 'remove')

					continue

				self.puzzle[targetRow][targetCol] += 1

			if self.isAssignmentValid(targetRow, targetCol):

				if withVisual:
					self.visual.updateScreen()

				self.updateEmptySquareList(targetRow, targetCol, 'add')

				history.append(self.emptySquares.pop())

				if len(self.emptySquares) > 0:
					currSquare = self.emptySquares[-1]
					targetRow, targetCol = currSquare.coords

		return self.puzzle


	def __repr__(self):
		representation = []
		for row in self.puzzle:
			adjustedRow = [str(elem) if elem != None else ' ' for elem in row]
			representation.append(' '.join(adjustedRow))
		return '\n'.join(representation)

	__str__ = __repr__



puzzle1 = [[1, 8, 4, 3, None, None, 2, None, 9],
	[None, 7, 2, None, None, None, 3, None, None],
	[6, None, 3, None, 9, 8, None, None, None],
	[None, 4, 5, 6, 8, None, 1, None, None],
	[None, None, None, None, None, None, None, None, None],
	[None, None, 7, None, 2, 3, 5, 9, None],
	[None, None, None, 4, 1, None, 6, None, 7],
	[None, None, 6, None, None, None, 9, 1, None],
	[7, None, 8, None, None, 5, 4, 2, 3]]

puzzle2 = [[3, None, None, 5, None, None, 8, 6, None],
	[None, 4, None, None, None, 8, None, 2, None],
	[None, None, 6, 7, None, None, None, None, None],
	[None, 8, None, None, 9, None, None, 4, None],
	[None, None, 1, None, None, None, 7, None, None],
	[None, 7, None, None, 2, None, None, 3, None],
	[None, None, None, None, None, 4, 2, None, None],
	[None, 9, None, 2, None, None, None, 7, None],
	[None, 5, 4, None, None, 1, None, None, 3]]


x = Sudoku(puzzle2)
x.visual.run()

# x = Sudoku(puzzle2)
# a = time.time()
# print(x.solve(withVisual = False)
# b = time.time()
# print(f'Attempt 3: {b-a}')

