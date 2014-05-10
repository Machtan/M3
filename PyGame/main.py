

from simplegame import Game, Transform, Axis, Animation
import pygame
import os


def load_image(path):
    if not path.endswith(".png"):
        path += ".png"
    if not "resources" in path:
        path = os.path.join("resources", path)
    image = pygame.image.load(path)
    image.convert()
    return image

speed = 100
class Kaijuu(Transform):
    def __init__(self, pos):
        self.still_image = load_image("kaijuu")
        self.image = self.still_image
        self.rect = self.image.get_rect()
        Transform.__init__(self, self.rect, pos)
        self.add(pygame.K_RIGHT, Axis.X, speed)
        self.add(pygame.K_LEFT, Axis.X, -speed)
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
    
    def render(self, surf):
        surf.blit(self.image, self.drawpos)
                

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