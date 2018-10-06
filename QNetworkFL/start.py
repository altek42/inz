import sys
sys.path.append('..')
from FrozenLake.Game import Config, FrozenLake
from random import randint
from Network.Network import Net
import pprint

class qNetAlgorithm(object):
	EPOCH = 1000

	def __init__(self):
		conf = Config()
		conf.setSize(10,10)
		conf.setEnd(9,9)
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))
		conf.addHole(randint(0,9),randint(0,9))

		game = FrozenLake(conf)
		game.print()
		game.onGameOver(self.gameOver)

		self.config = conf
		self.game = game
		self.gamma = 0.8
		self.gameRuning = True

	def main(self):
		self.gameMap = self.game.getMap()
		self.net = Net(10,30,1)
		self.net.setEpoch(1)
		self.train()	
		self.playGame()

	def playGame(self):
		self.createNewGame(0,0)
		i=0
		while self.gameRuning:
			print(' Move:',i)
			i+=1
			self.game.print()
			(maxQ, action) = self.getMaxQ()
			self.move(action)
			if i > 21:
				return
		i+=1
		print(' Epoch:',i)
		self.game.print()

	def train(self):
		for i in range(self.EPOCH):
			print('Game Epoch:',i+1,'/',self.EPOCH,end='\r')
			pos = self.getRandomPosition()
			(posX, posY) = pos
			self.createNewGame(posX,posY)
			while self.gameRuning:
				state = self.getState()
				actions = self.getActions()
				nextMove = randint(0, len(actions)-1)
				nextMove = actions[nextMove]
				self.move(nextMove)
				(maxQ, a) = self.getMaxQ()
				sa = state[:]
				sa.extend(nextMove)
				newQ = self.getReward() + self.gamma * maxQ
				self.net.Train([sa],[[newQ]])
		print()

	def getReward(self):
		(x,y) = self.game.getPosition()
		v = self.gameMap[x][y]
		if v == 1: return -200
		if v == 2: return 200
		return 0

	def getMaxQ(self):
		state = self.getState()
		tab = []
		actions = self.getActions()
		for action in actions:
			cp = state[:]
			cp.extend(action)
			q = self.net.Sim(cp)
			tab.append(q)
		index = tab.index(max(tab))
		return (max(tab)[0], actions[index])

	def move(self, action):
		if action[0] == 1:
			self.game.moveUp()
			return
		if action[1] == 1:
			self.game.moveDown()
			return
		if action[2] == 1:
			self.game.moveLeft()
			return
		if action[3] == 1:
			self.game.moveRight()
			return

	#up
	#down
	#left
	#right
	def getActions(self):
		(xPos, yPos) = self.game.getPosition()
		ac = []
		if xPos > 0:
			ac.append([1,0,0,0])
		if xPos < len(self.gameMap)-1:
			ac.append([0,1,0,0])
		if yPos > 0:
			ac.append([0,0,1,0])
		if yPos < len(self.gameMap[0])-1:
			ac.append([0,0,0,1])
		return ac

	def defineCell(self,x,y):
		if x < 0 or y < 0 or x > len(self.gameMap)-1 or y > len(self.gameMap[0])-1:
			return 0
		if self.gameMap[x][y] == 1:
			return -1
		return 1

	def getState(self):
		(xPos, yPos) = self.game.getPosition()
		(xEndPos, yEndPos) = self.game.getEndPosition()
		en = []
		en.append(self.defineCell(xPos-1,yPos)) #up
		en.append(self.defineCell(xPos+1,yPos)) #down
		en.append(self.defineCell(xPos,yPos-1)) #left
		en.append(self.defineCell(xPos,yPos+1)) #right
		# for row in self.gameMap:
		# 	for cell in row:
		# 		if cell == 1:
		# 			en.append(-1)
		# 		else:
		# 			en.append(1)
					
		en.append(xEndPos - xPos)
		en.append(yEndPos - yPos)
		return en		

	def getRandomPosition(self):
		x = randint(0,len(self.gameMap[0])-1)
		y = randint(0,len(self.gameMap)-1)
		return (x,y)
	
	def createNewGame(self, startX, startY):
		self.game.resetGame()
		self.game.setPosition(startX,startY)
		self.gameRuning = True

	def gameOver(self, res):
		self.gameRuning = False

def run():
	print('Run QNetwork')
	q = qNetAlgorithm()
	q.main()