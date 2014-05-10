# coding: utf-8
# Jabok @ 10th May
from simplegame import Sprite
class Upgrade(Sprite):
    def __init__(self, parent, name, relpos, imagefile, description):
        pos = parent.pos + relpos
        super().__init__(pos, imagefile)
        self.parent = parent
        self.description = description
        self.name = name

        
        
