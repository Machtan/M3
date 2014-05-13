from simplegame import Game, Transform, Axis, Animation, Sprite
from simplegame import Vector, MouseListener
from rotation import Rotatable
import pygame
import os
import math

gravity = Vector(0,0.1)
class Missile(Rotatable):
    def __init__(self, pos, vec):
        super().__init__(pos, "missile", 0)
        self.layer = 1
        self.vec = Vector(vec)
        self.mouseDown = False
        self.speed = 100
        self.drag = 0.9
    
    def update(self, deltatime):
        if self.vec.y < 0:
            angle = self.vec.angle()
        else:
            angle = 360 - self.vec.angle()
        self.rotation = angle
        self.move(self.vec  * deltatime * self.speed)
        self.vec += gravity  * deltatime * 50
        if self.mouseDown:
            rel = Vector(pygame.mouse.get_pos()) - self.pos
            self.vec += rel.normalized * deltatime * 10
        if self.vec.length > 5:
            self.vec = self.vec.normalized * 5
        #self.vec.normalize()
        
    def handle_mouse(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouseDown = True
                
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouseDown = False
            
size = (500,500)
game = Game(size, "Missile Game")      
def start():
    game.add(Missile((250,250),(0,0)))
            
start()
game.run()