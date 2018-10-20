import pprint

class Config(object):
	def __init__(self):
		self.Width=10
		self.Height=10
		self.StartPosition=(0,0)
		self.EndPosition=(9,9)
		self.Holes=[]
		pass
	
	def setSize(self, w, h):
		self.Width = w
		self.Height = h

	def setStart(self, x,y):
		self.StartPosition = (x,y)
	
	def setEnd(self, x,y):
		self.EndPosition = (x,y)

	def addHole(self, x, y):
		self.Holes.append((x,y))

class FrozenLake(object):
	
	def __init__(self, config):
		self.__config = config
		self.__gameOverCallbacks = []
		self.__reset(config)
	
	def __reset(self, config):
		(x,y) = config.StartPosition
		self.__position= [x,y]
		self.sPos = self.__position[:]
		self.__createMap(config)
	
	def setPosition(self, x,y):
		self.__position= [x,y]
	
	def getPosition(self):
		return (self.__position[0],self.__position[1])
	
	def getEndPosition(self):
		return self.__config.EndPosition

	def __createMap(self,config):
		self.__map = [[0 for i in range(config.Width)] for j in range(config.Height)]
		for (x,y) in config.Holes:
			self.__map[y][x] = 1
		(x,y) = config.EndPosition
		self.__map[y][x] = 2
	
	def print(self):
		print('Mapa:',len(self.__map),'x',len(self.__map[0]))
		cpMap = self.__cpMap()
		count = len(cpMap)
		for i in range(count):
			for cell in cpMap[i]:
				print(cell,end=' ')
			print()

	def getMap(self):
		return self.__cpMap()

	def __cpMap(self):
		cpMap = [row[:] for row in self.__map]
		cpMap[self.__position[0]][self.__position[1]]=4
		return cpMap

	def savePosition(self):
		self.sPos = self.__position[:]
	
	def loadPosition(self):
		self.__position = self.sPos[:]

	def moveLeft(self, isTest = False):
		isMove = False
		if self.__position[1] > 0:
			self.__position[1] -= 1
			isMove = True
		if isTest:
			self.__checkGameStatus()
		return isMove

	def moveRight(self, isTest = False):
		isMove = False
		if self.__position[1] < len(self.__map[0])-1:
			self.__position[1] += 1
			isMove = True
		if isTest:
			self.__checkGameStatus()
		return isMove
	
	def moveDown(self, isTest = False):
		isMove = False
		if self.__position[0] < len(self.__map)-1:
			self.__position[0] += 1
			isMove = True
		if isTest:
			self.__checkGameStatus()
		return isMove

	def moveUp(self, isTest = False):
		isMove = False
		if self.__position[0] > 0:
			self.__position[0] -= 1
			isMove = True
		if isTest:
			self.__checkGameStatus()
		return isMove
	
	def __checkGameStatus(self):
		val = self.__map[self.__position[0]][self.__position[1]]
		if val == 1:
			self.__gameOver('lose')
		elif val == 2:
			self.__gameOver('win')

	def onGameOver(self, callback):
		self.__gameOverCallbacks.append(callback)

	def __gameOver(self, status):
		for f in self.__gameOverCallbacks:
			f(status)
	
	def resetGame(self):
		self.__reset(self.__config)
