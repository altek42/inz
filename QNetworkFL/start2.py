import sys
sys.path.append('..')
from FrozenLake.Game import Config, FrozenLake
from random import randint
from random import random
from Network.Network import Net
import pprint


class qNetAlgorithm(object):
	EPOCH = 15000
	GRID_SIZE = 10

	def __init__(self):
		conf = Config()
		conf.setSize(self.GRID_SIZE, self.GRID_SIZE)
		conf.setEnd(self.GRID_SIZE-1, self.GRID_SIZE-1)
		conf.addHole(randint(0, 9), randint(0, 9))
		conf.addHole(randint(0, 9), randint(0, 9))
		conf.addHole(randint(0, 9), randint(0, 9))
		conf.addHole(randint(0, 9), randint(0, 9))
		conf.addHole(randint(0, 9), randint(0, 9))
		conf.addHole(randint(0, 9), randint(0, 9))
		conf.addHole(randint(0, 9), randint(0, 9))
		conf.addHole(randint(0, 9), randint(0, 9))
		conf.addHole(randint(0, 9), randint(0, 9))
		conf.addHole(randint(0, 9), randint(0, 9))
		conf.addHole(randint(0, 9), randint(0, 9))

		game = FrozenLake(conf)
		game.print()
		game.onGameOver(self.gameOver)

		self.config = conf
		self.game = game
		self.gamma = 0.8
		self.gameRuning = True

	def main(self):
		self.gameMap = self.game.getMap()
		self.net = Net(2, 30, 4)
		self.net.setEpoch(1)
		self.train()
		self.playGame()

	def playGame(self):
		self.createNewGame(0, 0)
		i = 0
		while self.gameRuning:
			print('\n---\n Move:', i)
			i += 1
			self.game.print()
			(maxQ, index) = self.getMaxQ()
			a = [0,0,0,0]
			a[index] = 1
			self.printDirection(a)
			self.move(a)
			if i > 21:
				return
		i += 1
		print(' Epoch:', i)
		self.game.print()

	def printDirection(self, move):
		if move[0] == 1:
			print('Direction up')
		if move[1] == 1:
			print('Direction down')
		if move[2] == 1:
			print('Direction left')
		if move[3] == 1:
			print('Direction right')

	def train(self):
		for i in range(self.EPOCH):
			print('Game Epoch:', i+1, '/', self.EPOCH, end='\r')
			pos = self.getRandomPosition()
			(posX, posY) = pos
			self.createNewGame(posX, posY)
			while self.gameRuning:
				state = self.getState()
				if random() < 0.2:
					nextMove = self.getRandMove()
				else:
					nextMove = self.getBestMove()
				qTab = self.qCrossReward()
				self.net.Train([state], [qTab])
				self.move(nextMove)

				
		print()
	
	def qCrossReward(self):
		qTab = []
		for i in range(4):
			self.game.savePosition()
			a = [0, 0, 0, 0]
			a[i] = 1
			isMove = self.move(a, True)
			(q, index) = self.getMaxQ()
			if isMove:
				reward = self.getReward()
			else:
				reward = -50
			maxQ = reward + self.gamma * q
			qTab.append(maxQ)
			self.game.loadPosition()
		return qTab
			

	def getRandMove(self):
		r = randint(0,3)
		a = [0, 0, 0, 0]
		a[r] = 1
		return a

	def getBestMove(self):
		a = [0, 0, 0, 0]
		(q, i) = self.getMaxQ()
		a[i] = 1
		return a

	def getMaxQ(self):
		state = self.getState()
		q = self.net.Sim(state)
		index = q.index(max(q))
		return (q[index], index)


	def getReward(self):
		(x, y) = self.game.getPosition()
		return self.getRewardForPosition(x,y)

	def getRewardForPosition(self, x, y):
		if not self.checkPosition(x,y):
			return -50
		v = self.gameMap[x][y]
		if v == 1:
			return -20
		if v == 2:
			return 20
		return 0

	def checkPosition(self, x, y):
		if x < 0:
			return False
		if y < 0:
			return False
		if x >= self.GRID_SIZE:
			return False
		if y >= self.GRID_SIZE:
			return False
		return True
	

	def move(self, action, isTest = False):
		if action[0] == 1:
			return self.game.moveUp(isTest)
		if action[1] == 1:
			return self.game.moveDown(isTest)
		if action[2] == 1:
			return self.game.moveLeft(isTest)
		if action[3] == 1:
			return self.game.moveRight(isTest)

	def getState(self):
		(xPos, yPos) = self.game.getPosition()
		en = []
		en.append(xPos)
		en.append(yPos)
		return en

	def getRandomPosition(self):
		x = randint(0, len(self.gameMap[0])-1)
		y = randint(0, len(self.gameMap)-1)
		return (x, y)

	def createNewGame(self, startX, startY):
		self.game.resetGame()
		self.game.setPosition(startX, startY)
		self.gameRuning = True

	def gameOver(self, res):
		self.gameRuning = False


def run():
	print('Run QNetwork')
	q = qNetAlgorithm()
	q.main()
