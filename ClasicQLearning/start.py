import sys
sys.path.append('..')
from FrozenLake.Game import Config, FrozenLake
from random import randint
import pprint

class qAlgorithm(object):
	EPOCH = 1000

	def __init__(self):
		conf = Config()
		conf.setSize(10,10)
		conf.setEnd(9,9)
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))

		game = FrozenLake(conf)
		game.print()
		game.onGameOver(self.gameOver)

		self.config = conf
		self.game = game
		self.gamma = 0.8
		self.gameRuning = True

	def gameOver(self, status):
		self.gameRuning = False

	def createNewGame(self, startX, startY):
		self.game.resetGame()
		self.game.setPosition(startX,startY)
		self.gameRuning = True
	
	def main(self):
		self.gameMap = self.game.getMap()
		self.initQRTable()
		self.train()
		self.playGame()
	
	def getRandomPosition(self):
		x = randint(0,len(self.gameMap[0])-1)
		y = randint(0,len(self.gameMap)-1)
		return (x,y)

	def playGame(self):
		self.createNewGame(0,0)
		i=0
		while self.gameRuning:
			print(' Epoch:',i)
			i+=1
			self.game.print()
			pos = self.game.getPosition()
			direction = max(self.qTable[pos], key=self.qTable[pos].get)
			self.move(direction)
		i+=1
		print(' Epoch:',i)
		self.game.print()
		

	def train(self):
		for i in range(self.EPOCH):
			print(' Epoch:',i+1,'/',self.EPOCH,end='\r')
			pos = self.getRandomPosition()
			(posX, posY) = pos
			self.createNewGame(posX,posY)
			while self.gameRuning:
				r = self.rTable[pos]
				nextMove = randint(0,len(r)-1)
				nextMove = [*r][nextMove]
				self.move(nextMove)
				newPos = self.game.getPosition()
				maxQ = max(self.qTable[newPos], key=self.qTable[newPos].get)
				self.qTable[pos][nextMove] = r[nextMove] + self.gamma * self.qTable[newPos][maxQ]
				pos = newPos
		print()

	def move(self, nextMove):
		if nextMove == 'right':
			self.game.moveRight()
		elif nextMove == 'left':
			self.game.moveLeft()
		elif nextMove == 'up':
			self.game.moveUp()
		elif nextMove == 'down':
			self.game.moveDown()

	def initQRTable(self):
		self.rTable = {}
		self.qTable = {}
		for i in range(len(self.gameMap)):
			for j in range(len(self.gameMap[0])):
				t = {}
				t2 = {}
				if j > 0: 
					t['left'] = self.getReward(i,j-1)
					t2['left'] = 0
				if j < len(self.gameMap[0])-1:
					t['right'] = self.getReward(i,j+1)
					t2['right'] = 0
				if i > 0:
					t['up'] = self.getReward(i-1,j)
					t2['up'] = 0
				if i < len(self.gameMap)-1:
					t['down'] = self.getReward(i+1,j)
					t2['down'] = 0
				self.rTable[(i,j)]=t
				self.qTable[(i,j)]=t2

	def getReward(self, x,y):
		v = self.gameMap[x][y]
		if v == 1: return -200
		if v == 2: return 200
		return 0

def run():
	q = qAlgorithm()
	q.main()
