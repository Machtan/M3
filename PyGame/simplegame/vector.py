# coding: utf-8
# Created by Jakob Lautrup Nysom @ March 15th 2014
import math
import pygame

degconv = 180/math.pi
class Vector:
    """A 2d vector with some convenience support"""
    class vec_iter: # Support indexing and iteration :p
        def __init__(self, vec):
            self.arr = [vec.x, vec.y]
            self.len = 2
        def __next__(self):
            if self.len == 0: raise StopIteration()
            val = self.arr[-self.len]
            self.len -= 1
            return val
        def __length_hint__(self):
            return self.len
        def __iter__(self):
            return self
    
    def __init__(self, x, y=None):
        if type(x) == tuple:
            self.x = x[0]
            self.y = x[1]
        elif type(x) == Vector:
            self.x = x.x
            self.y = x.y
        else:
            self.x = x
            self.y = y
    
    @property
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    @length.setter
    def length(self, val):
        self.normalize()
        self *= val
    
    @property
    def normalized(self):
        l = self.length
        if l == 0: return self
        return Vector(self.x/l, self.y/l)
    
    @property
    def tuple(self):
        return self.x, self.y
    
    def copy(self):
        return Vector(self.x, self.y)
    
    def dotp(self, other=(1, 0)):
        """Returns the dot product between two vectors"""
        other = Vector(other)
        return (self.x * other.x) + (self.y * other.y)
    
    def rect(self, other=(0,0)):
        """Finds the rect between two vectors"""
        x1 = min(self[0], other[0])
        x2 = max(self[0], other[0])
        y1 = min(self[1], other[1])
        y2 = max(self[1], other[1])
        w = x2 - x1
        h = y2 - y1
        return pygame.Rect(x1, y1, w, h)
    
    def angle(self, other=(1, 0)):
        """returns the angle between two vectors"""
        other = Vector(other)
        dot = self.dotp(other)
        l1 = self.length
        l2 = other.length
        if (l1 * l2) == 0:
            return math.acos(0) * degconv
        else:
            return math.acos(dot / (l1 * l2)) * degconv
    
    def normalize(self):
        """Normalizes the vector"""
        l = len(self)
        self.x /= l
        self.y /= l
    
    def __iter__(self):
        return Vector.vec_iter(self)
    
    def __getitem__(self, item):
        if item == 0: 
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError("Vector index exceeded: {0} > 1".format(item))
    
    def __mul__(self, other):
        if type(other) in {int, float}:
            return Vector(self.x * other, self.y * other)
        elif type(other) == Vector:
            # TODO I don't know how this should work
            return Vector(self.x * other.x, self.y * other.y)
    
    def __add__(self, other):
        if type(other) == Vector:
            return Vector(self.x + other.x, self.y + other.y)
        elif type(other) == tuple:
            return Vector(self.x + other[0], self.y + other[1])
    
    def __sub__(self, other):
        if type(other) == Vector:
            return Vector(self.x - other.x, self.y - other.y)
        elif type(other) == tuple:
            return Vector(self.x - other[0], self.y - other[1])
    
    def __eq__(self, other):
        if type(other) == Vector:
            return self.x == other.x and self.y == other.y
        elif type(other) == tuple:
            return self.x == other[0] and self.y == other[1]
    
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __str__(self):
        return "Vector({0}, {1})".format(self.x, self.y)
    
    def __len__(self):
        return int(math.floor(self.length))
    