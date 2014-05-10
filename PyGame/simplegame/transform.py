# coding: utf-8
# Created by Jakob Lautrup Nysom @ March 15th 2014
from .vector import Vector
import pygame

class Axis:
    """An axis enum"""
    X = "x"
    Y = "y" 

class Transform:
    """Represents an object's position and movement"""
    def __init__(self, rect, pos=None, move_cb=None):
        self.rect = rect
        self.pos = Vector(pos) if pos else Vector(rect.x, rect.y)
        self.dir = Vector(0,0)
        self.bindings = {} #{key:(axis, value)}
        self.move_cb = move_cb # Callback when moved :)
    
    @property
    def drawpos(self):
        return self.pos.tuple
    
    def move(self, vec):
        """Moves the transform by the given vector"""
        if vec == Vector(0,0): return
        self.pos += vec
        self.rect.x = round(self.pos.x)
        self.rect.y = round(self.pos.y)
        if self.move_cb:
            self.move_cb()
    
    def forward(self, factor=1, limit=None):
        """Moves the transform forward based on its velocity"""
        if limit: # Limits the movement to this given velocity
            self.move(self.dir.normalized*limit*factor)
        else:
            self.move(self.dir*factor)
    
    def moveto(self, pos):
        """Moves the transform to a specific position"""
        if pos == self.pos: return
        self.pos = Vector(pos)
        self.rect.x = round(self.pos.x)
        self.rect.y = round(self.pos.y)
        if self.move_cb:
            self.move_cb()
    
    def add(self, key, axis, value):
        print("Adding binding for {0} on {1}".format(key, axis))
        self.bindings[key] = (axis, value)
    
    def clamp(self, rect):
        self.moveto((min(max(self.rect.left, rect.left), 
                rect.right-self.rect.width),
            min(max(self.rect.top, rect.top), 
                rect.bottom-self.rect.height)))
    
    def handle(self, event):
        # Why can this only handle two axises at once :u
        if event.type == pygame.KEYDOWN:
            if event.key in self.bindings:
                axis, value = self.bindings[event.key]
                if axis == Axis.X:
                    self.dir.x += value
                elif axis == Axis.Y:
                    self.dir.y += value
            
        elif event.type == pygame.KEYUP:
            if event.key in self.bindings:
                axis, value = self.bindings[event.key]
                if axis == Axis.X:
                    self.dir.x -= value
                elif axis == Axis.Y:
                    self.dir.y -= value  
    
    def update(self, deltatime):
        if self.dir.x + self.dir.y:
            self.move(self.dir*deltatime)