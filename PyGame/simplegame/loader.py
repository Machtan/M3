# coding: utf-8
# Created by Jabok @ May 10th 2014
import os
import pygame
class Loader:
    def load_image(path):
        if not "." in path:
            path += ".png"
        if not "resources" in path:
            path = os.path.join("resources", path)
        image = pygame.image.load(path)
        image.convert()
        return image