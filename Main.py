from pygame.locals import *
from OnScreenFeatures import GameSettings, GET_KEY
from GameObjects import RandomPixels, Button, PlayerShip, BG, Laser
import time
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

    return WIN, GameSettings(fullScreen, WIN_SIZE, 5, 0.75)

def INITIALIZE_GAME_OBJECTS(GAME_SETTINGS):
    GAME_OBJECTS = {}
    GAME_OBJECTS['Pixels'] = RandomPixels(GAME_SETTINGS.initialPixels, (0, GAME_SETTINGS.gameResolution[0]), GAME_SETTINGS.bgSpeed, GAME_SETTINGS.gameResolution, GAME_SETTINGS.pixelSize)
    GAME_OBJECTS['Buttons'] = [Button('Button_StartGame.png', 'Start Game', GAME_SETTINGS.gameResolution),
                               Button('Button_FullScreen(On).png', 'Full Screen',
                                      buttonPosition=(0, GAME_SETTINGS.gameResolution[1]-(pygame.image.load('./Textures/Button_FullScreen(On).png').convert_alpha().get_size())[1])),
                               Button('Button_FullScreen(Off).png', 'Full Screen',
                                      buttonPosition=(0, GAME_SETTINGS.gameResolution[1]-(pygame.image.load('./Textures/Button_FullScreen(Off).png').convert_alpha().get_size())[1]))]
    GAME_OBJECTS['Player'] = [PlayerShip('Ship_Yellow.png', GAME_SETTINGS.gameResolution, GAME_SETTINGS.playerSpeed, resolutionToResize=(50, 50))]

    if GAME_SETTINGS.fullScreen:
        GAME_OBJECTS['Buttons'][1].isVisible = False
    else:
        GAME_OBJECTS['Buttons'][2].isVisible = False
    initialPlayerPosition = GAME_OBJECTS['Player'][0].Position
    GAME_OBJECTS['PlayerLasers'] = [Laser('Laser_Blue.png', laserID+1, initialPlayerPosition, GAME_SETTINGS.playerSpeed) for laserID in range(10)]
    GAME_OBJECTS['BG'] = [BG(GAME_SETTINGS.gameResolution)]
    return GAME_OBJECTS

def UPDATE_SCREEN(WIN, GAME_OBJECTS, GAME_SETTINGS):
    WIN.fill((32,32,32))
    for currentPixel in GAME_OBJECTS['Pixels'].Pixels:
        WIN.blit(currentPixel.Image, currentPixel.Position)
    for currentButton in GAME_OBJECTS['Buttons']:
        if currentButton.isVisible:
            WIN.blit(currentButton.Image, currentButton.Position)
    for playerLaser in GAME_OBJECTS['PlayerLasers']:
        if playerLaser.isVisible:
            playerLaser.Move()
            WIN.blit(playerLaser.Image, (playerLaser.Position[0] + GAME_OBJECTS['Player'][0].Size[0]/2 - playerLaser.Size[0]/2, playerLaser.Position[1]))
    for playerObject in GAME_OBJECTS['Player']:
        if playerObject.isVisible:
            WIN.blit(playerObject.Image, playerObject.Position)

    if GAME_SETTINGS.devMode:
        WIN.blit(DEV_FONT.render('DEVELOPER MODE', True, (255, 255, 255), (64, 64, 64)), (0,0)) # Dev Mode text.
        WIN.blit(DEV_FONT.render(f'Pixels on Screen: {len(GAME_OBJECTS["Pixels"])}', True, (255, 255, 255), (64, 64, 64)), (0, 12))
        if (pygame.mouse.get_pressed())[0] == 1:
            WIN.blit(DEV_FONT.render(f'Mouse Position: {pygame.mouse.get_pos()[0]},{pygame.mouse.get_pos()[1]}', True, (255, 0, 0), (64, 64, 64)), (0, 25))
        else:
            WIN.blit(DEV_FONT.render(f'Mouse Position: {pygame.mouse.get_pos()[0]},{pygame.mouse.get_pos()[1]}', True, (255, 255, 255), (64, 64, 64)), (0, 25))
        if not GAME_SETTINGS.fullScreen:
            WIN.blit(DEV_FONT.render(f'Ship Position: {GAME_OBJECTS["Player"][0].Position[0]},{GAME_OBJECTS["Player"][0].Position[1]}', True, (255, 255, 255), (64, 64, 64)), (0, 41))
        else:
            WIN.blit(DEV_FONT.render(f'Ship Position: {round(GAME_OBJECTS["Player"][0].Position[0], 3)},{round(GAME_OBJECTS["Player"][0].Position[1], 3)}', True, (255, 255, 255), (64, 64, 64)), (0, 41))
        for currentButton in GAME_OBJECTS['Buttons']:
            if currentButton.isVisible:
                pygame.draw.rect(WIN, (255, 0, 0), currentButton.Rect, 1) # Buttons HitBox.
        for playerObject in GAME_OBJECTS['Player']:
            if playerObject.isVisible:
                pygame.draw.rect(WIN, (255, 0, 0), playerObject.Rect, 1)  # Player ship HitBox.
        for bg in GAME_OBJECTS['BG']:
            pygame.draw.rect(WIN, (255, 0, 0), bg.Rect, 1)

    GAME_OBJECTS['Player'][0].Move()
    GAME_OBJECTS['Pixels'].Move() # Moving pixel.
    if random.randint(1, 200) == 100: # To avoid any patern creation, we decide if we create 10 new random pixels or not, randomly.
        GAME_OBJECTS['Pixels'].createNewPixels(random.randint(1,10)) # The number of new pixels is randomly choosen between 1 and 10.

