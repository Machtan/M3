# coding: utf-8
# Created by Jakob Lautrup Nysom 23 mar 2014
import pygame
import math
from .vector import Vector
class Label():
    
    def __init__(self, text, pos, color=(0,0,0), font="UnDotum", 
            size=24, hovercolor=(255,150,200), center=False, shadow_color=None):
        super().__init__()
        if not pygame.font.get_init(): pygame.font.init()
        # This order is crucial due to the setters.... I apologize
        self.pos        = pos
        self.drawpos    = pos
        self.center     = center
        self.fonttype   = font
        self.size       = size
        self.color      = color
        self.text       = text
        self.maincolor  = color
        self.hovercolor = hovercolor
        self.dirty      = True
        self.dirtyfont  = True
        self.shadow_color = shadow_color
    
    def redraw(self):
        self.dirty = False
        if self.dirtyfont: # Handle font changes
            self.font = pygame.font.Font(pygame.font.match_font(self.fonttype), self.size)
            self.dirtyfont = False
            
        lines = self.text.split("\n")
        self.subparts = []
        images = []
        width = 0
        height = 0
        for line in lines:
            if self.shadow_color:
                shadow = self.font.render(line, True, self.shadow_color)
                pos = Vector(0, height+2)
                self.subparts.append((shadow, pos))
            image = self.font.render(line, True, self.color)
            pos = Vector(0, height)
            self.subparts.append((image, pos))
            width = max(image.get_width(), width)
            height += image.get_height()
        
        self.rect = pygame.Rect(self.pos, (width, height))
        if self.center:
            x = self.pos[0] - math.floor(self.rect.width/2)
            y = self.pos[1] - math.floor(self.rect.height/2)
            self.drawpos = x,y  
    
    def __setattr__(self, mem, value):
        super().__setattr__(mem, value)
        if mem in {"size", "fonttype", "color", "text"}: 
            self.dirty = True
            if mem in {"fonttype", "size"}:
                self.dirtyfont = True
    
    def render(self, surface):
        if self.dirty: # Handle content/font changes
            self.redraw()
            
        for image, pos in self.subparts:
            p = (pos + self.drawpos).tuple
            surface.blit(image, p)