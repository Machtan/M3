# coding: utf-8
# Created by Jabok @ 15 mar 2014
"""
This script contains various utility methods for creating 
apps with python (code-freezing)
"""
import sys as _sys

def init_pygame():
    import pygame
    pygame.init()
    if "darwin" in _sys.platform:
        from pygame.macosx import sdlmain_osx as sdlmain
        rfa = sdlmain.RunningFromBundleWithNSApplication()
        if not pygame.display.get_init():
            print("Manually initializing context...")
            sdlmain.InstallNSApplication()