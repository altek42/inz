
import sys
sys.path.append('..')
from Game2048 import Game, DIRECTION
from Network import Net
from pprint import pprint
import random

class qNet2048(object):
	EPOCH = 2000
	
	def __init__(self):
		self.net = Net(20, 50, 1)
		self.net.setEpoch(1)
		self.gamma = 0.8
		self.main()
	
	def main(self):
		self.train()
		self.playGame()

	def playGame(self):
		self.initNewGame()
		i=0
		while self.gameRuning:
			print(' Move:',i)
			i+=1
			self.game.Print()
			(action, bestValue) = self.getMaxQ()
			self.game.Move(action)
		i+=1
		print(' Epoch:',i)
		self.game.Print()

	def train(self):
		for i in range(self.EPOCH):
			print('Game Epoch:',i+1,'/',self.EPOCH,end='\r')
			self.initNewGame()
			while self.gameRuning:
				state = self.gridToVector()
				action = random.choice(list(DIRECTION))
				self.game.Move(action)
				(action, bestValue) = self.getMaxQ()
				inValue = state + self.directionToVector(action)
				newQ = self.game.GetLastMoveScore() + self.gamma * bestValue
				self.net.Train([inValue],[[newQ]])
			print('\nScore: ',self.game.GetTotalScore())
		print()

	def getMaxQ(self):
		directions = self.simDirections()
		best = max(directions, key=directions.get)
		return (best, directions[best][0])

	def simDirections(self):
		gridVector = self.gridToVector()
		result = {}
		for direction in DIRECTION:
			inputArray = gridVector[:] + self.directionToVector(direction)
			result[direction] = self.net.Sim(inputArray)
		return result

	def directionToVector(self, direction):
		if direction == DIRECTION.LEFT:
			return [1.0, 0.0, 0.0, 0.0]
		if direction == DIRECTION.RIGHT:
			return [0.0, 1.0, 0.0, 0.0]
		if direction == DIRECTION.UP:
			return [0.0, 0.0, 1.0, 0.0]
		if direction == DIRECTION.DOWN:
			return [0.0, 0.0, 0.0, 1.0]

	def gridToVector(self):
		tab = self.game.GetGrid()
		i = []
		for row in tab:
			i += row
		maxValue = max(i)
		return [ x/maxValue for x in i ]

	def initNewGame(self):
		self.game = Game()
		self.game.onGameOver(self.handleGameOver)
		self.gameRuning = True

	def handleGameOver(self):
		self.gameRuning = False

def Run():
	qNet2048()