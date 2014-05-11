from simplegame import Game, Transform, Axis, Loader, Vector, Animation, Sprite
from rotation import Rotatable
import pygame
import os
import math

degconv = 180/math.pi
gravity = Vector(0,0.1)

def debug():
    print("Animations:", len(Animation.active))
    print("Objects:   ", Game.active.sprites.size())
        
def main():
    size = (800, 600)
    game = Game(size, "Kaijuu Game")
    mis = Helicopter((700,100))
    game.add(mis)
    game.add(Tank((700,500)))
    game.run()
    
if __name__=="__main__":
    main()