# endcoding: utf-8
# Created by Jabok @ March 30th 2014
import yaml
import os
import pygame
import math
from .drawutils import Clear

class Animation(Clear):
    """A spritesheet-based animation class"""
    # Static members
    active = set()
    
    def update(deltatime):
        """Updates all active animations"""
        for anim in Animation.active:
            anim.progress(deltatime)
    
    def __init__(self, sheetfile, cellrect=None, delays=None):
        """Creates a new information. The sheetfile is a path to the file
        containing a strip of images to use for this animation. The cellrect
        contains how big each cell in the animation is, and where in the
        sheetfile the animation should start. Delays are the frame lengths."""
        if not (cellrect or delays): # Load the animation from a file
            filepath = sheetfile
            if not filepath.endswith(".yaml"):
                filepath += ".yaml"
            if not os.path.exists(filepath):
                raise IOError("Could not load animation: '{0}'".format(filepath))
            with open(filepath, "r") as f:
                config = yaml.load(f)
                
            self.startpos = config['startpos']
            self.cellsize = config['cellsize']
            self.sheetfile = config['sheetfile']
            self.delays = config['delays']
        else: # Create the animation from parameters :)
            self.startpos   = cellrect.topleft # pixels
            self.cellsize   = cellrect.size # pixels
            self.delays     = delays # in ms
            self.sheetfile  = sheetfile # path
        
        super().__init__(self.cellsize)
        self.time       = 0
        self.running    = False
        self.loop       = False 
        if not os.path.exists(self.sheetfile):
            self.sheetfile = os.path.join(os.path.dirname(sheetfile), self.sheetfile)
        self.source     = pygame.image.load(self.sheetfile)
        self.source.convert_alpha()
        self.convert_alpha()
        self.set_frame(0)
    
    def save(self, filepath):
        """Saves the animation to the given file as yaml data"""
        metadata = {
            "sheetfile":    self.sheetfile,
            "startpos":     self.startpos,
            "cellsize":     self.cellsize,
            "delays":       self.delays
        }
        with open(filepath, "w") as f:
            yaml.dump(f, metadata)
    
    def set_frame(self, frame):
        """Sets the current frame of the animation to the one given"""
        self.frame = frame
        sw = self.source.get_width()
        dx = (self.startpos[0] + frame*self.cellsize[0])
        x = dx % sw
        y = self.startpos[1] + math.floor(dx/sw) * self.cellsize[1]
        if (y >= self.source.get_height()):
            y -= self.source.get_height();
        rect = pygame.Rect((x, y), self.cellsize)
        self.clear()
        self.blit(self.source, (0,0), rect)
    
    def play(self, loop=False):
        """Starts the animation"""
        self.running = True
        self.loop = loop
        Animation.active.add(self) # register for updates
        return self # Allow quickstarting :)
    
    def pause(self):
        """Pauses the animation"""
        self.running = False
    
    def stop(self, stopimage=None):
        """Stops the animation"""
        if self.running:
            self.running = False
            Animation.active.remove(self) # unregister for updates
        self.time = 0
        self.set_frame(0)
        if stopimage:
            self.clear()
            self.blit(stopimage, (0,0))
    
    def progress(self, deltatime):
        """Updates the animation"""
        if self.running:
            self.time += deltatime*1000.0 # ms / sec
            if self.time >= self.delays[self.frame]:
                self.time -= self.delays[self.frame]
                self.frame += 1
                self.set_frame(self.frame)
                if self.frame == len(self.delays): # The end is reached
                    self.frame = 0
                    self.set_frame(self.frame)
                    if not self.loop:
                        self.running = False


            
def main():
    from simplegame import Game, Dragable
    
    class Animated(Dragable):
        def __init__(self, pos, animfile):
            super().__init__()
            self.image = Animation(animfile).play(True)
            self.rect = pygame.Rect(pos, self.image.get_size())
    
        def render(self, surf):
            surf.blit(self.image, self.rect)
    
    game = Game((600, 500), "Animation test :)")
    
    game.add(Animation)
    game.add(Animated((50,50), "anim"))
    
    game.run()

if __name__ == '__main__':
    main()
    
        