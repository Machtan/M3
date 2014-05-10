

from simplegame import Game, Transform, Axis, Animation, Sprite, Loader, MouseListener
import pygame
import os

class DestructibleBlock(Sprite):
    def __init__(self, pos, tilefile):
        super().__init__(pos, tilefile)
    
    def damage(self, amount):
        

class MouseDestroyer(MouseListener):
    def __init__(self, game):
        self.game = game
    
    def on_press(self, pos, button):
        if button == 0:
            for obj in game.sprites:
                if hasattr(obj, "damage"):
                    if obj.rect.collidepoint(pos):
                        print("Damaging {0}!".format(obj))
                        obj.damage(10)


class Skyscraper(Sprite):
    def __init__(self, pos, size, tilefile):
        super().__init__(pos, None)
        self.tiles = []
        img = Loader.load_image(tilefile)
        x1, y1 = pos
        w, h = img.get_size()
        for x in range(size[0]):
            for y in range(size[1]):
                p = (x1 + x*w, y1 - y*h)
                self.tiles.append(DestructibleBlock(p, tilefile))
    
    def render(self, surf):
        for tile in self.tiles:
            tile.render(surf)

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
    ground = 400
    game.add(Skyscraper((0,  ground), (4,16), "window"))
    game.add(Skyscraper((100,ground), (7,13), "window"))
    game.add(Skyscraper((200,ground), (4,18), "window"))
    game.add(Skyscraper((350,ground), (5,35), "window"))
    game.run()
    

if __name__ == '__main__':
    main()