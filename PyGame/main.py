

from simplegame import Game, Transform, Axis, Animation, Sprite
from simplegame import Loader, MouseListener, Clear, Jukebox, KeyHandler
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
    
    def damage(self, amount, source, area):
        if not self.destroyed:
            if area.colliderect(self.rect):
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
        destroy(Line(start, end), source)
        
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
    
    def damage(self, amount, source, area):
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
        
def destroy(area, source):
    for obj in Game.active.sprites:
        if hasattr(obj, "damage"):
            if area.colliderect(obj.rect):
                obj.damage(10, source, area)
            
class Circle:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius
    
    def colliderect(self, rect):
        dist = math.sqrt((rect.centerx - self.pos[0])**2 + (rect.centery - self.pos[1])**2)
        return dist < self.radius

class SmallExplosion(Transform):
    def __init__(self, pos):
        super().__init__(pygame.Rect(0,0,0,0), pos=pos, centered=True)
        self.layer = -1
        cb = lambda: Game.active.remove(self)
        self.image = Animation("resources/smallExp", finish_cb=cb).play()
    
    def render(self, surf):
        surf.blit(self.image, self.drawpos)

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
        self.layer = 10
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
    
    def damage(self, amount, source, area):
        for tile in self.tiles:
            if area.colliderect(tile.rect):
                tile.damage(amount, area, area)
    
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
        self.dir = Vector(speed, 0)
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
        destroy(self.rect, self)
    
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
        if random.randint(0,2) == 0:
	        Game.active.add(Tank((start, self.ground-64)))
			
        if random.randint(0,3) == 0:
            Game.active.add(Helicopter((start, 200 + random.randint(0,200))))
        
        hydrants = random.randint(0, w//2)
        s = start
        for i in range(hydrants):
            s = s + random.randint(2, 16)
            Game.active.add(Hydrant((s, self.ground-16)))
            s += 16
            
class Tank(Sprite):
    def __init__(self, pos):
        super().__init__(pos, "tank")
        self.elapsed = 2
        self.shoot_delay = 2.5
        
    def update(self, deltatime):
        self.elapsed += deltatime
        if self.elapsed >= self.shoot_delay:
            mis = Missile(self.pos + (10,15),(-5.8,-3.8))
            Game.active.add(mis)
            self.elapsed -= self.shoot_delay
            
    def damage(self, amount, source, area):
        mis = SmallExplosion(self.pos + (0,10))
        Game.active.add(mis)
        self.destroy()

gravity = Vector(0,0.1)
class Helicopter(Sprite):
    def __init__(self, pos):
        super().__init__(pos, "helekopter")
        self.image = Animation("resources/helekopter").play(True)
        self.elapsed = 1.5
        self.shoot_delay = 2
        self.vec = Vector(0,0.5)
        
    def render(self, surf):
        surf.blit(self.image, self.drawpos)
        
    def update(self, deltatime):
        self.pos += self.vec
    
        self.elapsed += deltatime
        if self.elapsed >= self.shoot_delay:
            if self.pos.x < 300 or self.pos.y < 250:
                mis = Missile(self.pos + (0,32),(-8,1))
            else:
                mis = Missile(self.pos + (0,32),(-8,-1))
            Game.active.add(mis)
            self.elapsed -= self.shoot_delay
            self.vec = Vector(self.vec.x, -self.vec.y) 
    
    def damage(self, amount, source, area):
        mis = SmallExplosion(self.pos)
        Game.active.add(mis)
        self.destroy()

class Missile(Rotatable):
    def __init__(self, pos, vec):
        super().__init__(pos, "missile", 0)
        self.layer = 1
        self.vec = Vector(vec)
    
    def update(self, deltatime):
        if self.vec.y < 0:
            angle = self.vec.angle()
        else:
            angle = 360 - self.vec.angle()
        self.rotation = angle
        self.pos += self.vec
        self.vec += gravity
        if self.pos.y > 550:
            self.explode()
            
    def damage(self, amount, source, area):
        if type(source) == Kaijuu:
            restart()
        self.explode()
        
    def explode(self):
        mis = SmallExplosion(self.pos - (32,32))
        Game.active.add(mis)
        self.destroy()
        
size = (800,600)
game = Game(size, "Kaijuu Game") 
Jukebox.play("resources/234.wav", loop=True)
def restart():
    game.clear()
    ground = size[1]-16
    game.add(Ground(size))
    game.add(Ground(size, start=size[0]))
    monster = Kaijuu((100, ground-192))
    game.add(LaserEyes(monster))
    game.add(monster)
    gen = Generator(ground, size[0])
    gen.start()
    game.add(KeyHandler((restart, pygame.K_r)))
    game.add(gen)
    
restart()
game.run()