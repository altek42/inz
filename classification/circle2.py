import sys
sys.path.append("..")
from Network.Network import Net
from random import random
from matplotlib import pyplot as plt
from pprint import pprint
import math

class circle2(object):
	
	def __init__(self):
		self.run()
		pass

	def prepareData(self):
		self.input = []
		self.output = []

		for i in range(100):
			ax = (random() -0.5) * 0.5
			ay = (random() -0.5) * 0.5
			bx = (random() -0.5) * 0.5
			by = (random() -0.5) * 0.5
			cx = (random() -0.5) * 0.5
			cy = (random() -0.5) * 0.5
			dx = (random() -0.5) * 2
			dy = (random() -0.5) * 2
			self.input.append([ ax, ay+0.5 ])
			self.input.append([ bx+0.5, by-0.5 ])
			self.input.append([ cx-0.5, cy-0.5 ])
			d=math.sqrt(dx**2+dy**2)
			vx=dx/d
			vy=dy/d
			self.input.append([ dx+1.2*vx, dy+1.2*vy ])
			self.output.append( [1, -1, -1, -1] )
			self.output.append( [-1, 1, -1, -1] )
			self.output.append( [-1, -1, 1, -1] )
			self.output.append( [-1, -1, -1, 1] )

	def showData(self):
		plt.figure('data')
		indices = [i for i, x in enumerate(self.input) if self.output[i][0] == 1]
		indices2 = [i for i, x in enumerate(self.input) if self.output[i][1] == 1]
		indices3 = [i for i, x in enumerate(self.input) if self.output[i][2] == 1]
		for i,(x,y) in enumerate(self.input):
			if i in indices:
				plt.plot(x,y,'r.')
			elif i in indices2:
				plt.plot(x,y,'k.')
			elif i in indices3:
				plt.plot(x,y,'y.')
			else:
				plt.plot(x,y,'g.')

	def showNetData(self, net, name):
		print('Show net data.')
		plt.figure(name)
		for x in self.input:
			v = net.Sim(x)
			self.printDot(x,v)

	def printDot(self, x, v):
		if   v[0] > 0 and v[1] < 0 and v[2] < 0 and v[3] < 0:
			plt.plot(x[0],x[1],'r.')
		elif v[0] < 0 and v[1] > 0 and v[2] < 0 and v[3] < 0:
			plt.plot(x[0],x[1],'g.')
		elif v[0] < 0 and v[1] < 0 and v[2] > 0 and v[3] < 0:
			plt.plot(x[0],x[1],'k.')
		elif v[0] < 0 and v[1] < 0 and v[2] < 0 and v[3] > 0:
			plt.plot(x[0],x[1],'y.')
		else:
			plt.plot(x[0],x[1],'b.')

	def showGridData(self, net):
		print('Show grid.')
		plt.figure('grid')
		x = [ (i/10)-2 for i in range(40) ]
		for i in x:
			for j in x:
				v = net.Sim([i,j])
				self.printDot([i,j],v)


	def run(self):
		self.prepareData()
		self.showData()
		net = Net(2,6,4)
		self.showNetData(net,'dumb')
		net.Train(self.input, self.output)
		self.showNetData(net,'trained')
		self.showGridData(net)
		plt.show()



