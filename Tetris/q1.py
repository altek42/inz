from .Game3.game import Game
from random import randint
from random import random
import pickle

SAVE_FOLDER = 'LEARNED/Q_TABLE/'


class script(object):
	
# Q = {
#	state1 = {
#		action1 = value1
#		action2 = value2
#		action3 = value3
#	},
#	state2 = {
#		action1 = value1
#		action2 = value2
#		action3 = value3
#	},
# }

	def __init__(self):
		self.game = Game()
		self.game.onGameOver(self.handleGameOver)
		self.__gameRunnig = True
		self.Q = {}
		self.run()

	def run(self):
		self.qLearning(32, 0.8, 0.1)

		self.game.reset()
		self.__gameRunnig = True
		state = self.game.getState()
		while self.__gameRunnig:
			Q = self.getQForState(state)
			action = Q.index(max(Q))
			self.game.move(action)
			state = self.game.getState()
		self.save('q1')
		print('q size', len(self.Q))
		print('Score:', self.game.getScore())
		print('Height:', self.game.getRemovedLines())


	def qLearning(self, learningGames, gamma, epsilon):
		actionCount = self.game.getNumActions()
		bestScore = 0

		for i in range(learningGames):
			print('Game Epoch:', i+1, '/', learningGames, end='\r')
			self.__gameRunnig = True
			self.game.reset()
			self.__removedLines = self.game.getRemovedLines()

			state = self.game.getState()
			while self.__gameRunnig:
				Q = self.getQForState(state)
				action = Q.index(max(Q))
				if random() < epsilon:
					action = randint(0, actionCount-1)
				self.game.move(action)
				nextState=self.game.getState()
				reward = self.getReward()
				nextQ = self.getQForState(nextState)
				maxNextQ = max(nextQ)
				Q[action] = reward + gamma * maxNextQ
				self.setNewQForState(state, Q)
				state = nextState
			score = self.game.getScore()
			if score > bestScore:
				bestScore = score
		print()
		print('Best score:', bestScore)

	def setNewQForState(self, state, q):
		k = tuple(state)
		self.Q[k] = q

	def getReward(self):
		rl = self.game.getRemovedLines()
		d = rl - self.__removedLines
		self.__removedLines = rl
		return self.game.getScoreDif() - d

	def getQForState(self, state):
		k = tuple(state)
		if not k in self.Q:
			self.Q[k] = [0 for x in range(self.game.getNumActions())]
		return self.Q[k]


	def handleGameOver(self, isWin):
		self.__gameRunnig = False

	def save(self, name):
		with open(SAVE_FOLDER+name, 'wb') as output:
			pickle.dump(self.Q, output, pickle.HIGHEST_PROTOCOL)


def run():
	script()