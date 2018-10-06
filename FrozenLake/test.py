#!/usr/bin/python3
import pygame
from FrozenLake.Game import Config, FrozenLake


def printTableOnScreen(screen, table):
	myfont = pygame.font.SysFont("monospace", 15)
	for i in range(len(table)):
		for j in range(len(table[0])):
			if table[i][j] == 1:
				color = (0,255, 255)
			elif table[i][j] == 2:
				color = (255,0,0)
			elif table[i][j] == 4:
				color = (255,255,255)
			else:
				color = (255,255,0)
			label = myfont.render(str(table[i][j]), 1, color)
			screen.blit(label, (20*j + 10, 20*i + 10))

def gameOver(status):
	print('gameOver', status)

def run():
	con = Config()
	con.setSize(13,20)
	con.setEnd(12,19)
	con.addHole(2,5)
	con.addHole(8,10)
	con.addHole(9,6)

	fl = FrozenLake(con)
	fl.onGameOver(gameOver)

	pygame.init()
	screen = pygame.display.set_mode((600, 600))
	clock = pygame.time.Clock()
	done = False
	while not done:
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_q:
				done = True
			if event.key == pygame.K_w:
				fl.moveUp()
			if event.key == pygame.K_s:
				fl.moveDown()
			if event.key == pygame.K_a:
				fl.moveLeft()
			if event.key == pygame.K_d:
				fl.moveRight()
			if event.key == pygame.K_r:
				fl.resetGame()
		m = fl.getMap()
		printTableOnScreen(screen, m)
		pygame.display.flip()
		screen.fill((0,0,0))

