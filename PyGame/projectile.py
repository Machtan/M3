from simplegame import Game, Transform, Axis, Loader, Vector, Animation, Sprite
from rotation import Rotatable
import pygame
import os
import math

degconv = 180/math.pi
gravity = Vector(0,0.1)

def debug():
	print("Animations:", len(Animation.active))
	print("Objects:   ", Game.active.sprites.size())

class Missile(Rotatable):
	def __init__(self, pos, vec):
		super().__init__(pos, "missile", 0)
		self.layer = 1
		self.vec = Vector(vec)
	
	def update(self, deltatime):
		if self.vec.y < 0:
			angle = math.acos(self.vec.x/math.sqrt(self.vec.x**2 + self.vec.y**2)) * degconv
		else:
			angle = 360 - math.acos(self.vec.x/math.sqrt(self.vec.x**2 + self.vec.y**2)) * degconv
		self.rotation = angle
		self.pos += self.vec
		self.vec += gravity
		if self.pos.y > 550:
			self.explode()
			
	def damage(self, amount, pos):
		self.explode()
		
	def explode(self):
		mis = SmallExplosion(self.pos - (32,32))
		Game.active.add(mis)
		self.destroy()

		
class SmallExplosion(Transform):
	def __init__(self, pos):
		super().__init__(pygame.Rect(0,0,0,0), pos=pos, centered=True)
		self.layer = -1
		cb = lambda: Game.active.remove(self)
		self.image = Animation("resources/smallExp", finish_cb=cb).play()
	
	def render(self, surf):
		surf.blit(self.image, self.drawpos)

class Tank(Sprite):
	def __init__(self, pos):
		super().__init__(pos, "tank")
		self.elapsed = 2
		self.shoot_delay = 2.5
		
	def update(self, deltatime):
		self.elapsed += deltatime
		if self.elapsed >= self.shoot_delay:
			mis = Missile(self.pos + (10,15),(-5.8,-3.8))
			Game.active.add(mis)
			self.elapsed -= self.shoot_delay
			
	def damage(self, amount, pos):
		mis = SmallExplosion(self.pos + (0,10))
		Game.active.add(mis)
		self.destroy()
		
class Helicopter(Sprite):
	def __init__(self, pos):
		super().__init__(pos, "helekopter")
		self.image = Animation("resources/helekopter").play(True)
		self.elapsed = 1.5
		self.shoot_delay = 2
		self.vec = Vector(0,0.5)
		
	def render(self, surf):
		surf.blit(self.image, self.drawpos)
		
	def update(self, deltatime):
		self.pos += self.vec
	
		self.elapsed += deltatime
		if self.elapsed >= self.shoot_delay:
			if self.pos.x < 300 or self.pos.y < 250:
				mis = Missile(self.pos + (0,32),(-8,1))
			else:
				mis = Missile(self.pos + (0,32),(-8,-1))
			Game.active.add(mis)
			self.elapsed -= self.shoot_delay
			self.vec = Vector(self.vec.x, -self.vec.y) 
	
	def damage(self, amount, pos):
		mis = SmallExplosion(self.pos)
		Game.active.add(mis)
		self.destroy()
		
def main():
	size = (800, 600)
	game = Game(size, "Kaijuu Game")
	mis = Helicopter((700,100))
	game.add(mis)
	game.add(Tank((700,500)))
	game.run()
	
if __name__=="__main__":
	main()