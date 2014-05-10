# coding: utf-8
# Created by Jabok @ May 10th 2014
# Sprite is a simple sprite class
from .transform import Transform
from .loader import Loader
import pygame
class Sprite(Transform):
    def __init__(self, pos, imagefile, rect=None, centered=False):
        if imagefile:
            self.image = Loader.load_image(imagefile)
        else:
            self.image = pygame.Surface((0,0))
        if rect: 
            self.rect = rect 
        else:
            self.rect = pygame.Rect(pos, self.image.get_size())
            if centered:
                self.rect.center = pos
        Transform.__init__(self, self.rect, pos=pos, centered=centered)
    
    def render(self, surf):
        surf.blit(self.image, self.drawpos)