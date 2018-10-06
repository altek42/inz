
class Tile(object):
	def __init__(self):
		self.value = 0
		self.isLock = False

	def Unlock(self):
		self.isLock = False

	def __str__(self):
		return self.value