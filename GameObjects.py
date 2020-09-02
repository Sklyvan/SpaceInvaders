import pygame
import os
from GameExceptions import GetPixelError, WrongShipDirection, GetRectError
from random import randint, choice

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

class Laser:
    def __init__(self, imageName, laserID, laserPosition, laserSpeed, resolutionToResize=False):
        """
        Laser class, for the player ship.
        :param imageName: Image name to load the texture.
        :param laserID: Number to identify every laser object.
        :param laserPosition: Initial laser position.
        :param laserSpeed: Moving speed.
        :param resolutionToResize: If we are using a resolution diferent to 1920x1080, we should resize the image.
        """
        self.ID = laserID
        self.imagePath = os.path.join('Textures', imageName)
        self.Image = pygame.image.load(self.imagePath).convert_alpha()
        if resolutionToResize:
            self.Image = pygame.transform.scale(self.Image, resolutionToResize)
        self.Size = self.Image.get_size()
        self.Mask = pygame.mask.from_surface(self.Image)
        self.Rect = self.Image.get_rect()
        self.Position = laserPosition
        self.Speed = laserSpeed
        self.isVisible = False

    def Move(self, extraSpeed=False): # Since we are just moving on the y-axis, and going up, we have to dicrease the y-value.
        self.Position[1] -= (self.Speed + extraSpeed)
        return self.Position

    def __str__(self):
        return str('Laser ID: ' ) + str(self.ID) + str(' ') + str('Speed: ') + str(self.Speed) + str(' ') + str('Current Position: ') + str(self.Position)

class PlayerShip:
    def __init__(self, imageName, screenSize, Speed, initialHealth=100, resolutionToResize=False, initialPosition=None):
        """
        Player ship object.
        :param imagePath: Image name to load the texture.
        :param Position: Initial position of the ship.
        :param Speed: Moving speed, number of pixels.
        :param initialHealth: Player health, by default is 100.
        :param resolutionToResize: If we are using a resolution different to 1920x1080, we should resize the image.
        """
        self.imagePath = os.path.join('Textures', imageName)
        self.Image = pygame.image.load(self.imagePath).convert_alpha()
        if resolutionToResize:
            self.Image = pygame.transform.scale(self.Image, resolutionToResize)
        self.Size = self.Image.get_size()
        self.Health = initialHealth
        if initialPosition is None:
            self.Position = [int((screenSize[0] - self.Size[0]) // 2), screenSize[1]]
            self.initialPosition = [int((screenSize[0] - self.Size[0]) // 2), screenSize[1]]
        else:
            self.Position = initialPosition
            self.initialPosition = initialPosition
        self.Rect = pygame.Rect(self.Position[0], self.Position[1], self.Image.get_rect()[2], self.Image.get_rect()[3])
        self.Mask = pygame.mask.from_surface(self.Image)
        self.Speed = Speed
        self.currentDirection = 'UP'
        self.isVisible = False
        self.isTouchingBorder = False

    def Move(self, extraSpeed=False):
        if self.isVisible and not self.isTouchingBorder:
            moveDirection = self.currentDirection
            if moveDirection == 'UP':
                self.Position[1] -= self.Speed + extraSpeed
            elif moveDirection == 'DOWN':
                self.Position[1] += self.Speed + extraSpeed
            elif moveDirection == 'LEFT':
                self.Position[0] -= self.Speed + extraSpeed
            elif moveDirection == 'RIGHT':
                self.Position[0] += self.Speed + extraSpeed
            elif moveDirection != False:
                raise WrongShipDirection(f"{moveDirection} isn't a valid direction, direction should be LEFT, RIGHT, UP or DOWN.")

            self.Rect = pygame.Rect(self.Position[0], self.Position[1], self.Image.get_rect()[2], self.Image.get_rect()[3])
            return self.Position
        else:
            return False

    def getReverseDirection(self):
        if self.currentDirection == 'UP':
            return 'DOWN'
        elif self.currentDirection == 'DOWN':
            return 'UP'
        elif self.currentDirection == 'LEFT':
            return 'RIGHT'
        elif self.currentDirection == 'RIGHT':
            return 'LEFT'
        else:
            raise WrongShipDirection(f"Current ship direction is {self.currentDirection}, and it isn't a valid direction, direction should be LEFT, RIGHT, UP or DOWN.")

    def Bounce(self):
        self.currentDirection = self.getReverseDirection()
        self.Move()
        self.currentDirection = False

    def Shoot(self):
        raise NotImplementedError

    def __str__(self):
        return str('Player Ship at ') + str(self.Position) + str(f'with {self.Health} health.')

    def __len__(self):
        return self.Health

class BG:
    def __init__(self, screenSize):
        self.Rect = pygame.Rect(0, 0, screenSize[0], screenSize[1])

    def isContaining(self, objectToCheck):
        try: objectToCheck.Rect
        except AttributeError:
            raise GetRectError(f'Object {type(objectToCheck)} does not have .Rect attribute.')
        else:
            return self.Rect.contains(objectToCheck.Rect)

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

    def createNewPixels(self, nPixels, extraSpeed=0):
        for pixelID in range(nPixels):
            imageName = str('Pixel') + str('_') + str(choice(('Blue', 'Green', 'Purple', 'Red', 'Yellow'))) + str('.png')
            self.Pixels.append(Pixel(imageName, self.lastID+1, [randint(self.initialPositionRange[0], self.initialPositionRange[1]), 0], choice(self.speedRange)+extraSpeed, self.resolutionToResize))
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
    def __init__(self, imageName, buttonName, screenSize=None, buttonPosition=None, isVisible=True, resolutionToResize=False):
        """
        Class to work with on-screen buttons.
        :param imageName: Image file.
        :param buttonName: Type of button.
        :param screenSize: Current screen size to center the object.
        :param buttonPosition: If we don't want to centrate the button, we define the position.
        :param isVisible: When we click on it, it desapears so that turns to False.
        :param resolutionToResize: If we want to resize the button.
        """
        self.imageName = imageName
        self.imagePath = os.path.join('Textures', imageName)
        self.Image = pygame.image.load(self.imagePath).convert_alpha()
        self.Size = self.Image.get_size()
        self.Mask = pygame.mask.from_surface(self.Image)
        self.buttonName = buttonName
        self.isVisible = isVisible
        if buttonPosition is None:
            self.Position = (int((screenSize[0] - self.Size[0]) // 2), int((screenSize[1] - self.Size[1]) // 2))
        else:
            self.Position = buttonPosition
        self.Rect = pygame.Rect(self.Position[0], self.Position[1], self.Image.get_rect()[2], self.Image.get_rect()[3])

    def isClicked(self, clickPosition):
        if self.isVisible:
            if self.Rect.collidepoint(clickPosition):
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        return self.buttonName