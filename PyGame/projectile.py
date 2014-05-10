from simplegame import Game, Transform, Axis, Loader, Vector
from rotation import Rotatable
import pygame
import os
import math

degconv = 180/math.pi
gravity = Vector(0,0.1)

class Missile(Rotatable):
	def __init__(self, pos, vec):
		super().__init__(pos, "missile", 0)
		self.vec = Vector(vec)
	
	def update(self, deltatime):
		if self.vec.y < 0:
			angle = math.acos(self.vec.x/math.sqrt(self.vec.x**2 + self.vec.y**2)) * degconv
		else:
			angle = 360 - math.acos(self.vec.x/math.sqrt(self.vec.x**2 + self.vec.y**2)) * degconv
		self.rotation = angle
		self.pos += self.vec
		self.vec += gravity

def main():
	size = (800, 600)
	game = Game(size, "Kaijuu Game")
	mis = Missile((100,200),(4.5,-4.8))
	game.add(mis)
	mis = Missile((100,200),(5.5,-5.2))
	game.add(mis)
	mis = Missile((100,200),(5,-5))
	game.add(mis)
	game.run()
	
if __name__=="__main__":
	main()