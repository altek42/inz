from pprint import pprint 
from Network.Network import Net, LearningMethod
from random import randint
from random import random
import os
import time

class flTry1(object):

	def __init__(self):
		self.grid = [
			[0,0,0,0],
			[0,1,0,0],
			[0,0,0,1],
			[1,1,0,2]
		]
		# self.grid = [
		# 	[0,0,0,0,0,0,0,0],
		# 	[0,0,0,0,0,0,0,0],
		# 	[0,0,0,1,0,0,0,1],
		# 	[0,0,0,0,0,0,0,0],
		# 	[0,0,0,1,0,0,0,0],
		# 	[0,1,1,0,0,0,1,0],
		# 	[0,1,0,0,1,0,1,0],
		# 	[0,0,0,1,0,0,0,2],
		# ]
		self.run()



	def run(self):
		self.printGrid()
		net = self.qlearningNeuralNetwork(self.grid, 50000, 5, 0.1, 0.8, 0.1)

		state=0
		for i in range(20):
			self.printGrid(state)
			if state == -1 or self.isFinalState(self.grid, state):
				break
			Q = net.Sim(self.stateToNetInput(self.grid, state))
			print("Q:",Q)
			action = Q.index(max(Q))
			state = self.nextState(self.grid, state, action)

	
	def reward(self, lake, state):
		if state < 0:
			return -1

		x = int(state / len(lake))
		y = int(state % len(lake[0]))
		if lake[x][y] == 1:
			return -1
		if lake[x][y] == 2:
			return 1
		return 0

	def stateToNetInput(self, lake, state):
		x = int(state / len(lake))
		y = int(state % len(lake[0]))
		return [x,y]

	def nextState(self, lake, state, action):
		x = int(state / len(lake))
		y = int(state % len(lake[0]))
		if action == 0:
			x += 1
		if action == 1:
			x -= 1
		if action == 2:
			y += 1
		if action == 3:
			y -= 1
		if x < 0 or y < 0 or x >= len(lake) or y>= len(lake[0]):
			return -1
		else:
			return x * len(lake) + y

	def isFinalState(self, lake, state):
		if state == -1:
			return False

		x = int(state / len(lake))
		y = int(state % len(lake[0]))
		return lake[x][y] == 1 or lake[x][y] == 2


	def qlearningNeuralNetwork(self, lake, learningIterations, neuronsCount, eta, gamma, epsilon = 0.1):
		statesCount = len(lake) * len(lake[0])
		actionCount = 4

		net = Net(2, neuronsCount, actionCount)
		net.setEpoch(1)
		# net.setLearningMethod(LearningMethod.MOMENTUM)

		for i in range(learningIterations):
			print('Game Epoch:', i+1, '/', learningIterations, end='\r')
			state = randint(0, statesCount-1)
			# state = 0
			if self.reward(lake,state) < 0:
				continue

			for j in range(40):
				# os.system('clear')
				# self.printGrid(state)
				# time.sleep(0.1)
				
				Q = net.Sim(self.stateToNetInput(lake,state))
				action = Q.index(max(Q))

				if random() < epsilon:
					action = randint(0, actionCount-1)
				
				newState = self.nextState(lake, state, action)
				rew = self.reward(lake, newState)

				if newState == -1:
					maxNewQ = 0
				else:
					maxNewQ = max(net.Sim(self.stateToNetInput(lake,newState)))
				Q[action] = rew + gamma * maxNewQ
				net.Train([self.stateToNetInput(lake,state)], [Q])

				prevState = state
				state = newState

				if state == -1 or self.isFinalState(lake, state):
					break

		print()
		return net



	def printGrid(self, state=-1):
		i = 0
		print()
		for row in self.grid:
			for item in row:
				if i == state:
					print('X', end=' ')
				else:
					print(item, end=' ')

				i+=1
			print()

	pass

	