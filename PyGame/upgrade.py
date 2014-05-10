# coding: utf-8
# Jabok @ 10th May
from simplegame import Sprite, Loader, Game, Vector, Clear
from rotation import Rotatable
#from main import destroy
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
        