def START_GAME():
    GAME_SETTINGS.gameStarted = True
    for currentButton in GAME_OBJECTS['Buttons']: # Cleaning buttons from screen.
        currentButton.isVisible = False
    for currentPixel in GAME_OBJECTS['Pixels'].Pixels:  # Moving faster all pixels on screen.
        currentPixel.Speed = random.choice((0.5, 1, 1.5, 2))
    GAME_OBJECTS['Player'][0].isVisible = True

    return time.time() # Getting the initial time of the game.

fullScreen = False
WIN, GAME_SETTINGS = INITIALIZE_SCREEN(fullScreen)
GAME_OBJECTS = INITIALIZE_GAME_OBJECTS(GAME_SETTINGS)
GAME_LOOP = True
StartTime = False
while GAME_LOOP:
    if GAME_OBJECTS['BG'][0].isContaining(GAME_OBJECTS['Player'][0]):
        None
    elif GAME_SETTINGS.gameStarted and StartTime is not False and (time.time() - StartTime) > 0.5: # If player ship is touching screen edges, bounce.
        GAME_OBJECTS['Player'][0].Bounce()
    KEY = GET_KEY(pygame.event.get())
    if KEY == 'LEFT':
        GAME_OBJECTS['Player'][0].currentDirection = KEY
    elif KEY == 'RIGHT':
        GAME_OBJECTS['Player'][0].currentDirection = KEY
    elif KEY == 'UP':
        GAME_OBJECTS['Player'][0].currentDirection = KEY
    elif KEY == 'DOWN':
        GAME_OBJECTS['Player'][0].currentDirection = KEY
    elif KEY == 'TAB':
        if not GAME_SETTINGS.devMode: GAME_SETTINGS.devMode = True
        else: GAME_SETTINGS.devMode = False
    elif KEY == 'SPACE':
        if not GAME_SETTINGS.gameStarted:
            StartTime = START_GAME()
        else:
            GAME_OBJECTS['PlayerLasers'][0].isVisible = True
    elif KEY == 'F11':
        if GAME_SETTINGS.fullScreen:
            GAME_SETTINGS.fullScreen = False
        elif not GAME_SETTINGS.fullScreen:
            GAME_SETTINGS.fullScreen = True
        WIN, GAME_SETTINGS = INITIALIZE_SCREEN(GAME_SETTINGS.fullScreen)
        GAME_OBJECTS = INITIALIZE_GAME_OBJECTS(GAME_SETTINGS)
    elif KEY == 'RESTART':
        if GAME_SETTINGS.gameStarted:
            WIN, GAME_SETTINGS = INITIALIZE_SCREEN(GAME_SETTINGS.fullScreen)
            GAME_OBJECTS = INITIALIZE_GAME_OBJECTS(GAME_SETTINGS)
            StartTime = False
    elif KEY == 'ESC' or KEY == 'QUIT':
        GAME_LOOP = False
        pygame.quit()
        sys.exit()

    if (pygame.mouse.get_pressed())[0] == 1: # If there's a Left Click.
        if not GAME_SETTINGS.gameStarted:
            if GAME_OBJECTS['Buttons'][0].isClicked(pygame.mouse.get_pos()): # If we clicked on the Start Game button and the button is on screen.
                StartTime = START_GAME()

            if GAME_OBJECTS['Buttons'][1].isClicked(pygame.mouse.get_pos()): # If we click on the FullScreen(On) button and the button is on screen.
                GAME_SETTINGS.fullScreen = True
                WIN, GAME_SETTINGS = INITIALIZE_SCREEN(GAME_SETTINGS.fullScreen)
                GAME_OBJECTS = INITIALIZE_GAME_OBJECTS(GAME_SETTINGS)
                GAME_OBJECTS['Buttons'][1].isVisible, GAME_OBJECTS['Buttons'][2].isVisible = False, True

            if GAME_OBJECTS['Buttons'][2].isClicked(pygame.mouse.get_pos()): # If we click on the FullScreen(Off) button and the button is on screen.
                GAME_SETTINGS.fullScreen = False
                WIN, GAME_SETTINGS = INITIALIZE_SCREEN(GAME_SETTINGS.fullScreen)
                GAME_OBJECTS = INITIALIZE_GAME_OBJECTS(GAME_SETTINGS)
                GAME_OBJECTS['Buttons'][1].isVisible, GAME_OBJECTS['Buttons'][2].isVisible = True, False


    UPDATE_SCREEN(WIN, GAME_OBJECTS, GAME_SETTINGS)
    pygame.display.update()