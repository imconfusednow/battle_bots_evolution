import numpy
import pygame
import csv
from bot import Bot
import sys
import os
import threading
import time

sys.path.insert(0, 'H:\\Documents\\Coding_projects')
sys.path.insert(1, 'H:\\Documents\\Coding_projects\\neat')
from neat import DataConf
from neat import Network
from neat import Population

states = ["Menu", "Train", "Config", "Human", "data", "show"]
labels = ["Total", "Best", "Theoretical", "Species", "Recurrents", "Complexity", "Time"]

game_state = 0

win_width = 1500
win_height = 1000
pop_size = 150
run_time = 1500
chosen = False

pygame.init()
win = pygame.display.set_mode((win_width,win_height))
data_handler = DataConf(win)

pop = Population(pop_size, 5, 3, True)
nets = pop.get_pop()
bots = []


def make_pop():
    print("Creating population of " + str(len(nets)))
    complexity = 0
    for i in range(len(nets)):
        bots.append(Bot(win, numpy.random.randint(win_width),
                        numpy.random.randint(win_height), 1, nets[i], 4, (255, 0, 0), 1))
        nets[i].fitness = 1
        complexity += nets[i].max_node

    return complexity


loop = True


def gui(game_state, events):
    for event in events:
      if event.type == pygame.KEYDOWN:
        try:
            key = int(pygame.key.name(event.key))
            states[key]
            game_state = key
        except:
            pass

    if game_state == 1:
        make_pop()
        '''dna = {'neurons': [[0, 1, 2, 3, 4], [5, 6, 7]], 'connections': [[0, 5, 1, True], [0, 6, 0.0, True], [0, 7, -1, True], [1, 5, 1, True], [1, 6, -0.8, True], [1, 7, 0.0, True], [2, 5, -0.0, True], [2, 6, 0.0, True], [2, 7, 0.1, True], [3, 5, -0.8, True], [3, 6, 1, True], [3, 7, 0.0, True], [4, 5, -0.0, True], [4, 6, 0.0, True], [4, 7, 0.1, True]], 'recurrents': []}
        nets.append(Network(5, 3, True, 0, dna, False, False, 0, (255, 255, 0)))
        bots[0] = (Bot(win, numpy.random.randint(win_width), numpy.random.randint(win_height), 1, nets[-1], 4, (255, 255, 0), 1))'''
        
        data_handler.clear_saves()
        data_handler.create_data_file(labels)
        #f = open("H:\\Documents\\Coding_projects\\battle_bots_evolution\\data\\debug.txt", "w")
        #f.close()
    return game_state


theoretical_adj = 0
t1 = 0

def battle(game_state, count):
    global bots
    global nets
    global theoretical_adj
    global t1
    sum_of = 0
    best = 0
    recurrents = 0

    if count > run_time:
        for bot in range(len(bots) - 1, -1, -1):
            sum_of += bots[bot].brain.fitness
            recurrents += len(bots[bot].brain.dna["recurrents"])
            if bots[bot].brain.fitness > best:
                best = bots[bot].brain.fitness

        data_handler.save(nets)
        arr = [sum_of, best, theoretical_adj, len(pop.species), recurrents, time.perf_counter() - t1]
        print("Time: ", time.perf_counter() - t1)
        t1 = time.perf_counter()
        theoretical = 0
        theoretical_adj = 0
        nets = pop.next_gen(nets)
        data_handler.set_chosen(pop.chosen)
        print("Pop size: ", len(nets))
        bots = []
        arr.append(make_pop())
        data_handler.save_data(arr)
        data_handler.change_gen(pop.generation, False)
        return 0
    for bot in range(len(bots) - 1, -1, -1):
        if not bots[bot].alive:
            bots[bot].brain.fitness = 0
            continue
        draw = False
        #if bot < 100 and count % 3 == 0:
        #    draw = True
        fit = bots[bot].go(False, draw)
        bots[bot].brain.fitness += fit
        theoretical_adj += 10
    return count + 1


def config(game_state):
    pass


def data(game_state):
    if game_state == 4:
        data_handler.draw_brain(nets)
    elif game_state == 6:
        data_handler.show_graph()



def play(game_state):
    if len(bots) == 0:
        net = Network(3, 6, True, 0, {"neurons": [[], []], "connections": [], "recurrents": []}, True, False, 0)
        bots.append(Bot(win, numpy.random.randint(win_width),
                        numpy.random.randint(win_height), 1, net, 4, (255, 0, 0), 1))
    bots[0].go(True, True)
    
info = dict()
colours = dict()
def replay(game_state, count, events):
    global nets
    global bots
    global chosen
    global info

    data_handler.text("Generation: " + str(data_handler.gen), 10, 10, (255,255,255))
    if len(bots) == 0 or count > run_time:
        count = 0
        info = data_handler.load()
        dnas = info["dna"]
        nets = []
        bots = []
        for c, i in enumerate(dnas):
            species = info["species"][c]
            if species not in colours:
                colours[species] = [numpy.random.randint(255), numpy.random.randint(255), numpy.random.randint(255)]
            colour = (255, 0, 0)
            if chosen and str(info["id"][c]) in info["chosen"]:
                colour = (255,255,0)
            elif not chosen:
                colour = colours[species]
            nets.append(Network(5, 3, True, info["id"][c], i, False, False, species, colour))
            bots.append(Bot(win, info["loc"][c][0],info["loc"][c][1], 1, nets[-1], 4, colour, 1))
            bots[-1].dir = info["loc"][c][2]

    run_go(info["species"])


    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if data_handler.change_gen(1, True):
                    count = run_time
                events.clear()
            if event.key == pygame.K_LEFT:
                if data_handler.change_gen(-1, True):
                    count = run_time
                events.clear()
            if event.key == pygame.K_LSHIFT:
                count = run_time
                new_gen = get_string()
                if new_gen == "":
                    new_gen = data_handler.tot_saves
                data_handler.change_gen(int(new_gen), False)
                events.clear()
            if event.key == pygame.K_LCTRL:
                chosen = not chosen

        if event.type == pygame.QUIT:
            print("Quitting")
            exit()

    return count + 1

def run_go(display_value):
    for i in range(len(bots) -1,-1, -1):
        if not bots[i].alive:
            continue
        fit = bots[i].go(False, True)
        bots[i].brain.fitness += fit

def get_string():
    string = ""
    loop = True

    while loop:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.unicode.isnumeric():
                    string += event.unicode
                if event.key == pygame.K_RETURN:
                    loop = False
            if event.type == pygame.QUIT:
                exit()
    return string


def calc_state(state, count):
    if state == 1 and count > 10000:
        count = 0
        return 0
    else:
        return 1


count = 0
last_state = 0
result1 = 0
events = []

def do_stuff():
    global game_state
    global count
    global last_state
    global events

    events += pygame.event.get()

    if game_state == 0:
        game_state = gui(game_state, events)
    elif game_state == 1:
        count = battle(game_state, count)
    elif game_state == 2:
        config(game_state)
    elif game_state == 3:
        play(game_state)
    elif game_state == 4 or game_state == 6:
        data(game_state)
        game_state = last_state
    elif game_state == 5:
        count = replay(game_state, count, events)

    if count % 4 == 0:
        pygame.display.update()
        win.fill((0))
        for event in events:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    last_state = game_state if not game_state == 4 else last_state
                    game_state = 4
                elif event.key == pygame.K_RETURN:
                    last_state = game_state if not game_state == 6 else last_state
                    game_state = 6
        events = []


    return True

if __name__ == '__main__':
    while loop:
        loop = do_stuff()
