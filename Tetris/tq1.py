from .Game3.game import Game
import pickle
from Network.Network import Net

SAVE_FOLDER = 'LEARNED/Q_TABLE/'

class script(object):
	def __init__(self):
		self.game = Game()
		self.game.onGameOver(self.handleGameOver)
		self.__gameRunnig = True
		self.Q = self.load('q1')
		self.run()

	def run(self):
		net = self.learn(10000, 100)

	def learn(self, epoch, neuronsCount):
		actionCount = self.game.getNumActions()
		state = self.game.getState()
		net = Net(len(state), neuronsCount, actionCount)
		net.setEpoch(epoch)

		(iData, oData) = self.transformQToLearningData()
		net.Train(iData, oData)
		return net

	def transformQToLearningData(self):
		i = []
		o = []
		maxValue = 0
		for item in self.Q:
			i.append(list(item))
			o.append(self.Q[item])
			m = max(self.Q[item])
			if m > maxValue:
				maxValue = m
		no = []
		for item in o:
			no.append([x - maxValue for x in item])
		return (i, no)


	def handleGameOver(self, isWin):
		self.__gameRunnig = False

	def load(self, name):
		with open(SAVE_FOLDER+name, 'rb') as input:
			return pickle.load(input)

def run():
	script()