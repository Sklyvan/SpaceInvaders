import pygame
from pygame.locals import *

class GameSettings:
    def __init__(self, fullScreen, gameResolution, pixelSize, playerSpeed, initialPixels=10, devMode=False, extraSpeed=False):
        self.fullScreen = fullScreen
        self.gameResolution = gameResolution
        self.pixelSize = pixelSize
        if fullScreen:
            self.playerSpeed = playerSpeed + 0.65
        else:
            self.playerSpeed = playerSpeed
        self.initialPixels = initialPixels
        self.devMode = devMode
        if fullScreen: self.bgSpeed = 1 + extraSpeed
        else: self.bgSpeed = 0.75 + extraSpeed
        self.gameStarted = False

def GET_KEY(Events):
    for Event in Events:
        if Event.type == pygame.KEYDOWN:
            if Event.key == K_LEFT or Event.key == K_a:
                return 'LEFT'
            if Event.key == K_RIGHT or Event.key == K_d:
                return 'RIGHT'
            if Event.key == K_DOWN or Event.key == K_s:
                return 'DOWN'
            if Event.key == K_UP or Event.key == K_w:
                return 'UP'
            if Event.key == K_r:
                return 'RESTART'
            if Event.key == K_F11:
                return 'F11'
            if Event.key == K_TAB:
                return 'TAB'
            if Event.key == K_ESCAPE:
                return 'ESC'
            if Event.key == K_SPACE:
                return 'SPACE'
        if Event.type == pygame.QUIT:
            return 'QUIT'
    return None