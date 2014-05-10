
from simplegame import Game, Transform, Axis, Animation
import pygame
import os



class Explosion(Transform):
	def __init__(self, pos):
		super().__init__(pygame.Rect(0,0,0,0), pos=pos)
		self.image = Animation("resources/bAnim").play(True)
	
	def render(self, surf):
		surf.blit(self.image, self.drawpos)


def main():
	size = (800, 600)
	game = Game(size, "Kaijuu Game")
	game.add(Explosion((50,50)))
	game.run()
	
	

	
	
	
if __name__=="__main__":
	main()