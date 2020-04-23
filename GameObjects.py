import pygame
import os
from GameExceptions import GetPixelError
from random import randint, choice

class PlayerShip:
    def __init__(self, imagePath):
        None

class Pixel:
    def __init__(self, imageName, pixelID, Position, Speed, resolutionToResize=False):
        """
        Class for background random pixels.
        :param imageName: Image name to load it.
        :param pixelID: Number to identify every pixel object.
        :param Position: Current position on screen, initial position is random.
        :param Speed: Moving speed, a random value.
        :param resolutionToResize: If we are using a resolution different to 1920x1080, we should resize the image.
        """
        self.ID = pixelID
        self.imagePath = os.path.join('Textures', imageName)
        self.Image = pygame.image.load(self.imagePath)
        self.Size = self.Image.get_size()
        if resolutionToResize: # If we need to resize the image for another screen resolution.
            newSize = (resolutionToResize, resolutionToResize)
            self.Image = pygame.transform.scale(self.Image, newSize)
            self.Size = self.Image.get_size() # Updating the image size attribute.
        self.Mask = pygame.mask.from_surface(self.Image)
        self.Rect = self.Image.get_rect()
        self.Position = Position
        self.Speed = Speed

    def Move(self, extraSpeed=False):
        self.Position[1] += (self.Speed + extraSpeed) # Moving just on the y-axis, if there's no extraSpeed, N+False = N.
        return self.Position

    def __str__(self):
        return str('Pixel ID: ' ) + str(self.ID) + str(' ') + str('Speed: ') + str(self.Speed) + str(' ') + str('Current Position: ') + str(self.Position)

class RandomPixels:
    def __init__(self, nPixels, initialPositionRange, maxSpeed, screenResolution, resolutionToResize=False):
        """
        Creating nPixels with random attributes.
        :param nPixels: Number of pixels that we want to create.
        :param initialPositionRange: X-Axis range.
        :param initialSpeedRange: Moving speed range.
        :param resolutionToResize: If we are using a resolution different to 1920x1080, we should resize the image.
        """
        self.Pixels = []
        self.nPixels = nPixels
        self.initialPositionRange = initialPositionRange
        self.maxSpeed = maxSpeed
        self.screenResolution = screenResolution
        self.resolutionToResize = resolutionToResize
        self.speedRange = []
        speedCounter = 0.1
        SpeedLoop = True
        while SpeedLoop:
            self.speedRange.append(round(speedCounter, 1))
            speedCounter += 0.05
            if speedCounter >= maxSpeed: SpeedLoop = False
        for pixelID in range(1, nPixels+1):
            imageName = str('Pixel') + str('_') +  str(choice(('Blue', 'Green', 'Purple', 'Red', 'Yellow'))) + str('.png')
            self.Pixels.append(Pixel(imageName, pixelID, [randint(initialPositionRange[0], initialPositionRange[1]), 0], choice(self.speedRange), resolutionToResize))
        self.lastID = pixelID

    def Move(self, extraSpeed=False):
        for currentPixel in self.Pixels:
            if currentPixel.Move(extraSpeed)[1] > self.screenResolution[1]: # If the pixel is out of screen, we delete it from the list to avoid lag.
                self.Pixels.remove(currentPixel)
        return [currentPixel.Position for currentPixel in self.Pixels] # Returning array with all new positions.

    def createNewPixels(self, nPixels):
        for pixelID in range(nPixels):
            imageName = str('Pixel') + str('_') + str(choice(('Blue', 'Green', 'Purple', 'Red', 'Yellow'))) + str('.png')
            self.Pixels.append(Pixel(imageName, self.lastID+1, [randint(self.initialPositionRange[0], self.initialPositionRange[1]), 0], choice(self.speedRange), self.resolutionToResize))
            self.lastID += 1

    def __getitem__(self, itemKey):
        try:
            return self.Pixels[itemKey]
        except IndexError:
            GetPixelError(f'Error while getting pixel number {itemKey}, max value for pixel number is {len(self.Pixels)-1}.')

    def __len__(self):
        return len(self.Pixels)

    def __str__(self):
        pixelsString = ''
        for currentPixel in self.Pixels:
            pixelsString += str(currentPixel)
            if currentPixel != self.Pixels[-1]:
                pixelsString += str('\n')
        return pixelsString

class Button:
    def __init__(self, imageName, buttonName, screenSize, buttonPosition=None):
        self.imageName = imageName
        self.imagePath = os.path.join('Textures', imageName)
        self.Image = pygame.image.load(self.imagePath).convert_alpha()
        self.Size = self.Image.get_size()
        self.Mask = pygame.mask.from_surface(self.Image)
        self.buttonName = buttonName
        if buttonPosition is None:
            self.Position = (int((screenSize[0] - self.Size[0]) // 2), int((screenSize[1] - self.Size[1]) // 2))
        else:
            self.Position = buttonPosition
        self.Rect = pygame.Rect(self.Position[0], self.Position[1], self.Image.get_rect()[2], self.Image.get_rect()[3])

    def isClicked(self, clickPosition):
        if self.Rect.collidepoint(clickPosition):
            return True
        else:
            return False
    def __str__(self):
        return buttonName