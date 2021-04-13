import turtle	

class Grid:

	FONTSIZE = 30

	def __init__(self, sudokuObject):
		self.sudokuObject = sudokuObject
		self.sideLength = sudokuObject.sideLength
		self.quadrantLength = sudokuObject.quadrantLength

	def updateScreen(self):
		turtle.undo()
		turtle.write(self.sudokuObject, move = True, align = 'center', font = ('courier', self.FONTSIZE, 'normal'))

	def drawTitle(self):
		turtle.sety(((self.FONTSIZE) * self.sideLength) // 1.3)
		turtle.write('CLICK to Solve the Sudoku', move = True, align = 'center', font = ('courier', int(self.FONTSIZE * 1.2), 'normal'))

	def drawBox(self):
		for sideDivider in [20, 6]:
			otherSide = 6 if sideDivider == 20 else 20

			turtle.left(90)
			for i in range(self.quadrantLength):
				for j in range(self.quadrantLength):
					turtle.width(4)

					turtle.forward(((self.FONTSIZE + self.FONTSIZE//sideDivider) * self.quadrantLength) // self.quadrantLength)
					if j < self.quadrantLength - 1:
						turtle.width(1)

						turtle.left(90)
						turtle.forward((self.FONTSIZE + self.FONTSIZE//otherSide) * self.sideLength)
						turtle.right(180)
						turtle.forward((self.FONTSIZE + self.FONTSIZE//otherSide) * self.sideLength)
						turtle.left(90)

				if i < self.quadrantLength - 1:
					turtle.left(90)
					turtle.forward((self.FONTSIZE + self.FONTSIZE//otherSide) * self.sideLength)
					turtle.right(180)
					turtle.forward((self.FONTSIZE + self.FONTSIZE//otherSide) * self.sideLength)
					turtle.left(90)

		for sideDivider in [20, 6]:
			turtle.left(90)
			turtle.forward((self.FONTSIZE + self.FONTSIZE//sideDivider) * self.sideLength)

	def gridSetup(self, window):
		window.tracer(0)

		turtle.penup()
		self.drawTitle()

		turtle.home()
		turtle.sety((-(self.FONTSIZE) * self.sideLength) // 2)
		turtle.setx(((self.FONTSIZE + self.FONTSIZE//6) * self.sideLength) // 2)

		turtle.pendown()
		self.drawBox()
		turtle.penup()

		turtle.home()
		turtle.sety(-self.FONTSIZE * self.sideLength // 2)
		turtle.forward(1) #Nonsense command

		self.updateScreen()
		window.update()

	def helper(self,a,b):
		turtle.onscreenclick(None)
		self.sudokuObject.solve()

	def run(self):
		wn = turtle.Screen()
		turtle.hideturtle()
		turtle.speed(0)
		self.gridSetup(wn)
		turtle.onscreenclick(self.helper)
		turtle.done()
