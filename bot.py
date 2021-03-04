from bullet import Bullet
import numpy
import pygame
import math


class Bot:
    def __init__(self, win, x, y, id, brain, ins, colour, opponent):
        self.win = win
        self.x = x
        self.y = y
        self.dir = numpy.random.uniform(0, 359)
        self.hspeed = 0
        self.vspeed = 0
        self.rspeed = 0
        self.maxspeed = 4
        self.maxrspeed = 0.1
        self.friction = 0.98
        self.id = id
        self.brain = brain
        self.brain.start_loc = (x,y,self.dir)
        self.alive = True
        self.thrust = 0.0
        self.turn_left = 0
        self.turn_right = 0
        self.eyes = ins
        self.eye_pos = []
        self.bullets = []
        self.colour = colour
        self.last_shot = 0
        self.win_width, self.win_height = pygame.display.get_surface().get_size()
        self.opponent = opponent
        self.boundaries = [[0, 0, self.win_width, 0], [self.win_width, 0, self.win_width, self.win_height], [
            0, self.win_height, self.win_width, self.win_height], [0, 0, 0, self.win_height]]
        self.inputs = [0, 0, 0, 0, 1]
        self.font = pygame.font.SysFont("comicsansms", 12)
        self.total_rot = 0
        self.see_something = False


    def go(self, human, draw, display_value=""):
        if human:
            self.get_input()
        else:
            self.think()
        to_return = self.update()
        if draw:
            self.draw(display_value)
        return to_return

    def get_input(self):
        pressed = pygame.key.get_pressed()
        left = 0
        right = 0
        if pressed[pygame.K_LEFT]:
            self.left(1)
            right = 1
        if pressed[pygame.K_RIGHT]:
            self.right(1)
            left = 1
        if pressed[pygame.K_UP]:
            self.activate_thrust(1)
        if pressed[pygame.K_SPACE]:
            self.shoot()
        self.look()

    def think(self):
        self.look()
        outs = self.brain.feed_forward(self.inputs)
        out_left = outs[0]
        out_right = outs[1]
        out_thrust = outs[2]
        # out_shoot = outs[3]
        if out_left > 0:
            self.left(outs[0])
        if out_right > 0:
            self.right(outs[1])
        if out_thrust > 0:
            self.activate_thrust(out_thrust)
        # if out_thrust > 0:
        # self.activate_thrust(outs[2])
        # if out_shoot  > 0:
        # self.shoot()

    def update(self):
        speed = numpy.sqrt(self.hspeed**2 + self.vspeed**2)
        if speed > 0.001:
            self.hspeed *= self.friction
            self.vspeed *= self.friction
        else:
            self.hspeed = 0
            self.vspeed = 0
        if self.thrust > 0:
            if speed < self.maxspeed:
                self.hspeed += self.thrust * math.cos(numpy.deg2rad(self.dir))
                self.vspeed += self.thrust * math.sin(numpy.deg2rad(self.dir))
            #else:
            #    self.hspeed = self.maxspeed * math.cos(numpy.deg2rad(self.dir))
            #    self.vspeed = self.maxspeed * math.sin(numpy.deg2rad(self.dir))

        self.rspeed = self.turn_right - self.turn_left
        #if self.rspeed > self.maxrspeed: self.rspeed = self.maxrspeed

        self.x += self.hspeed
        self.y += self.vspeed
        self.dir += self.rspeed
        if self.dir > 360:
            self.dir = 0
        elif self.dir <= 0:
            self.dir = 360

        self.turn_left = 0
        self.turn_right = 0
        self.thrust = 0

        if self.x < 0 or self.x > self.win_width or self.y < 0 or self.y > self.win_height:
            self.alive = False

        '''self.update_bullets()

        if abs(self.rspeed) > 0.1:
            speed /= 2'''
        #self.total_rot += self.rspeed

        if not self.see_something and abs(self.rspeed) > 0.3:
            return 0

        return max(0, speed )

    def draw(self, display_value):
        display_value = display_value if display_value != "" else self.brain.id
        for e in range(len(self.eye_pos)):
            colour = (0, 255, 0)
            i = self.eye_pos[e]
            if self.inputs[e] > 0:
                colour = (255, 0, 0)
            pygame.draw.line(self.win, colour, (int(self.x),
                                                int(self.y)), (i[0], i[1]), 2)
        colour = self.brain.colour if self.brain != 0 else (
            0, 0, 255)
        pygame.draw.circle(self.win, colour, (int(self.x), int(self.y)), 20)
        self.text(str(display_value), self.x - 10, self.y - 10)
        for bu in range(len(self.bullets) - 1, -1, -1):
            b = self.bullets[bu]
            b.draw()

    def text(self, text, x, y):
        text = self.font.render(text, True, (0, 0, 0))
        self.win.blit(text, (x, y))

    def activate_thrust(self, power):
        self.thrust = power * 0.1

    def left(self, power):
        self.turn_left = power * 3

    def right(self, power):
        self.turn_right = power * 3

    def shoot(self):
        if self.last_shot > 200:
            self.bullets.append(Bullet(self.win, self.x, self.y, math.cos(
                numpy.deg2rad(self.dir)), math.sin(numpy.deg2rad(self.dir)), (255, 255, 0)))
            self.last_shot = 0
        else:
            self.last_shot += 1

    def update_bullets(self):
        for bu in range(len(self.bullets) - 1, -1, -1):
            b = self.bullets[bu]
            if b.age > 2000:
                del self.bullets[bu]
            b.update()

    def look(self):
        self.eye_pos = []
        self.see_something = False
        for i in range(self.eyes):
            this_dir = self.dir + (360 / self.eyes) * i
            end = [self.x + int(math.cos(numpy.deg2rad(this_dir)) * 100),
                   self.y + int(math.sin(numpy.deg2rad(this_dir)) * 100)]
            self.eye_pos.append(end)

        if self.x > 100 and self.x < self.win_width - 100 and self.y > 100 and self.y < self.win_height - 100:
            self.inputs = [0 for i in self.inputs]
            self.inputs[-1] = 1

        for j in range(len(self.eye_pos)):
            for i in range(len(self.boundaries)):
                d = self.cast(self.boundaries[i], self.eye_pos[j])
                if (d < 100):
                    break
            self.eye_pos[j][0] = (self.eye_pos[j][0] - self.x) / 100
            self.eye_pos[j][1] = (self.eye_pos[j][1] - self.y) / 100
            self.eye_pos[j][0] = self.eye_pos[j][0] * d + self.x
            self.eye_pos[j][1] = self.eye_pos[j][1] * d + self.y
            self.inputs[j] = 1 - (d / 100)

    def cast(self, wall, eye):
        x1 = wall[0]
        y1 = wall[1]
        x2 = wall[2]
        y2 = wall[3]

        x3 = self.x
        y3 = self.y
        x4 = eye[0]
        y4 = eye[1]

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if (den == 0):
            return 100

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        if (t > 0 and t < 1 and u > 0):
            pt = []
            pt.append(x1 + t * (x2 - x1))
            pt.append(y1 + t * (y2 - y1))
            dist = numpy.sqrt((self.x - pt[0])**2 + (self.y - pt[1])**2)
            if (dist > 100):
                return 100
            else:
                self.see_something = True
                return dist
        else:
            return 100
