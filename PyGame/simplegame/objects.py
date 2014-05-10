# coding: utf-8
# Created by Jakob Lautrup Nysom @ March 15th 2014
import pygame
class Block:
    """A simple block for testing stuff"""
    def __init__(self, pos, size, color):
        if type(size) in {int, float}:
            size = (size, size)
        self.rect = pygame.Rect(pos,size)
        self.image = pygame.Surface(size)
        self.image.convert()
        self.color = color
        self.image.set_colorkey((10,10,10))
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value if value else (10,10,10)
        self.redraw()
    
    def redraw(self):
        self.image.fill(self.color)
        rec = self.image.get_rect()
        nw = rec.topleft
        ne = (rec.right-1, rec.top)
        sw = (rec.left, rec.bottom-1)
        se = (rec.right-1, rec.bottom-1)
        pygame.draw.line(self.image, (50,50,50), se, sw, 3)
        pygame.draw.line(self.image, (50,50,50), se, ne, 3)
        pygame.draw.line(self.image, (150,150,150), nw, ne, 3)
        pygame.draw.line(self.image, (150,150,150), nw, sw, 3)
        
    def render(self, surface):
        surface.blit(self.image, self.rect)
    def __str__(self):
        return "Block({0}, {1})".format(self.rect.topleft, self.rect.size)