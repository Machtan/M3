from simplegame import Clear, Sprite, Vector
import pygame
import math


class Rotatable(Sprite):   
    """A class for rotatable sprites"""
    @property
    def rotation(self):
        return self._rotation
        
    @rotation.setter
    def rotation(self, val):
        self._rotation = val % 360
        self.image = pygame.transform.rotate(self.source, self._rotation)
        self.rect.size = self.image.get_size()
        self.image.convert()
        
    def __init__(self, pos, imagefile, rotation, centered=True):
        Sprite.__init__(self, pos, imagefile, centered=centered)
        self.source = self.image
        self.image = Clear(self.source.get_size())
        self.rotation = rotation
        
    def render(self, surf):
        surf.blit(self.image, self.drawpos)