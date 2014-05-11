

from simplegame import Game, Transform, Axis, Animation, Sprite
from simplegame import Loader, MouseListener, Clear, Jukebox
from simplegame import Vector
from upgrade import Upgrade
from rotation import Rotatable
import random
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
        destroy(Line(start, end))
        
    def update(self, deltatime):
        self.elapsed += deltatime
        if self.elapsed >= self.duration:
            self.destroy()

class Hydrant(Sprite):
    def __init__(self, pos):
        super().__init__(pos, "hydrant")
        self.layer = 0
        self.spout = None
        self.destroyed = False
    
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
    
    def move(self, vec):
        super().move(vec)
        if self.rect.right < 0:
            self.destroy()
    
    def destroy(self):
        super().destroy()
        self.spout.stop()

class RelPosFinder(MouseListener):
    def __init__(self, target):
        super().__init__()
        self.target = target
    
    def on_press(self, pos, button):
        rel = Vector(pos) - self.target.pos
        print("Relative distance to the target:", rel.tuple)
        
def destroy(area):
    for obj in Game.active.sprites:
        if hasattr(obj, "damage"):
            if area.colliderect(obj.rect):
                obj.damage(10, area)
            
class Circle:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius
    
    def colliderect(self, rect):
        dist = math.sqrt((rect.centerx - self.pos[0])**2 + (rect.centery - self.pos[1])**2)
        return dist < self.radius

class Line:
    def __init__(self, startpos, endpos):
        self.start = startpos
        self.end = endpos
        delta = Vector(self.end) - self.start
        self.x1 = min(startpos[0], endpos[0])
        self.x2 = max(startpos[0], endpos[0])
        a = delta.y / delta.x
        b = self.start[1] - a * self.start[0]
        self.value = lambda x: a*x + b
    
    def colliderect(self, rect):
        left = self.value(rect.left)
        if rect.right <= self.x1: return False
        if rect.left >= self.x2: return False
        if rect.top < left < rect.bottom: 
            return True
        right = self.value(rect.right)
        if rect.top < right < rect.bottom:
            return True
        return False
        
        

laser_length = 400
class LaserEyes(Upgrade):
    def __init__(self, parent, key=pygame.K_e):
        super().__init__(parent, "Laser Eyes", (35, 24), "lasereye", 
            "Zap!", centered=True)
        self.key = key
        self.keydown = False
    
    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.key:
                self.shoot_laser()
    
    def shoot_laser(self):
        start = Vector(self.rect.center)
        direction = Vector(pygame.mouse.get_pos()) - start
        end = start + direction.normalized * laser_length
        Game.active.add(Laser(start, end))

class Skyscraper(Sprite):
    def __init__(self, pos, size, tilefile, winwidth, cb):
        self.tiles = []
        img = Loader.load_image(tilefile)
        x1, y1 = pos
        w, h = img.get_size()
        totalw = size[0] * w
        totalh = size[1] * h
        self.winwidth = winwidth
        rect = pygame.Rect(x1, y1 - totalh, totalw, totalh)
        super().__init__(rect.topleft, None, rect=rect)
        self.visible = False
        self.cb = cb
        
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
    
    def move(self, vec):
        if (not self.visible) and self.rect.right < self.winwidth:
            self.visible = True
            self.cb()
            
        super().move(vec)
        if self.rect.right < 0:
            self.destroy()

speed = 100
class Kaijuu(Sprite):
    def __init__(self, pos):
        super().__init__(pos, "kaijuu")
        self.still_image = self.image
        self.add_binding(pygame.K_RIGHT, Axis.X, speed)
        self.walking = False
        self.layer = 3

    def update(self, deltatime):
        Transform.update(self, deltatime)
        if self.dir.x:
            if not self.walking:
                self.walking = True
                self.image = Animation("resources/kaijuu").play(True)
        else:
            if self.walking:
                self.walking = False
                self.image.stop(self.still_image)
        destroy(self.rect)
    
    def move(self, vec):
        #super().move(vec)
        mov = vec * -1
        for sprite in Game.active.sprites:
            if hasattr(sprite, "move"):
                if sprite is self: 
                    continue
                elif sprite in self.children:
                    continue
                else:
                    sprite.move(mov)

class Ground(Sprite):
    def __init__(self, windowsize, start=0):
        super().__init__((start, windowsize[1]-16), "ground")
        self.windowsize = windowsize
        print("Ground added at ", self.pos)
    
    def move(self, vec):
        Sprite.move(self, vec)
        if self.rect.right < 0:
            print("Jumping!")
            print("old:", self.pos)
            self.move(Vector(self.windowsize[0]*2, 0))
            print("new:", self.pos)

class Generator:
    def __init__(self, ground, winwidth):
        self.ground = ground
        self.winwidth = winwidth
    
    def start(self):
        self.generate()
    
    def generate(self, start=None):
        start = start if start else self.winwidth
        w = random.randint(4, 8)
        h = random.randint(w, w*4)
        padding = random.randint(4, 16)
        x = start + padding
        skyscraper = Skyscraper((x, self.ground), (w, h), 
            "window", self.winwidth, self.generate)
        Game.active.add(skyscraper)
        
        hydrants = random.randint(1, w)
        s = start
        for i in range(hydrants):
            s = s + random.randint(2, 16)
            Game.active.add(Hydrant((s, self.ground-16)))
            s += 16

def main():
    """
    For at et objekt opdateres: definer 'update(self, deltatime)'
    For at et objekt renderes: definer 'render(self, surf)'
    For at et object modtager events: definer 'handle(self, event)'
    
    For at kalde en metode i superklassen: ex Transform.render(self, surf)
    
    
    """
    size = (800,600)
    game = Game(size, "Kaijuu Game") 
    ground = size[1]-16
    game.add(Ground(size))
    game.add(Ground(size, start=size[0]))
    monster = Kaijuu((100, ground-192))
    game.add(LaserEyes(monster))
    game.add(monster)
    gen = Generator(ground, size[0])
    gen.start()
    Jukebox.play("resources/234.wav")
    game.add(gen)
    """game.add(RelPosFinder(monster))
    game.add(Hydrant((400, ground-16)))
    game.add(Hydrant((416, ground-16)))
    game.add(Hydrant((432, ground-16)))
    game.add(Hydrant((448, ground-16)))
    game.add(Hydrant((500, ground-16)))
    game.add(Skyscraper((0,  ground), (4,16), "window"))
    game.add(Skyscraper((100,ground), (7,13), "window"))
    game.add(Skyscraper((200,ground), (4,18), "window"))
    game.add(Skyscraper((350,ground), (5,35), "window"))"""
    game.run()
    

if __name__ == '__main__':
    main()