from enum import Enum

class DIRECTION(Enum):
	LEFT=1
	RIGHT=2
	UP=3
	DOWN=4

def VECTOR(dir):
	if dir == DIRECTION.LEFT:
		return (0, -1)
	if dir == DIRECTION.RIGHT:
		return (0, 1)
	if dir == DIRECTION.UP:
		return (-1, 0)
	if dir == DIRECTION.DOWN:
		return (1, 0)