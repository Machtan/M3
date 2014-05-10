

from simplegame import Game, Transform, Axis
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
        self.image = load_image("kaijuu")
        self.rect = self.image.get_rect()
        Transform.__init__(self, self.rect, pos)
        self.add(pygame.K_RIGHT, Axis.X, speed)
        self.add(pygame.K_LEFT, Axis.X, -speed)
    
    def render(self, surf):
        surf.blit(self.image, self.drawpos)
                

def main():
    size = (800,600)
    game = Game(size, "Kaijuu Game")
    game.add(Kaijuu((0,0)))
    game.run()
    

if __name__ == '__main__':
    main()