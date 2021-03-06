from .Game2.game import Game
from Network.Network import Net, LearningMethod
from Network import LoadNet
from random import randint
from random import random

class script(object):

	def __init__(self):
		self.game = Game()
		self.game.onGameOver(self.handleGameOver)
		self.run()
		# self.trainForever()

	def run(self):
		net = self.qlearningNeuralNetwork(50000, 100, 0.8, 0.1)
		# net = LoadNet('tra_209')
		self.game.reset()
		self.__gameRunnig = True
		state = self.game.getState()
		while self.__gameRunnig:
			Q = net.Sim(state)
			action = Q.index(max(Q))
			self.game.move(action)
			state = self.game.getState()
			self.game.print()
		print(self.game.getScore())
	
	def trainForever(self):
		i = 0
		net = self.qlearningNeuralNetwork(100000, 100, 0.8, 0.1)
		# net = LoadNet('net_1_'+str(i))
		i+=1
		# net = self.qlearningNeuralNetwork(100000, 100, 0.8, 0.1)
		while True:
			print('Net learned:',i)
			net.save('net_1_'+str(i))
			i+=1
			net = self.qlearningNeuralNetwork(50000, 100, 0.8, 0.1, net)


	def qlearningNeuralNetwork(self, learningIterations, neuronsCount, gamma, epsilon = 0.1, net=None):
		actionCount = self.game.getNumActions()
		state = self.game.getState()

		if net == None:
			net = Net(len(state), neuronsCount, actionCount)
			net.setEpoch(1)

		bestScore = 0

		for i in range(learningIterations):
			print('Game Epoch:', i+1, '/', learningIterations, end='\r')
			self.__lastHoles = 0
			self.__gameRunnig = True
			self.game.reset()

			state = self.game.getState()
			while self.__gameRunnig:
				Q = net.Sim(state)
				action = Q.index(max(Q))
				reward = self.getReward(state)

				if random() < epsilon:
					action = randint(0, actionCount-1)
				self.game.move(action)
				nextState = self.game.getState()
				maxNextQ = max(net.Sim(nextState))
				Q[action] = reward + gamma * maxNextQ
				net.Train([state], [Q])
				state = nextState
			score = self.game.getScore()
			if score > bestScore:
				bestScore = score
				net.save('tra_'+str(bestScore))
		print()
		print('Best score:', bestScore)
		return net

	def getReward(self, state):
		score = self.game.getScoreDif()
		holes = state[-1]
		hill = state[-2]
		h = holes - self.__lastHoles
		self.__lastHoles = holes
		return score - h - hill


	def handleGameOver(self, isWin):
		self.__gameRunnig = False
		if isWin:
			print("Win!")
		# print('Game over isWin:', isWin)

def run():
	script()


