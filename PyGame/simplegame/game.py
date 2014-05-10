# coding: utf-8
# Created by Jabok @ 15 mar 2014
import pygame
from .group import Group
from .jukebox import Jukebox
import os
__doc__ = \
"""
This script contains utilities for easily setting up a prototyping 
environment in PyGame.
"""

class Game:
    """Game is a simple initializer and main 
    loop for small PyGame applications"""
    def __init__(self, winsize=(550, 400), title="Application", iconfile="", color=(255,255,255)):
        print("Initializing...")
        from apputil import init_pygame
        init_pygame()
        self.clock = pygame.time.Clock()
        self.cbqueue = []
        self.default_layer = 5
        self.sprites = Group(layer=self.default_layer)
        self.color = color
        self.running = False
        if iconfile:
            try:
                pygame.display.set_icon(pygame.image.load(iconfile))
            except:
                print("Bad iconfile: '{0}'".format(iconfile))
        self.win = pygame.display.set_mode(winsize)
        pygame.display.set_caption(title)        
        print("Application initialized!")
    
    def _run_queue(self):
        """Runs all callbacks in the queue and clears it"""
        for cb in self.cbqueue:
            cb()
    
    def queue(self, callback):
        """Queues a callback to be run after the next event loop.
        This is mainly to prevent changing the list of spriteects
        while iterating over it for event handling"""
        self.cbqueue.append(callback)
    
    def add(self, *sprites):
        """Adds one or more spriteects to the game"""
        self.queue(lambda: self.sprites.add(*sprites))
        return sprites if len(sprites) > 1 else sprites[-1]
    
    def remove(self, *sprites):
        """Removes a sprite from the game"""
        self.queue(lambda: self.sprites.remove(*sprites))
    
    def clear(self):
        """Clears all sprites from the game"""
        self.queue(lambda: self.sprites.clear())
    
    def set_color(self, color):
        """Sets the color used to clear the background of the game"""
        self.color = color
    
    def pause(self):
        """Pauses the game"""
        self.paused = True
        self._oldcap = pygame.display.get_caption()[0]
        pygame.display.set_caption(self._oldcap+" - Paused")
        if not Jukebox.paused: Jukebox.pause()
        print("App Paused")
    
    def resume(self):
        """Unpauses the game"""
        self.paused = False
        self.clock.tick()
        pygame.display.set_caption(self._oldcap)
        if Jukebox.paused: Jukebox.unpause()
        print("App Resumed")
    
    def run(self):
        """Runs the game"""
        print("Running application -")
        if self.running: return # Nothing to do here :)
        self.running = True
        self.clock.tick() # Remove pent up time
        self.loop = True
        self.paused = False
        mouseevents = {pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP}
        while self.loop:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Window closed
                    self.loop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and event.mod in {1024, 2048}: # Cmd + Q
                        self.loop = False
                    if event.key == pygame.K_p and event.mod in {1024, 2048}: # Cmd + P
                        self.resume() if self.paused else self.pause() # Toggle pause
                    if event.key == pygame.K_d and event.mod in {1024, 2048}:
                        print("Sprites:")
                        print("- "+"\n- ".join([str(sprite) for sprite in self.sprites]))
                    if event.key == pygame.K_j and event.mod in {1024, 2048}:
                        musfile = os.path.join(os.path.dirname(__file__), "dredmor.ogg")
                        Jukebox.play(musfile)
                if not self.paused: # Run the main loop
                    if (event.type in mouseevents):
                        self.sprites.handle_mouse(event)
                    else:
                        self.sprites.handle(event)
            
            if self.paused:
                self.clock.tick(10) # tick, tock
            else:
                # Handle removals as the result of event handling
                self._run_queue() 
        
                # Update
                deltatime = self.clock.tick(60)/1000.0
                self.sprites.update(deltatime)
            
                # Handle removals as the result of updating
                self._run_queue() 
        
                # Render        
                self.win.fill(self.color)
                self.sprites.render(self.win)
                pygame.display.flip()
    
        print("Application ended.")
    