import random
import copy

J = ([
	[0, 1],
	[1, 1]
],[
	[1, 0],
	[1, 1]
],[
	[1, 1],
	[1, 0]
],[
	[1, 1],
	[0, 1]
])

I = ([
	[2, 0],
	[2, 0]
],[
	[2, 2],
	[0, 0]
],[
	[0, 2],
	[0, 2]
],[
	[0, 0],
	[2, 2]
])

O = ([
	[3, 3],
	[3, 3]
],[
	[3, 3],
	[3, 3]
],[
	[3, 3],
	[3, 3]
],[
	[3, 3],
	[3, 3]
])

Z = ([
	[4, 0],
	[0, 4]
],[
	[0, 4],
	[4, 0]
],[
	[4, 0],
	[0, 4]
],[
	[0, 4],
	[4, 0]
])

D = ([
	[0, 5],
	[0, 0]
],[
	[0, 0],
	[0, 5]
],[
	[0, 0],
	[5, 0]
],[
	[5, 0],
	[0, 0]
])

BRICKS = [
	I, J
]

BOARD_WIDTH=5
BOARD_HEIGHT=5

class Brick(object):
	def __init__(self, shapeNum):
		self.x=0
		self.y=0
		self.rot=0
		self.shape = shapeNum
		pass

	def getShapeCopy(self):
		return copy.deepcopy(BRICKS[self.shape][self.rot])

	def getShape(self):
		return BRICKS[self.shape][self.rot]

	def moveDown(self):
		self.y+=1

	def moveUp(self):
		self.y-=1

	def moveRight(self):
		self.x+=1

	def rotate(self):
		self.rot += (self.rot + 1) % 4

class Game(object):

	#	board[y][x]
	#	x	+	->
	#	x	-	<-
	#	y	+	\/
	#	y	-	/\


	def __init__(self):
		self.brickLimit = 10000
		self.__onGameOver = None
		self.reset()		
	
	def reset(self):
		self.board=[[0 for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]
		self.__brickCouter = 0
		self.__score = 0
		self.__removeLines = 0
		self.__lastScore = 0
		self.__getNextBrick()

	def getNumActions(self):
		return (BOARD_WIDTH - 1) * 4

	def move(self, action):
		rot = action % 4
		moveTimes = action // 4
		self.__rotate(rot)
		self.__moveRight(moveTimes)
		self.__confirmMove()

	def onGameOver(self, func):
		self.__onGameOver = func

	def getState(self):
		
		# return self.__topLevelRepresentationStartegyState()
		return self.__counturStrategyState()
		# return self.__ownStrategyGetState()

	def __topLevelRepresentationStartegyState(self):
		vec = []
		for row in [-2,-1]:
			for cell in self.board[row]:
				if cell == 0:
					vec.append(0)
				else:
					vec.append(1)
		vec.extend(self.__getBrickState())
		return vec

	def __counturStrategyState(self):
		vec = [0 for i in range(BOARD_WIDTH)]
		for y in range(BOARD_HEIGHT):
			for x in range(BOARD_WIDTH):
				if vec[x] == 0 and self.board[y][x] != 0:
					vec[x] = BOARD_HEIGHT - y
		countur = []
		vecIter = iter(vec)
		lastCell = vecIter.__next__()
		for cell in vecIter:
			countur.append(cell- lastCell)
			lastCell = cell
		countur.extend(self.__getBrickState())
		return countur

	def __ownStrategyGetState(self):
		vec = [0 for i in range(BOARD_WIDTH)]
		emptyCells = 0
		for y in range(BOARD_HEIGHT):
			for x in range(BOARD_WIDTH):
				if vec[x] == 0 and self.board[y][x] != 0:
					vec[x] = BOARD_HEIGHT - y
				elif vec[x] != 0 and self.board[y][x] == 0:
					emptyCells += 1
		d = max(vec)-min(vec)
		if d <= 2 :
			d = 0
		else:
			d -= 2
		vec.extend(self.__getBrickState())
		vec.append(d)
		vec.append(emptyCells)
		return vec

	def getScoreDif(self):
		r = self.__score - self.__lastScore
		self.__lastScore = self.__score
		return r

	def getScore(self):
		return self.__score

	def getRemovedLines(self):
		return self.__removeLines

	def __getBrickState(self):
		vec = [0 for x in range(len(BRICKS))]
		vec[self.brick.shape] = 1
		return vec


	def __moveRight(self, times):
		while times > 0:
			times -= 1
			self.brick.moveRight()

	def __rotate(self, times):
		while times > 0:
			times -= 1
			self.brick.rotate()


	def __confirmMove(self):
		while self.__moveBrickDown():
			pass

	def __moveBrickDown(self):
		self.brick.moveDown()
		if not self.__isBrickOnBoardValid():
			self.brick.moveUp()
			self.__newTurn()
			return False
		else:
			# self.__score+=1
			return True
	
	def __newTurn(self):
		self.__connectBrictToBoard()
		self.__getNextBrick()
		self.__removeFullLines()
		self.__removeLastLines()

		
	def __removeLastLines(self):
		for i in [0,1]:
			for cell in self.board[2]:
				if cell != 0:
					self.board.remove(self.board[-1])
					self.board.insert(0, [0 for x in range(BOARD_WIDTH)])
					self.__removeLines += 1
					break

	def __isBoardFirstTwoLinesEmpty(self):
		for y in [0,1]:
			for cell in self.board[y]:
				if cell != 0:
					return False
		return True

	def __removeFullLines(self):
		lines = 0
		for line in self.board:
			fullLine = True
			for cell in line:
				if cell == 0:
					fullLine = False
					break
			if fullLine:
				lines+=1
				self.board.remove(line)
				self.board.insert(0, [0 for x in range(BOARD_WIDTH)])
		self.__addScoreForLines(lines)

	def __addScoreForLines(self, lines):
		if lines == 1:
			self.__score += 20
		elif lines == 2:
			self.__score += 50

	def __connectBrictToBoard(self):
		brick = self.brick.getShape()
		y = self.brick.y
		for row in brick:
			x = self.brick.x
			for cell in row:
				if cell != 0:
					self.board[y][x] = cell
				x+=1
			y+=1

	def __isBrickOnBoardValid(self):
		brick = self.brick.getShape()
		y = self.brick.y
		for row in brick:
			x = self.brick.x
			for cell in row:
				if cell != 0:
					if y >= BOARD_HEIGHT:
						return False
					if self.board[y][x] != 0:
						return False
				x+=1
			y+=1
		return True


	def __getNextBrick(self):
		if self.__brickCouter > self.brickLimit:
			# self.__score += 1000
			self.__gameOver(False)
			return
		self.__brickCouter += 1
		num = random.randint(0, len(BRICKS) -1)
		self.brick = Brick(num)

	def __gameOver(self, isWin):
		if self.__onGameOver != None:
			self.__onGameOver(isWin)

	def print(self):
		for row in self.board:
			for item in row:
				print(item, end=' ')
			print()
		print()