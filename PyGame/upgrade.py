# coding: utf-8
# Jabok @ 10th May
from simplegame import Sprite, Loader, Game, Vector, Clear
from rotation import Rotatable
from main import 
import pygame
import math

class Upgrade(Sprite):
    def __init__(self, parent, name, relpos, imagefile, description,
            centered=False):
        self.layer = 2
        pos = parent.pos + relpos
        img = Loader.load_image(imagefile)
        rect = img.get_rect()
        rect.center = pos.tuple
        super().__init__(pos, imagefile, rect=rect, centered=centered)
        self.parent = parent
        parent.add_child(self)
        print("Position:", self.pos)
        self.description = description
        self.name = name

class Laser(Rotatable):
    def __init__(self, start, end, duration=0.1):
        self.layer = 1
        extent = end - start
        middle = start + extent * 0.5
        img = Loader.load_image("laser")
        length = int(math.floor(extent.length))
        source = Clear((length, 8))
        for i in range(length):
            pos = (i*16, 0)
            source.blit(img, pos)
        self.elapsed = 0
        self.duration = duration
        angle = extent.angle()
        if end.y < start.y:
            angle = 180 - angle
        super().__init__(middle.tuple,"laser", 0)
        self.source = source
        self.rotation = -angle
        
    def update(self, deltatime):
        self.elapsed += deltatime
        if self.elapsed >= self.duration:
            Game.active.remove(self)
        
laser_length = 150
class LaserEyes(Upgrade):
    def __init__(self, parent, key=pygame.K_e):
        super().__init__(parent, "Laser Eyes", (35, 24), "lasereye", 
            "Zap!", centered=True)
        self.key = key
        self.keydown = False
    
    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.key:
                self.keydown =True
                
        if event.type == pygame.KEYUP:
            self.keydown = False
    
    def update(self, deltatime):
        if self.keydown:
            start = Vector(self.rect.center)
            direction = Vector(pygame.mouse.get_pos()) - start
            end = start + direction.normalized * laser_length
            Game.active.add(Laser(start, end))
    
    def move(self, vec):
        print("Moving by", vec)
        super().move(vec)

class MissileLauncher(Upgrade):
    def __init__(self, parent, key):
        pass

if __name__=="__main__":
    game = Game((800, 600), "Lasers")
    parent = Sprite((50,50), "lasereye")
    game.add(LaserEyes(parent))
    """game.add(Laser(Vector(0,0), Vector(200,200), 1))
    game.add(Laser(Vector(0,0), Vector(100,200), 2))
    game.add(Laser(Vector(100,200), Vector(150,200), 3))
    game.add(Laser(Vector(150,200), Vector(200,250), 4))"""
    game.run()
        
