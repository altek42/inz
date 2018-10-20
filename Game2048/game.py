from numpy import random
from .settings import Settings
from .grid import Grid
from .const import VECTOR

class Game(object):

	def __init__(self):
		self.__score = 0
		self.__lastMoveScore = 0
		self.__grid = Grid()
		self.__addStartTiles()
	
	def __addStartTiles(self):
		for i in range(Settings.START_TILES):
			self.__addRandomTile()

	def __addRandomTile(self):
		cells = self.__grid.CellsAvailable()
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
			self.__updateScore()
			self.__addRandomTile()
		else:
			cells = self.__grid.CellsAvailable()
			if len(cells) == 0:
				self.__gameOver()
				return

	def __updateScore(self):
		score = self.__grid.getScore()
		self.__lastMoveScore = score
		self.__score += score
	
	def GetTotalScore(self):
		return self.__score
	
	def GetLastMoveScore(self):
		return self.__lastMoveScore

	def __gameOver(self):
		if self.__gameOverFunc:
			self.__gameOverFunc()

	def onGameOver(self, func):
		self.__gameOverFunc = func
	
	def Print(self):
		self.__grid.Print()
		print()
		