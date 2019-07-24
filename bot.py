from bullet import Bullet
import numpy
import pygame
import math

class Bot:
	def __init__(self, win, x, y, id, brain, ins, human, colour, opponent ):
		self.win = win
		self.x = x
		self.y = y
		self.dir = numpy.random.uniform(0,359)
		self.hspeed = 0
		self.vspeed = 0
		self.rspeed = 0
		self.maxspeed = 0.2
		self.maxrspeed = 10
		self.friction = 0.001
		self.id = id
		self.brain = brain
		self.alive = True
		self.thrusting = False
		self.thrust = 0.1
		self.turn_left = 0
		self.turn_right = 0
		self.eyes = ins
		self.human = human
		self.bullets = []
		self.colour = colour
		self.last_shot = 0
		self.win_width, self.win_height = pygame.display.get_surface().get_size()
		self.opponent = opponent


	def go(self):
		if self.human:
			self.get_input()
		else:
			self.think()
		self.update()
		self.draw()



	def get_input(self):
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_LEFT]:
			self.left()
		if pressed[pygame.K_RIGHT]:
			self.right()
		if pressed[pygame.K_UP]:
			self.activate_thrust()
		if pressed[pygame.K_SPACE]:
			self.shoot()


	def think(self):
		outs = self.brain.feed_forward([0,1,2,1,1])
		out_left = outs[0]
		out_right = outs[1]
		out_thrust = outs[2]
		out_shoot = outs[3]

		if out_left > 0:
			self.left()
		if out_right > 0:
			self.right()
		if out_thrust > 0:
			self.activate_thrust()
		if out_shoot  > 0:
			self.shoot()

	def update(self):	
		speed = numpy.sqrt(self.hspeed**2 + self.vspeed**2)
		if self.thrusting:
			if speed < self.maxspeed:
				self.hspeed += self.thrust * math.cos(numpy.deg2rad(self.dir))
				self.vspeed += self.thrust * math.sin(numpy.deg2rad(self.dir))
			else:
				self.hspeed = self.maxspeed * math.cos(numpy.deg2rad(self.dir))
				self.vspeed = self.maxspeed * math.sin(numpy.deg2rad(self.dir))
		elif speed > 0.01:
			self.hspeed *= self.friction
			self.vspeed *= self.friction
		else:
			self.hspeed = 0
			self.vspeed = 0
		self.rspeed =  self.turn_right - self.turn_left
		
		self.x += self.hspeed
		self.y += self.vspeed
		self.dir += self.rspeed
		if self.dir > 360:
			self.dir = 0
		elif self.dir <= 0:
			self.dir = 360


		self.turn_left = 0
		self.turn_right = 0
		self.thrusting = False

		self.update_bullets()


	def draw(self):
		pygame.draw.circle(self.win, self.colour, (int(self.x), int(self.y)), 20)
		for i in range(self.eyes):
			this_dir = self.dir + (360 / self.eyes) * i
			pygame.draw.line(self.win, self.colour, (int(self.x), int(self.y)), (self.x + (int(math.cos(numpy.deg2rad(this_dir)) * 100)), self.y + int((math.sin(numpy.deg2rad(this_dir)) * 100))),2)
		pygame.display.update()

	def activate_thrust(self):
		self.thrusting = True

	def left(self):
		self.turn_left = 0.1

	def right(self):
		self.turn_right = 0.1


	def shoot(self):
		if self.last_shot > 200:
			self.bullets.append(Bullet(self.win, self.x, self.y, math.cos(numpy.deg2rad(self.dir)), math.sin(numpy.deg2rad(self.dir)), self.colour))
			self.last_shot = 0
		else:
			self.last_shot += 1

	def update_bullets(self):
		for bu in range(len(self.bullets) - 1, -1, -1):
			b = self.bullets[bu]
			if b.age > 2000:
				del self.bullets[bu]
			b.update()
			b.draw()

