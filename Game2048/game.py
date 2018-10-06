from numpy import random
from .settings import Settings
from .grid import Grid
from .const import VECTOR

class Game(object):

	def __init__(self):
		self.__grid = Grid()
		self.__addStartTiles()
	
	def __addStartTiles(self):
		for i in range(Settings.START_TILES):
			self.__addRandomTile()

	def __addRandomTile(self):
		cells = self.__grid.CellsAvailable()
		if len(cells) == 0:
			self.__gameOver()
			return
		r = random.randint(len(cells))
		(x, y) = cells[r]
		if random.rand() < 0.9: 
			value = 2 
		else:
			value = 4 
		self.__grid.set(x,y, value)

	def GetGrid(self):
		return self.__grid.getTable()

	def Move(self, direction):
		if self.__grid.Move(VECTOR(direction)):
			self.__addRandomTile()
	
	def __gameOver(self):
		if self.__gameOverFunc:
			self.__gameOverFunc()

	def onGameOver(self, func):
		self.__gameOverFunc = func
	
	def Print(self):
		self.__grid.Print()
		print()
		