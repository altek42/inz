#!/usr/bin/python3
import numpy as np
import pprint
from random import random
import sys
import bigfloat

def exponent(x):
	a = x.astype(np.float128)

	a = np.exp(a)
	
	# b = a[~np.isfinite(a)]
	# print(b)
	# if len(b) > 0:
		# sys.exit()
	# a[~np.isfinite(a)] = 1
	return a


"""
	(x)-- W --(fi1)-- V --(fi2)->
"""
class Net(object):
	ETA=0.1
	EPOCH=500

	def __init__(self, layerIn, layerMid, layerOut):
		self.__layers=[layerIn, layerMid, layerOut]
		self.__weightW=[[random() for x in range(layerMid)] for y in range(layerIn+1)]
		self.__weightV=[[random() for x in range(layerOut)] for y in range(layerMid+1)]
		pass
	
	def setEpoch(self, e):
		self.EPOCH = e

	def Sim(self, values):
		(fi1, fi2) = self.__sim2(values)
		return fi2

	def __sim2(self, values):
		val=values[:]
		val.insert(0,1)
		fi1 = np.matmul(val, self.__weightW)
		
		fi1 = (1/(1+exponent(-fi1))) 	#sigmoid
		# fi1 = fi1 / 1 + abs(fi1)		#Softsign
		
		val = fi1.tolist()
		val.insert(0,1)
		fi2 = np.matmul(val, self.__weightV).tolist()
		return (fi1, fi2)

	def __singleFix(self,values, expected):
		val = values[:]
		(fi1, fi2) = self.__sim2(val)
		dOut = np.subtract(expected, fi2)
		dMid = np.matmul(self.__weightV, dOut)
		# dIn = np.matmul(self.__weightW, dMid[1:])

		derivative = fi1*(1-fi1)				#sigmoid
		# derivative = 1 / (1 + abs(fi1))**2	#Softsign
		
		w = self.ETA * dMid[1:] * derivative
		
		val.insert(0,1)
		#nie wiem czy czasem nie odwrotinie
		w = np.outer(val,w)
		
		self.__weightW = np.add(self.__weightW,w).tolist()
		# derivative = 1	# bo funkcja liniowa
		w = self.ETA * dOut
		cpFi = fi1.tolist()
		cpFi.insert(0,1)
		w = np.outer(cpFi, w)
		self.__weightV = np.add(self.__weightV,w).tolist()

	"""
		valuesArray and expectedArray shoud be a colums
	"""
	def Train(self, valuesArray, expectedArray):
		permutation = np.arange(len(valuesArray))
		for e in range(self.EPOCH):
			if(self.EPOCH > 1):
				print('Train Epoch:',e+1,'/',self.EPOCH,end='\r')
			np.random.shuffle(permutation)
			for i in permutation:
				self.__singleFix(valuesArray[i],expectedArray[i])
		if(self.EPOCH > 1):
			print()

	def print(self):
		print('W', np.shape(self.__weightW))
		pprint.pprint(self.__weightW)
		print('V', np.shape(self.__weightV))
		pprint.pprint(self.__weightV)

if __name__ == '__main__':
	pass


