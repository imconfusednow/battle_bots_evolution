import numpy
import pygame
import csv
from bot import Bot
import sys
sys.path.insert(0, 'H:\\Documents\\Coding_projects')
sys.path.insert(1, 'H:\\Documents\\Coding_projects\\neat')
from neat import DataConf
from neat import Network
from neat import Population

states = ["Menu", "Train", "Config", "Human", "data", "show"]
game_state = 0

pop_size = 400
bots = []
pop = Population(pop_size, 5, 3, True)
nets = pop.get_pop()

pygame.init()

win_width = 1000
win_height = 1000

win = pygame.display.set_mode((win_width, win_height))
data_handler = DataConf(win)


def make_pop():
    print("Creating population of " + str(len(nets)))
    complexity = 0
    for i in range(len(nets)):
        bots.append(Bot(win, numpy.random.randint(win_width),
                        numpy.random.randint(win_height), 1, nets[i], 4, (255, 0, 0), 1))
        nets[i].fitness = 1
        complexity += nets[i].max_node

    print("Complexity: ", complexity)


loop = True


def gui(game_state):
    pressed = pygame.mouse.get_pressed()
    if pressed[0]:
        make_pop()
        '''dna = {'neurons': [[0, 1, 2, 3, 4], [5, 6, 7]], 'connections': [[0, 5, 1, True], [0, 6, 0.0, True], [0, 7, -1, True], [1, 5, 1, True], [1, 6, -0.8, True], [1, 7, 0.0, True], [2, 5, -0.0, True], [2, 6, 0.0, True], [2, 7, 0.1, True], [3, 5, -0.8, True], [3, 6, 1, True], [3, 7, 0.0, True], [4, 5, -0.0, True], [4, 6, 0.0, True], [4, 7, 0.1, True]], 'recurrents': []}
        nets.append(Network(5, 3, True, 0, dna, False, False, 0, (255, 255, 0)))
        bots[0] = (Bot(win, numpy.random.randint(win_width), numpy.random.randint(win_height), 1, nets[-1], 4, (255, 255, 0), 1))'''
        game_state = 1
        with open('H:\\Documents\\Coding_projects\\battle_bots_evolution\\data\\scores.csv', mode='w', newline='') as csv_file:
            csv_file = csv.writer(csv_file, delimiter=',')
            csv_file.writerow(["total", "Best", "Theoretical"])
    return game_state


theoretical = 0
theoretical_adj = 0


def battle(game_state, count):
    global bots
    global nets
    global theoretical
    global theoretical_adj
    sum_of = 0
    best = 0

    if count > 1500:

        for bot in range(len(bots) - 1, -1, -1):
            sum_of += bots[bot].brain.fitness
            if bots[bot].brain.fitness > best:
                best = bots[bot].brain.fitness
        print(sum_of)
        '''arr = [""] * pop.max_species_id * 2 + 1
        arr[0] = sum_of

        for s in pop.species:
            arr[s.id * 2 + 1] = len(s.members)
            arr[s.id * 2 + 2] = s.fitness'''
        arr = [sum_of, best, theoretical, theoretical_adj]
        theoretical = 0
        theoretical_adj = 0

        with open('H:\\Documents\\Coding_projects\\battle_bots_evolution\\data\\scores.csv', mode='a', newline='') as csv_file:
            csv_file = csv.writer(csv_file, delimiter=',')
            csv_file.writerow(arr)
        nets = pop.next_gen(nets)
        print("Pop size: ", len(nets))
        bots = []
        make_pop()
        return 0
    for bot in range(len(bots) - 1, -1, -1):
        theoretical += 10
        if not bots[bot].alive:
            bots[bot].brain.fitness = 0
            continue
        draw = False
        if bot < 100 and count % 3 == 0:
            draw = True
        fit = bots[bot].go(False, draw)
        bots[bot].brain.fitness += fit
        theoretical_adj += 10

    return count + 1


def config(game_state):
    pass


def data(game_state):
    data_handler.draw_brain(nets)


def play(game_state):
    if len(bots) == 0:
        net = Network(3, 6, True, 0, {"neurons": [[], []], "connections": [], "recurrents": []}, True, False, 0)
        bots.append(Bot(win, numpy.random.randint(win_width),
                        numpy.random.randint(win_height), 1, net, 4, (255, 0, 0), 1))
    bots[0].go(True, True)


def show_one(game_state):
    global nets
    if len(bots) == 0:
        dna = {'neurons': [[0, 1, 2, 3, 4], [5, 6, 7]], 'connections': [[0, 5, 1, True], [0, 6, 0.0, True], [0, 7, -1, True], [1, 5, 1, True], [1, 6, -0.8, True], [1, 7, 0.0, True], [2, 5, -0.0, True], [2, 6, 0.0, True], [2, 7, 0.1, True], [3, 5, -0.8, True], [3, 6, 1, True], [3, 7, 0.0, True], [4, 5, -0.0, True], [4, 6, 0.0, True], [4, 7, 0.1, True]], 'recurrents': []}
        nets = [Network(5, 3, True, 0, dna, False, False, 0)]
        bots.append(Bot(win, numpy.random.randint(win_width),
                    numpy.random.randint(win_height), 1, nets[0], 4, (255, 0, 0), 1))
    for bot in range(len(bots) - 1, -1, -1):
        if not bots[bot].alive:
            continue
        fit = bots[bot].go(False, True)
        bots[bot].brain.fitness += fit

    print(bots[0].brain.fitness)


def calc_state(state, count):
    if state == 1 and count > 10000:
        count = 0
        return 0
    else:
        return 1


count = 0
last_state = 0

def do_stuff():
    global game_state
    global count
    global last_state

    if game_state == 0:
        game_state = gui(game_state)
    elif game_state == 1:
        count = battle(game_state, count)
    elif game_state == 2:
        config(game_state)
    elif game_state == 3:
        play(game_state)
    elif game_state == 4:
        data(game_state)
        game_state = last_state
    elif game_state == 5:
        show_one(game_state)

    if count % 4 == 0:
        pygame.display.update()
        win.fill((0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    last_state = game_state
                    game_state = 4

    return True


while loop:
    loop = do_stuff()
