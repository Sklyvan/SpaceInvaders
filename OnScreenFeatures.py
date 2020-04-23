import pygame
from pygame.locals import *

class GameSettings:
    def __init__(self, fullScreen, gameResolution, pixelSize, initialPixels=10, devMode=False, extraSpeed=False):
        self.fullScreen = fullScreen
        self.gameResolution = gameResolution
        self.pixelSize = pixelSize
        self.initialPixels = initialPixels
        self.devMode = devMode
        if fullScreen: self.bgSpeed = 1 + extraSpeed
        else: self.bgSpeed = 0.75 + extraSpeed