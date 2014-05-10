

from simplegame import Game, Transform, Axis, Animation, Sprite
import pygame
import os






class DestructibleBlock(Sprite):
    def __init__(self, pos, tilefile):
        super().__init__(pos, tilefile)
        

class Scyscraper(Transform):
    def __init__(self, pos, size, tilefile):
        self.tiles = []
        for x in range(size[0]):
            for y in range(size[1]):
                pass

speed = 100
class Kaijuu(Sprite):
    def __init__(self, pos):
        super().__init__(pos, "kaijuu")
        self.still_image = self.image
        self.add_binding(pygame.K_RIGHT, Axis.X, speed)
        self.add_binding(pygame.K_LEFT, Axis.X, -speed)
        self.walking = False
    
    def update(self, deltatime):
        Transform.update(self, deltatime)
        if self.dir.x:
            if not self.walking:
                self.walking = True
                self.image = Animation("kaijuu").play(True)
        else:
            if self.walking:
                self.walking = False
                self.image.stop(self.still_image)
                

def main():
    """
    For at et objekt opdateres: definer 'update(self, deltatime)'
    For at et objekt renderes: definer 'render(self, surf)'
    For at et object modtager events: definer 'handle(self, event)'
    
    For at kalde en metode i superklassen: ex Transform.render(self, surf)
    
    
    """
    size = (800,600)
    game = Game(size, "Kaijuu Game")
    game.add(Kaijuu((0,0)))
    game.run()
    

if __name__ == '__main__':
    main()