import sys
sys.path.insert(0, 'H:\\Documents\\Coding_projects')
sys.path.insert(1, 'H:\\Documents\\Coding_projects\\neat')
from neat import Population
from neat import Network
from neat import DataConf
from bot import Bot
import csv
import pygame

bots = []
pop = Population(1, 5, 4, False)
nets = pop.get_pop()

pygame.init()

win = pygame.display.set_mode((500,500))

bots.append(Bot(win, 100, 100, 1, nets[0], 4, False, (255, 0, 0),1))

loop = True

while loop:	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			loop = False
	



	win.fill((255,255,255))
	bots[0].go()


