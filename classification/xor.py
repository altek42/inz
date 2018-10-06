import sys
sys.path.append("..")
from Network.Network import Net
from random import random
from matplotlib import pyplot as plt
from pprint import pprint

class xor(object):
	
	def __init__(self):
		self.run()
		pass

	def prepareData(self):
		self.input = [ [(random() - 0.5)*2, (random() - 0.5)*2] for x in range(500) ]
		self.output = []
		for (x, y) in self.input:
			if x > 0 and y > 0 or x < 0 and y < 0:
				v=1
			else:
				v=-1
			self.output.append( [v, v*-1] )

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



