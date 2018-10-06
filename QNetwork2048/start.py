
import sys
sys.path.append('..')
from Game2048 import Game, DIRECTION
from Network import Net

class qNet2048(object):
	
	def __init__(self):
		self.game = Game()
		self.main()
	
	def main(self):
		self.game.Print()
		pass

def Run():
	qNet2048()
	pass