from simplegame import Game, Transform, Axis, Loader, Vector, Animation, Sprite
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

		
class SmallExplosion(Transform):
	def __init__(self, pos):
		super().__init__(pygame.Rect(0,0,0,0), pos=pos)
		cb = lambda: Game.active.remove(self)
		self.image = Animation("resources/smallExp", finish_cb=cb).play(True)
	
	def render(self, surf):
		surf.blit(self.image, self.drawpos)

shoot_delay = 3
class Tank(Sprite):
	def __init__(self, pos):
		super().__init__(pos, "tank")
		self.elapsed = 0
		
	def update(self, deltatime):
		self.elapsed += deltatime
		if self.elapsed >= shoot_delay:
			mis = Missile(self.pos,(-5.8,-4.8))
			game.add(mis)
			self.elapsed -= shoot_delay
		
shoot_delay = 2
class Helicopter(Sprite):
	def __init__(self, pos):
		super().__init__(pos, "helekopter")
		cb = lambda: Game.active.remove(self)
		self.image = Animation("resources/helekopter", finish_cb=cb).play(True)
		self.elapsed = 0
		
	def render(self, surf):
		surf.blit(self.image, self.drawpos)
		
	def update(self, deltatime):
		self.elapsed += deltatime
		if self.elapsed >= shoot_delay:
			mis = Missile(self.pos,(-5.8,-4.8))
			game.add(mis)
			self.elapsed -= shoot_delay

		
def main():
	size = (800, 600)
	game = Game(size, "Kaijuu Game")
	game.add(SmallExplosion((100,100)))
	mis = Missile((110,210),(5.8,-4.8))
	game.add(mis)
	mis = Missile((100,200),(6,-5))
	game.add(mis)
	mis = Missile((90,190),(6.2,-5.2))
	game.add(mis)
	mis = Helicopter((500,100))
	game.add(mis)
	game.add(Tank((500,500)))
	game.run()
	
if __name__=="__main__":
	main()