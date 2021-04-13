import sudokuFront
import time

class Stack:

	def __init__(self):
		self.container = []

	@property
	def isEmpty(self):
		return self.container == []

	@property
	def peek(self):
		if self.isEmpty:
			return None
		return self.container[0]

	def push(self, val):
		self.container.append(val)

	def pop(self):
		if self.isEmpty:
			return None
		return self.container.pop()


class Sudoku:

	FONTSIZE = 30

	def __init__(self, puzzle):
		self.puzzle = puzzle
		self.sideLength = len(puzzle[0])
		self.quadrantLength = int(self.sideLength ** 0.5)

		self.visual = sudokuFront.Grid(self)

		self.allRows = [set() for i in range(self.sideLength)]
		self.allCols = [set() for i in range(self.sideLength)]
		self.allQuadrants = [set() for i in range(self.sideLength)]

		self.initValiditySets()

	def initValiditySets(self):
		for row in range(self.sideLength):
			for col in range(self.sideLength):
				self.addSquareToSets(row, col)

	def addSquareToSets(self, row, col):
		val = self.puzzle[row][col]
		if val != None:
			quadrantIndex = self.findQuadrant(row, col)

			self.allRows[row].add(val)
			self.allCols[col].add(val)
			self.allQuadrants[quadrantIndex].add(val)

	def removeSquareFromSets(self, row, col):
		val = self.puzzle[row][col]
		quadrant = self.findQuadrant(row, col)

		self.allRows[row].remove(val)
		self.allCols[col].remove(val)
		self.allQuadrants[quadrant].remove(val)


	def findQuadrant(self, row, col):
		quadrant = (row//self.quadrantLength, col//self.quadrantLength)
		return quadrant[0]*3 + quadrant[1]

	def isAssignmentValid(self, row, col):
		val = self.puzzle[row][col]
		quadrantIndex = self.findQuadrant(row, col)

		if val in self.allRows[row] or val in self.allCols[col] or val in self.allQuadrants[quadrantIndex]:
			return False
		return True

	def findTotalEmptySquares(self):
		total = 0
		for row in self.puzzle:
			for val in row:
				if val == None:
					total += 1
		return total

	def findNextEmptySquare(self):
		for row in range(self.sideLength):
			for col in range(self.sideLength):
				if self.puzzle[row][col] == None:
					return (row, col)
		return None

	def solve(self, withVisual = True):

		history = Stack()
		squaresToFill = self.findTotalEmptySquares()
		targetRow, targetCol = self.findNextEmptySquare()

		while squaresToFill:

			if self.puzzle[targetRow][targetCol] == None:
				self.puzzle[targetRow][targetCol] = 1

			else:
				if self.puzzle[targetRow][targetCol] == 9:
					self.puzzle[targetRow][targetCol] = None
					
					if withVisual:
						self.visual.updateScreen()

					squaresToFill += 1

					targetRow, targetCol = history.pop()
					self.removeSquareFromSets(targetRow, targetCol)

					continue

				self.puzzle[targetRow][targetCol] += 1

			if self.isAssignmentValid(targetRow, targetCol):

				self.addSquareToSets(targetRow, targetCol)

				if withVisual:
					self.visual.updateScreen()

				squaresToFill -= 1
				history.push((targetRow, targetCol))

				if squaresToFill:
					targetRow, targetCol = self.findNextEmptySquare()

		return self.puzzle

	def __repr__(self):
		representation = []
		for row in self.puzzle:
			adjustedRow = [str(elem) if elem != None else 'X' for elem in row]
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

# a = time.time()
# x.solve(withVisual = False)
# b = time.time()
# print(f'Attempt 2: {b-a}')

