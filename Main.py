from pygame.locals import *
from OnScreenFeatures import GameSettings
from GameObjects import RandomPixels, Button
import random
import pygame
import ctypes
import sys
import os

pygame.font.init() # Initializing just the fonts, full library initialized later.
DEV_FONT = pygame.font.SysFont('Consolas', 15)
GAME_FONT = pygame.font.Font('./Textures/Font.ttf', 50)

def INITIALIZE_SCREEN(fullScreen):
    if fullScreen:
        FLAGS = FULLSCREEN | DOUBLEBUF  # Fullscreen mode.
        user32 = ctypes.windll.user32
        SCREENSIZE = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        WIN_SIZE = (SCREENSIZE[0], SCREENSIZE[1])  # Screen resolution depending on the screen size.
        pygame.init()  # Starting PyGame library.
        WIN = pygame.display.set_mode(WIN_SIZE, FULLSCREEN)  # Creating screen in fullscreen mode.

    if not fullScreen:
        user32 = ctypes.windll.user32
        SCREENSIZE = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        WIN_SIZE = (int(SCREENSIZE[0] // 1.5), int(SCREENSIZE[1] // 1.5)) # Screen resolution depending on the screen size. (If screen size 1920x1080, WIN_SIZE = (1280, 720)).
        CENTER_POSITION = int((SCREENSIZE[0] - WIN_SIZE[0]) // 2), int((SCREENSIZE[1] - WIN_SIZE[1]) // 2)
        # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (CENTER_POSITION)  # Starting the game screen on the center.
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (-1650, 200)  # Double Screen DEV Mode.
        pygame.init()  # Starting PyGame library.
        WIN = pygame.display.set_mode(WIN_SIZE)  # Creating screen.

    pygame.display.set_caption('Space Invaders')
    pygame.mouse.set_visible(True) # Hidding the mouse.

    return WIN, GameSettings(fullScreen, WIN_SIZE, 5)

def INITIALIZE_GAME_OBJECTS(GAME_SETTINGS):
    GAME_OBJECTS = {}
    GAME_OBJECTS['Pixels'] = RandomPixels(GAME_SETTINGS.initialPixels, (0, GAME_SETTINGS.gameResolution[0]), GAME_SETTINGS.bgSpeed, GAME_SETTINGS.gameResolution, GAME_SETTINGS.pixelSize)
    GAME_OBJECTS['Buttons'] = [Button('Button_StartGame.png', 'Start Game', GAME_SETTINGS.gameResolution)]
    return GAME_OBJECTS

def UPDATE_SCREEN(WIN, GAME_OBJECTS, GAME_SETTINGS):
    WIN.fill((32,32,32))
    for currentPixel in GAME_OBJECTS['Pixels'].Pixels:
        WIN.blit(currentPixel.Image, currentPixel.Position)
    for currentButton in GAME_OBJECTS['Buttons']:
        WIN.blit(currentButton.Image, currentButton.Position)
    if GAME_SETTINGS.devMode:
        WIN.blit(DEV_FONT.render('DEV MODE', True, (255, 0, 0)), (0,0)) # Dev Mode text.
        WIN.blit(DEV_FONT.render(f'Pixels on Screen: {len(GAME_OBJECTS["Pixels"])}', True, (255, 255, 255)), (0, 12))
        for currentButton in GAME_OBJECTS['Buttons']:
            pygame.draw.rect(WIN, (255, 0, 0), currentButton.Rect, 1)
    GAME_OBJECTS['Pixels'].Move() # Moving pixel.
    if random.randint(1, 200) == 100: # To avoid any patern creation, we decide if we create 10 new random pixels or not, randomly.
        GAME_OBJECTS['Pixels'].createNewPixels(random.randint(1,10))

WIN, GAME_SETTINGS = INITIALIZE_SCREEN(False)
GAME_OBJECTS = INITIALIZE_GAME_OBJECTS(GAME_SETTINGS)
GAME_LOOP = True

while GAME_LOOP:
    if (pygame.mouse.get_pressed())[0] == 1:
        if GAME_OBJECTS['Buttons'][0].isClicked(pygame.mouse.get_pos()):
            print('Click!')
    for Event in pygame.event.get():
        if Event.type == pygame.KEYDOWN:
            if Event.key == K_LEFT or Event.key == K_a:
                print("LEFT")
            if Event.key == K_RIGHT or Event.key == K_d:
                print("RIGHT")
            if Event.key == K_DOWN or Event.key == K_s:
                print("DOWN")
            if Event.key == K_UP or Event.key == K_w:
                print("UP")
            if Event.key == K_TAB:
                if not GAME_SETTINGS.devMode: GAME_SETTINGS.devMode = True
                else: GAME_SETTINGS.devMode = False
            if Event.key == K_ESCAPE:
                GAME_LOOP = False
                pygame.quit()
                sys.exit()
            if Event.key == K_SPACE:
                print("SPACE")
        if Event.type == pygame.QUIT:
            GAME_LOOP = False
            pygame.quit()
            sys.exit()

    UPDATE_SCREEN(WIN, GAME_OBJECTS, GAME_SETTINGS)
    pygame.display.update()