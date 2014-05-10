from simplegame import Clear, Sprite, Vector
import pygame
import math


class Rotatable(Sprite):

	@property
	def rotation(self):
		return self._rotation
	
	@rotation.setter
	def rotation(self, val):
		self._rotation = val % 360
		self.image = pygame.transform.rotate(self.source, self._rotation)
		self.image.convert()

	def __init__(self, pos, imagefile, rotation):
		Sprite.__init__(self, pos, imagefile)
		self.source = self.image
		self.image = Clear(self.source.get_size())
		self.rotation = rotation
		
	def render(self, surf):
		offset = Vector(self.image.get_size()) - self.source.get_size()
		pos = round(self.drawpos[0] - offset.x/2), round(self.drawpos[1] - offset.y/2)
		surf.blit(self.image, pos)