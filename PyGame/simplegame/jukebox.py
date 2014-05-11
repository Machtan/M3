# coding: utf-8
# Created by Jabok @ April 19th 2014
import pygame
import os
pymus = pygame.mixer.music

class _Meta(type): # Metaclass to make volume a static property of the jukebox
    def _donotset(self, val): raise Exception("This property is read-only!")
    volume  = property(lambda s: pymus.get_volume(),    lambda s,v: pymus.set_volume(v))
    playing = property(lambda s: pymus.get_busy(),      _donotset)
    played  = property(lambda s: pymus.get_pos(),       _donotset)
    signal  = property(lambda s: pymus.get_endevent(),  lambda s,v: pymus.set_endevent(v))

class Jukebox(metaclass=_Meta):
    paused = False
    loop = False
    current = None
    if not pygame.mixer.get_init(): 
        pygame.mixer.init()
    
    endmusicevent = 57
    
    def play(filepath, *args, loop=False, **kwargs):
        if Jukebox.playing: Jukebox.stop()
        Jukebox.paused = False
        if not os.path.exists(filepath):
            raise FileNotFoundError("Cannot find music track at '{0}'".format(filepath))
        pymus.load(filepath)
        Jukebox.signal = Jukebox.endmusicevent
        Jukebox.loop = loop
        Jukebox.current = filepath
        pymus.play(*args, **kwargs)
    def stop(): 
        Jukebox.paused = False
        pymus.stop()
    def pause(): 
        Jukebox.paused = True
        pymus.pause()
    def unpause(): 
        Jukebox.paused = False
        pymus.unpause()
    def rewind(): 
        pymus.rewind()
    def fadeout(millis): 
        pymus.fadeout(millis)
    
    def handle(event):
        if event.type == Jukebox.endmusicevent:
            if Jukebox.loop:
                Jukebox.play(Jukebox.current, loop=True)

def main():
    from simplegame import Game, KeyHandler, Label
    playtext = "Playing", "Press space to pause"
    pausetext = "Paused", "Press space to resume"
    shadow = None #(0,0,0)
    statelabel = Label(playtext[0], (150,80), color=(255,255,255), shadow_color=shadow, center=True)
    keylabel = Label(playtext[1], (150, 105), color=(255,255,255), shadow_color=shadow, center=True)
    def toggle_pause(): 
        if Jukebox.paused:
            statelabel.text = playtext[0]
            keylabel.text = playtext[1]
            Jukebox.unpause()
        else: 
            statelabel.text = pausetext[0]
            keylabel.text = pausetext[1]
            Jukebox.pause()
    game = Game((300,200),"Music playback test", color=(255,0,255))
    game.add(KeyHandler(toggle_pause, pygame.K_SPACE))
    game.add(statelabel, keylabel)
    Jukebox.play("dredmor.ogg")
    game.run()

if __name__ == '__main__':
    main()
    