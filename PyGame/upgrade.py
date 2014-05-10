# coding: utf-8
# Jabok @ 10th May
from simplegame import Sprite, Loader, Game
import pygame
class Upgrade(Sprite):
    def __init__(self, parent, name, relpos, imagefile, description):
        pos = parent.pos + relpos
        img = Loader.load_image(imagefile)
        rect = img.get_rect()
        rect.center = pos.tuple // Center
        super().__init__(pos, imagefile, rect=rect)
        self.parent = parent
        self.description = description
        self.name = name

class Laser(Rotatable):
    def __init__(self, start, extent, duration=0.1):
        img = Loader.load_image("laser")
        self.source = pygame.Surface((extent.length, 8))
        self.elapsed = 0
        self.duration = duration
        print("Active game:", Game.active)
        
    def update(self, deltatime):
        self.elapsed += deltatime
        if self.elapsed >= self.duration:
            Game.active.remove(self)
        
laser_length = 150
class LaserEyes(Upgrade):
    def __init__(self, parent, key=pygame.K_E):
        super().__init__(parent, "Laser Eyes", (35, 24), "lasereye", 
            "Zap!")
        self.key = key
    
    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.key:
                start = Vector(self.rect.center)
                direction = Vector(pygame.mouse.get_pos()) - start
                extent = direction.normalized() * laser_length
                Laser(start, extent)

class MissileLauncher(Upgrade):
    def __init__(self, parent, key)

if __name__=="__main__":
    Laser(Vector(0,0), Vector(10,10), 10000000)
        
