
from .game import Game
from .const import DIRECTION

def start():
	a = Game()
	a.onGameOver(__handleGameOver)
	print(a.GetGrid())

	# while True:
	# 	a.Print()
	# 	d = input()
	# 	if d == 'q':
	# 		break
	# 	if d == 'a':
	# 		a.Move(DIRECTION.LEFT)
	# 	if d == 'd':
	# 		a.Move(DIRECTION.RIGHT)
	# 	if d == 'w':
	# 		a.Move(DIRECTION.UP)
	# 	if d == 's':
	# 		a.Move(DIRECTION.DOWN)

	# pass

def __handleGameOver():
	print('Game Over')
	pass