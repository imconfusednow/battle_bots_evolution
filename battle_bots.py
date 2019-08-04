import sys
sys.path.insert(0, 'H:\\Documents\\Coding_projects')
sys.path.insert(1, 'H:\\Documents\\Coding_projects\\neat')
from neat import Population
from neat import Network
from neat import DataConf
from bot import Bot
import csv
import pygame
import numpy

states = ["Menu", "Train", "Config", "Human", "data" ]
game_state = 0

pop_size = 200
bots = []
pop = Population(pop_size, 6, 4, False)
nets = pop.get_pop()

pygame.init()

win = pygame.display.set_mode((1000,1000))
data_handler = DataConf(win)

def make_pop():
	for i in range(len(nets)):
		bots.append(Bot(win, numpy.random.randint(1000), numpy.random.randint(1000), 1, nets[i], 4, (255, 0, 0),1))
		nets[i].fitness = 1
	data_handler.draw_net(nets[-1].dna)
	pygame.time.wait(500)

loop = True

def gui(game_state):
	pressed = pygame.mouse.get_pressed()
	if pressed[0]:
		make_pop()
		game_state = 1
		with open('H:\\Documents\\Coding_projects\\battle_bots_evolution\\data\\scores.csv', mode='w', newline='') as csv_file:
			csv_file = csv.writer(csv_file, delimiter=',')
			csv_file.writerow(["total", "members", "fitness"])
	return game_state

def battle(game_state, count):
	global bots
	global nets	
	sum_of = 0
	if count > 1000:		
		for bot in range(len(bots) - 1, -1, -1):
			sum_of += bots[bot].brain.fitness
		print(sum_of)
		'''arr = [""] * pop.max_species_id * 2 + 1
		arr[0] = sum_of

		for s in pop.species:
			arr[s.id * 2 + 1] = len(s.members)
			arr[s.id * 2 + 2] = s.fitness'''
		arr = [sum_of]

		with open('H:\\Documents\\Coding_projects\\battle_bots_evolution\\data\\scores.csv', mode='a', newline='') as csv_file:
			csv_file = csv.writer(csv_file, delimiter=',')
			csv_file.writerow(arr)
		nets = pop.next_gen(nets)
		print("Pop size: ",len(nets))
		bots = []
		make_pop()
		return 0
	for bot in range(len(bots) - 1, -1, -1):
		if not bots[bot].alive:
			continue
		draw = False
		if bot < 10:
			draw = True
		fit = bots[bot].go(False, draw)
		bots[bot].brain.fitness += fit

	return count + 1



def config(game_state):
	pass

def play(game_state):
	bots[0].go(True, True)

def calc_state(state, count):
	if state == 1 and count > 10000:
		count = 0
		return 0
	else:
		return 1


count = 0


while loop:
	
	#game_state = calc_state(game_state, count)

	if game_state == 0:
		game_state = gui(game_state)
	elif game_state == 1:		
		count = battle(game_state, count)
	elif game_state == 2:
		config(game_state)
	elif game_state == 3:
		play(game_state)


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			loop = False

	pygame.display.update()

	win.fill((0))





