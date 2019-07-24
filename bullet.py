import pygame

class Bullet:
	def __init__(self, win, x, y, hspeed, vspeed, colour):
		self.win = win
		self.x = x
		self.y = y
		self.hspeed = hspeed * 0.5
		self.vspeed = vspeed * 0.5
		self.colour = colour
		self.age = 0


	def update(self):
		self.x += self.hspeed
		self.y += self.vspeed
		self.age += 1


	def draw(self):
		pygame.draw.circle(self.win, self.colour, (int(self.x), int(self.y)), 5)