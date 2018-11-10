from neupy import algorithms, layers
import sys
sys.path.append("..")
from Network.Network import Net
from random import random
from matplotlib import pyplot as plt
from pprint import pprint
import math
import numpy as np


class sincos(object):
	DATA_SIZE = 500

	def __init__(self):
		self.run()

	def prepareData(self):
		self.input = []
		self.output = []
		for i in range(self.DATA_SIZE):
			x = 10*i/self.DATA_SIZE

			y1 = math.sin(x)
			y2 = math.cos(x)

			self.input.append([x])
			self.output.append([y1, y2])

	def showData(self):
		plt.figure('data')
		y1 = []
		y2 = []
		for (i1, i2) in self.output:
			y1.append(i1)
			y2.append(i2)
		plt.plot(self.input[:], y1)
		plt.plot(self.input[:], y2)
		plt.legend(['sin', 'cos'], loc='lower left')

	def showNetData(self, net, name):
		plt.figure(name)
		y1 = []
		y2 = []

		for x in self.input:
			# v = net.Sim(x)
			v = net.predict([x])
			y1.append(v[0][0])
			y2.append(v[0][1])
		plt.plot(self.input[:], y1)
		plt.plot(self.input[:], y2)
		plt.legend(['sin', 'cos'], loc='lower left')

	def run(self):
		self.prepareData()
		self.showData()
		# net = Net(1,8,2)
		lmnet = algorithms.LevenbergMarquardt([
			layers.Input(1),
			layers.Sigmoid(8),
			layers.Sigmoid(2),
		],
		verbose=True,
		shuffle_data=True)

		self.showNetData(lmnet, 'dumb')
		# net.Train(self.input, self.output)
		a = np.array(self.input)
		b = np.array(self.output)
		lmnet.fit(a, b, epochs=100)
		self.showNetData(lmnet, 'trained')
		plt.show()


def run():
	sincos()
	pass
