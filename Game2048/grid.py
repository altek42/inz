from .settings import Settings
from .tile import Tile


class Grid(object):

	def __init__(self):
		self.__initTable()
		super()

	def __initTable(self):
		self.__table = [[Tile() for z in range(Settings.SIZE)]
		                      for x in range(Settings.SIZE)]

	def get(self, x, y):
		return self.__table[x][y].value

	def set(self, x, y, value):
		self.__table[x][y].value = value

	def getTable(self):
		return [[x.value for x in row] for row in self.__table]

	def __isLock(self, x, y):
		return self.__table[x][y].isLock

	def __lock(self, x, y):
		self.__table[x][y].isLock = True

	def __unlockAll(self):
		for row in self.__table:
			for item in row:
				item.Unlock()

	def CellsAvailable(self):
		cells = []
		for x in range(Settings.SIZE):
			for y in range(Settings.SIZE):
				if self.__table[x][y].value == 0:
					cells.append((x, y))
		return cells

	def Move(self, vector):
		ran = range(Settings.SIZE)
		(vecX, vecY) = vector
		self.__unlockAll()

		self.__isMoved = False		
		x = 0
		for y in ran:
			if vecX == 0:
				a = y
				b = x
			else:
				a = x
				b = y
			if vecX < 0:
				a = -a - 1
			if vecY < 0:
				b = -b -1
			self.__moveTile(a, b, vector)
		return self.__isMoved

	def __moveTile(self, x, y, vector):
		(vx, vy) = vector
		if not self.__isInBounds( x+vx, y+vy, vector ):
			return
		self.__moveTile( x+vx, y+vy, vector )
		
		value = self.get(x,y)
		if value == 0:
			return
		nextValue = self.get(x+vx, y+vy)
		if nextValue == 0:
			self.__swapTiles( (x,y), (x+vx, y+vy) )
			self.__isMoved = True
			self.__moveTile( x+vx, y+vy, vector )
			return
		if value == nextValue:
			self.__mergeTile(x,y,vector)
			self.__isMoved = True
			return

	def __mergeTile(self,x,y,vector):
		(vecX,vecY) = vector
		if self.__isLock(x,y) or self.__isLock(x+vecX,y+vecY):
			return
		value = self.get(x,y)
		self.set(x,y,0)
		self.set(x+vecX,y+vecY,value*2)
		self.__lock(x+vecX,y+vecY)

	def __swapTiles(self, posA, posB):
		(xa,ya) = posA
		(xb,yb) = posB
		(self.__table[xa][ya], self.__table[xb][yb]) = (self.__table[xb][yb], self.__table[xa][ya])

	def __isInBounds(self, x, y, vector):
		(vx, vy) = vector
		a = x
		b = y
		if vx < 0:
			a = -a -1
		if vy < 0:
			b = -b -1
		return a >= 0 and a < Settings.SIZE and b >= 0 and b < Settings.SIZE
	
	def Print(self):
		ran = range(Settings.SIZE)
		for x in ran:
			for y in ran:
				cell = self.__table[x][y].value
				print(cell,end='\t')
			print()
			print()
