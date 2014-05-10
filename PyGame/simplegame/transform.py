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
    def __init__(self, rect, pos=None, move_cb=None, centered=False):
        self.rect = rect
        self.pos = Vector(pos) if pos else Vector(rect.x, rect.y)
        self.dir = Vector(0,0)
        self.bindings = {} #{key:[axis, value, status]}
        self.move_cb = move_cb # Callback when moved :)
        self.children = set()
        self.centered = centered
    
    @property
    def drawpos(self):
        if not self.centered:
            pos = self.pos.tuple
        else:
            pos = (self.pos - Vector(self.rect.size)*0.5).tuple
        return pos
    
    def move(self, vec):
        """Moves the transform by the given vector"""
        if vec == Vector(0,0): return
        self.pos += vec
        x, y = round(self.pos.x), round(self.pos.y)
        if not self.centered:
            self.rect.topleft = x,y
        else:
            self.rect.center = x, y
        
        if self.move_cb:
            self.move_cb()
        for child in self.children:
            child.move(vec)
    
    def add_child(self, child):
        """Adds a child to the transform"""
        self.children.add(child)
    
    def forward(self, factor=1, limit=None):
        """Moves the transform forward based on its velocity"""
        if limit: # Limits the movement to this given velocity
            self.move(self.dir.normalized*limit*factor)
        else:
            self.move(self.dir*factor)
    
    def moveto(self, pos):
        """Moves the transform to a specific position"""
        if pos == self.pos: return
        delta = Vector(pos) - self.pos
        self.pos = Vector(pos)
        self.rect.x = round(self.pos.x)
        self.rect.y = round(self.pos.y)
        if self.move_cb:
            self.move_cb()
        for child in self.children:
            child.move(delta)
        
    
    def add_binding(self, key, axis, value):
        print("Adding binding for {0} on {1}".format(key, axis))
        self.bindings[key] = [axis, value, False]
    
    def clamp(self, rect):
        self.moveto((min(max(self.rect.left, rect.left), 
                rect.right-self.rect.width),
            min(max(self.rect.top, rect.top), 
                rect.bottom-self.rect.height)))
    
    def handle(self, event):
        # Why can this only handle two axises at once :u
        if event.type == pygame.KEYDOWN:
            if event.key in self.bindings:
                axis, value, status = self.bindings[event.key]
                self.bindings[event.key][2] = True
                if axis == Axis.X:
                    self.dir.x += value
                elif axis == Axis.Y:
                    self.dir.y += value
            
        elif event.type == pygame.KEYUP:
            if event.key in self.bindings:
                axis, value, status = self.bindings[event.key]
                if status:
                    if axis == Axis.X:
                        self.dir.x -= value
                    elif axis == Axis.Y:
                        self.dir.y -= value
                self.bindings[event.key][2] = False
    
    def update(self, deltatime):
        self.forward(deltatime)