#!/usr/bin/python3
import numpy as np
import pprint
from random import random
import sys
import bigfloat
from enum import Enum  
import copy
import pickle

SAVE_FOLDER = 'LEARNED/'

class LearningMethod(Enum):
	BACK_PROPAGATION = 1
	MOMENTUM = 2


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
	ETA = 0.1
	ALFA = 0.9 #momentum discount
	EPOCH = 500

	def __init__(self, layerIn, layerMid, layerOut):
		self.__layers = [layerIn, layerMid, layerOut]
		self.__weightW = [[random() for x in range(layerMid)]
						  for y in range(layerIn+1)]
		self.__weightV = [[random() for x in range(layerOut)]
						  for y in range(layerMid+1)]

		self.__lastWeightW = [[0 for x in range(layerMid)]
						  for y in range(layerIn+1)]
		self.__lastWeightV = [[0 for x in range(layerOut)]
						  for y in range(layerMid+1)]

		self.__learningMethod = LearningMethod.BACK_PROPAGATION
		pass

	def setLearningMethod(self, method):
		self.__learningMethod = method

	def setEpoch(self, e):
		self.EPOCH = e

	def Sim(self, values):
		(fi1, fi2) = self.__sim2(values)
		return fi2

	def save(self, name):
		with open(SAVE_FOLDER+name, 'wb') as output:
			pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

	def __sim2(self, values):
		val = values[:]
		val.insert(0, 1)
		fi1 = np.matmul(val, self.__weightW)

		fi1 = (1/(1+exponent(-fi1)))  # sigmoid
		# fi1 = fi1 / 1 + abs(fi1)		#Softsign

		val = fi1.tolist()
		val.insert(0, 1)
		fi2 = np.matmul(val, self.__weightV).tolist()
		return (fi1, fi2)

	def __singleFix(self, values, expected):
		val = values[:]
		(fi1, fi2) = self.__sim2(val)
		dOut = np.subtract(expected, fi2)
		dMid = np.matmul(self.__weightV, dOut)
		# dIn = np.matmul(self.__weightW, dMid[1:])

		derivative = fi1*(1-fi1)  # sigmoid
		# derivative = 1 / (1 + abs(fi1))**2	#Softsign

		w = self.ETA * dMid[1:] * derivative

		val.insert(0, 1)
		# nie wiem czy czasem nie odwrotinie
		w = np.outer(val, w)

		if self.__learningMethod == LearningMethod.MOMENTUM:
			# momentum = self.ALFA * np.array(self.__weightW)
			# momentum = self.ALFA * np.array(self.__lastWeightW)
			momentum = self.ALFA * np.subtract(self.__weightW, self.__lastWeightW)
			self.__lastWeightW = copy.deepcopy(self.__weightW)

		self.__weightW = np.add(self.__weightW, w).tolist()
		if self.__learningMethod == LearningMethod.MOMENTUM:
			self.__weightW = np.add(self.__weightW, momentum).tolist()

		# derivative = 1	# bo funkcja liniowa
		w = self.ETA * dOut
		cpFi = fi1.tolist()
		cpFi.insert(0, 1)
		w = np.outer(cpFi, w)
		if self.__learningMethod == LearningMethod.MOMENTUM:
			# momentum = self.ALFA * np.array(self.__weightV)
			# momentum = self.ALFA * np.array(self.__lastWeightV)
			momentum = self.ALFA * np.subtract(self.__weightV, self.__lastWeightV)
			self.__lastWeightV = copy.deepcopy(self.__weightV)

		self.__weightV = np.add(self.__weightV, w).tolist()
		if self.__learningMethod == LearningMethod.MOMENTUM:
			self.__weightV = np.add(self.__weightV, momentum).tolist()


	"""
		valuesArray and expectedArray shoud be a colums
	"""

	def Train(self, valuesArray, expectedArray):
		permutation = np.arange(len(valuesArray))
		for e in range(self.EPOCH):
			if(self.EPOCH > 1):
				print('Train Epoch:', e+1, '/', self.EPOCH, end='\r')
			np.random.shuffle(permutation)
			for i in permutation:
				self.__singleFix(valuesArray[i], expectedArray[i])
		if(self.EPOCH > 1):
			print()

	def print(self):
		print('W', np.shape(self.__weightW))
		pprint.pprint(self.__weightW)
		print('V', np.shape(self.__weightV))
		pprint.pprint(self.__weightV)


def Load(name):
	with open(SAVE_FOLDER+name, 'rb') as input:
		return pickle.load(input)


if __name__ == '__main__':
	pass
