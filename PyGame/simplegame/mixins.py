# coding: utf-8
# Created by Jakob Lautrup Nysom @ March 15th 2014
from .transform import Transform, Axis
import pygame

class KeyHandler:
    """A simple class for registering a callback 
    to be called when one or more keys are pressed"""
    def __init__(self, callback, *keys):
        self.cb = callback
        self.keys = keys
        
    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys:
                self.cb()

class Controllable:
    """A thing to subclasss to easily make a controllable object"""
    def __init__(self, rect, speed, up=pygame.K_UP, 
        down=pygame.K_DOWN, left=pygame.K_LEFT, right=pygame.K_RIGHT,
        limit=None, move_cb=None):
        self.transform = Transform(rect, move_cb)
        self.transform.add(right,   Axis.X,   speed)
        self.transform.add(left,    Axis.X, - speed)
        self.transform.add(up,      Axis.Y, - speed)
        self.transform.add(down,    Axis.Y,   speed)
        self.limit = limit
    
    def handle(self, event):
        self.transform.on(event)
    
    def move(self, dx, dy):
        self.transform.move(dx, dy)
    
    def update(self, deltatime):
        self.transform.forward(deltatime, self.limit)