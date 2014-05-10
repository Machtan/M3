

from simplegame import Game, Transform, Axis, Animation, Sprite, Loader, MouseListener
from simplegame import Vector
import pygame
import os
import math

class DestructibleBlock(Sprite):
    def __init__(self, pos, tilefile):
        super().__init__(pos, tilefile)
        self.destroyed = False
    
    def damage(self, amount, pos):
        if not self.destroyed:
            self.image = Loader.load_image("brokenwindow")
            self.destroyed = True

class Hydrant(Sprite):
    def __init__(self, pos):
        super().__init__(pos, "hydrant")
        self.layer = 0
        self.destroyed = False
        self.spout = None
    
    def damage(self, amount, pos):
        if not self.destroyed:
            self.image = Loader.load_image("brokenhydrant")
            self.destroyed = True
            self.spout = Animation("resources/wateranim").play(True)
    
    def render(self, surf):
        if self.spout:
            spoutpos = (self.pos - Vector(0, self.spout.get_height()-24)).tuple
            surf.blit(self.spout, spoutpos)
        super().render(surf)

class RelPosFinder(MouseListener):
    def __init__(self, target):
        super().__init__()
        self.target = target
    
    def on_press(self, pos, button):
        rel = Vector(pos) - self.target.pos
        print("Relative distance to the target:", rel.tuple)
        

class MouseDestroyer(MouseListener):
    def __init__(self, game):
        super().__init__()
        self.game = game
        
    def destroy(self, area):
        for obj in self.game.sprites:
            if hasattr(obj, "damage"):
                if area.colliderect(obj.rect):
                    #print("Destroying", obj)
                    obj.damage(10, area)
    
    def on_press(self, pos, button):
        if button == 1:
            self.destroy(Circle(pos, 64))
            
class Circle:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius
    
    def colliderect(self, rect):
        dist = math.sqrt((rect.centerx - self.pos[0])**2 + (rect.centery - self.pos[1])**2)
        return dist < self.radius

class Skyscraper(Sprite):
    def __init__(self, pos, size, tilefile):
        self.tiles = []
        img = Loader.load_image(tilefile)
        x1, y1 = pos
        w, h = img.get_size()
        totalw = size[0] * w
        totalh = size[1] * h
        rect = pygame.Rect(x1, y1 - totalh, totalw, totalh)
        super().__init__(rect.topleft, None, rect=rect)
        
        for x in range(1, size[0]+1):
            for y in range(1, size[1]+1):
                p = (x1 + x*w, y1 - y*h)
                block = DestructibleBlock(p, tilefile)
                self.add_child(block)
                self.tiles.append(block)
        
        
    
    def render(self, surf):
        for tile in self.tiles:
            tile.render(surf)
    
    def damage(self, amount, area):
        for tile in self.tiles:
            if area.colliderect(tile.rect):
                tile.damage(amount, area)

speed = 50

class Ground(Sprite):
    def __init__(self, windowsize, start=0):
        super().__init__((start, windowsize[1]-16), "ground")
        self.windowsize = windowsize
    
    def move(self, vec):
        Sprite.move(self, vec)
        if self.rect.right < 0:
            self.moveBy(Vector(self.windowsize[0], 0))

def main():
    """
    For at et objekt opdateres: definer 'update(self, deltatime)'
    For at et objekt renderes: definer 'render(self, surf)'
    For at et object modtager events: definer 'handle(self, event)'
    
    For at kalde en metode i superklassen: ex Transform.render(self, surf)
    
    
    """
    size = (800,600)
    game = Game(size, "Kaijuu Game")
    
    destroyer = MouseDestroyer(game)
    game.add(destroyer)
    
    class Kaijuu(Sprite):
        def __init__(self, pos):
            super().__init__(pos, "kaijuu")
            self.still_image = self.image
            self.add_binding(pygame.K_RIGHT, Axis.X, speed)
            #self.add_binding(pygame.K_LEFT, Axis.X, -speed)
            self.walking = False
            self.layer = 3
    
        def update(self, deltatime):
            Transform.update(self, deltatime)
            if self.dir.x:
                movement = self.dir.x*deltatime
                for sprite in game.sprites:
                    if hasattr(sprite, "move"):
                        sprite.move(Vector(-movement, 0))
                if not self.walking:
                    self.walking = True
                    self.image = Animation("resources/kaijuu").play(True)
            else:
                if self.walking:
                    self.walking = False
                    self.image.stop(self.still_image)
            destroyer.destroy(self.rect)
    
    ground = size[1]-16
    game.add(Ground(size))
    game.add(Ground(size, start=size[0]))
    monster = Kaijuu((100, ground-192))
    game.add(monster)
    game.add(RelPosFinder(monster))
    game.add(Hydrant((400, ground-16)))
    game.add(Hydrant((416, ground-16)))
    game.add(Hydrant((432, ground-16)))
    game.add(Hydrant((448, ground-16)))
    game.add(Hydrant((500, ground-16)))
    game.add(Skyscraper((0,  ground), (4,16), "window"))
    game.add(Skyscraper((100,ground), (7,13), "window"))
    game.add(Skyscraper((200,ground), (4,18), "window"))
    game.add(Skyscraper((350,ground), (5,35), "window"))
    game.run()
    

if __name__ == '__main__':
    main()