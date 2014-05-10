# coding: utf-8
# Created by Jakob Lautrup Nysom @ March 15th 2014
import pygame

class Clear(pygame.Surface):
    """A converted clearable surface"""
    def __init__(self, size, colorkey=(10,10,10)):
        super().__init__(size)
        if pygame.display.get_init():
            self.convert()
        self.fill(colorkey)
        self.set_colorkey(colorkey)
        self.colorkey = colorkey
        
    def clear(self):
        self.set_colorkey((9,9,9))
        self.fill(self.colorkey)
        self.set_colorkey(self.colorkey)