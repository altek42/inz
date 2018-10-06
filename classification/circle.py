import sys
sys.path.append("..")
from Network.Network import Net
from random import random
from matplotlib import pyplot as plt
from pprint import pprint
import math

class circle(object):
	
	def __init__(self):
		self.run()
		pass

	def prepareData(self):
		self.input = []
		self.output = []
		for i in range(500):
			x = (random() -0.5) * 2
			y = (random() -0.5) * 2
			d = math.sqrt(x**2 + y**2)
			if d > 0.5:
				x += x/2
				y += y/2
				self.output.append( [1, -1] )
			else:
				self.output.append( [-1, 1] )
			self.input.append([x,y])

	def showData(self):
		plt.figure('data')
		indices = [i for i, x in enumerate(self.input) if self.output[i][0] == 1]
		for i,(x,y) in enumerate(self.input):
			if i in indices:
				plt.plot(x,y,'r.')
			else:
				plt.plot(x,y,'g.')

	def showNetData(self, net, name):
		plt.figure(name)
		for x in self.input:
			v = net.Sim(x)
			if v[0] > 0 and v[1] < 0:
				plt.plot(x[0],x[1],'r.')
			elif v[0] < 0 and v[1] > 0:
				plt.plot(x[0],x[1],'g.')
			else:
				plt.plot(x[0],x[1],'b.')

	def run(self):
		self.prepareData()
		self.showData()
		net = Net(2,6,2)
		self.showNetData(net,'dumb')
		net.Train(self.input, self.output)
		self.showNetData(net,'trained')
		plt.show()



