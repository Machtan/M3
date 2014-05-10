# coding: utf-8
# Created by Jabok @ April 17th 2014
import pygame
from .vector import Vector

class Group:                    
    """Contains methods for easier handling groups of sprites"""
    def __init__(self, *sprites, layer=5):
        self.sprites = {}
        self.default_layer = layer
        self.add(*sprites)
    
    @property
    def rect(self):
        sr = self.rect
        left, top, right, bottom = sr.left, sr.top, sr.right, sr.bottom
        for sprite in added:
            if hasattr(sprite, rect):
                r       = sprite.rect
                left    = min(left, r.left)
                right   = max(right, r.right)
                top     = min(top, r.top)
                bottom  = max(bottom, r.bottom)
        return pygame.Rect(left, top, right-left, bottom-top)
    
    def move(self, amount):
        """Moves every sprite in the group by the given amount"""
        self.call("move", amount)
    
    def add(self, *sprites):
        """Adds sprites to the group"""
        for sprite in sprites:
            if not hasattr(sprite, "layer"):
                setattr(sprite, "layer", self.default_layer)
            if not sprite.layer in self.sprites:
                self.sprites[sprite.layer] = {sprite}
            else:
                self.sprites[sprite.layer].add(sprite)
        
    def get(self, layer, default=set()):
        """Returns the sprites in the requested layer, or the default 
        if the layer doesn't exist"""
        if layer in self.sprites:
            return self.sprites[layer]
        else:
            return default
    
    def remove(self, *sprites):
        """Removes sprites from the group"""
        for sprite in sprites:
            con = self.sprites[sprite.layer]
            if sprite in con:
                con.remove(sprite)
                if hasattr(sprite, "remove"):
                    sprite.remove()
    
    def clear(self):
        """Clears the group"""
        self.sprites = {}
    
    def contains(self, sprite):
        """Checks for a sprite in the group"""
        return sprite in self.sprites(sprite.layer, set())
    
    def call(self, path, *args, **kwargs):
        """Calls a method on all viable sprites and returns if any of the calls 
        return true (else false). Allows member syntax, eg. 'rect.colliderect' as the path"""
        parts = path.split(".")
        def get_member(sprite, parts):
            target = sprite
            for part in parts:
                if not hasattr(target, part):
                    return sprite, False
                else:
                    target = getattr(target, part)
            return target, True
        
        for sprite in self:
            func, succes = get_member(sprite, parts)
            if not succes: continue
            if func(*args, **kwargs) == True: # True breaks the iteration
                return True
        return False
    
    def colliderect(self, rect):
        """Checks whether a rect collides with the group"""
        return self.call("rect.colliderect", rect)
        
    def collidepoint(self, point):
        """Checks whether a point is inside the group"""
        return self.call("rect.collidepoint", point)
    
    def render(self, surf):
        """Renders all sprites in the group in order"""
        self.call("render", surf)
    
    def update(self, deltatime):
        """Updates all sprites in layered order"""
        self.call("update", deltatime)
    
    def handle(self, event):
        """Lets all sprites handle the event"""
        self.call("handle", event)
    
    def handle_mouse(self, event):
        """Lets all sprites handle the event"""
        self.call("handle_mouse", event)
    
    def __iter__(self):
        for layer, sprite_list in sorted(self.sprites.items(), reverse=True):
            yield from sprite_list

def main():
    """derp"""
    class Derp:
        def __init__(self, name, layer):
            self.name = name
            self.layer = layer
        def __str__(self):
            return self.name
        def hello(self):
            print("Hello, my name is {0}".format(self.name))
        rect = pygame.Rect(1,1,1,1)
    
    class D2:
        pass
    
    def iterprint(*args):
        for obj in args:
            print(obj)
        
    grp = SpriteGroup(Derp("Hi", 1), Derp("I", 2), Derp("Derp", 3), D2())
    grp.call("hello")

if __name__ == '__main__':
    main()