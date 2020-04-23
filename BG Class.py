class BackGround_Part:
    def __init__(self, imageName, movingSpeed, bgID, screenPosition=[0,0], resizeImageForResolution=False):
        """
        Creating the Background surface, with his own features.
        :param imageName: Image.filetype to load the image.
        :param movingSpeed: Number of pixels to move at every iteration.
        :param screenPosition: Position where the image is drawn.
        :param resizeImageForResolution: If we are not using fullscreen, we have to resize the image to use it at resizeImageForResolution resolution. (Example, resizeImageForResolution=(1280,720))
        """
        if type(screenPosition) is not list: # Screen position can't be objects like Tuple, since we need to modify the x value of our position.
            raise TypeError(f'Screen position should be a list type, not a {type(screenPosition)}.')
        else:
            self.ID = bgID
            self.imagePath = os.path.join('Textures', imageName)
            self.Image = pygame.image.load(self.imagePath).convert_alpha() # Convert_Alpha is used to optimize our surface.
            self.Size = self.Image.get_size() # Height and Width image sizes.
            if resizeImageForResolution: # If we have to resize.
                resizeImage = (resizeImageForResolution[0], int(self.Size[1]/2))
                self.Image = pygame.transform.scale(self.Image, resizeImage) # If we are playing at 1280x720, we have to resize the background.
            self.Mask = pygame.mask.from_surface(self.Image)
            self.Rect = self.Image.get_rect()
            self.screenPosition = screenPosition
            self.movingSpeed = movingSpeed

    def __str__(self):
        return str('ID: ') + str(self.ID) + str('\t') + str('Speed: ') + str(self.movingSpeed) + str(' ') + str('Current Position: ') + str(self.screenPosition)

class BackGround:
    def __init__(self, imageName, movingSpeed, screenPosition=[0,0], resizeImageForResolution=False, nPieces=2):
        """
        Creating the Background, since we create the moving bg effect, we need more than one image.
        :param imageName: Image.filetype to load the images.
        :param movingSpeed: Number of pixels to move at every iteration.
        :param screenPosition: Position where the first image is drawn.
        :param resizeImageForResolution: If we are not using fullscreen, we have to resize the image to use it at resizeImageForResolution resolution. (Example, resizeImageForResolution=(1280,720))
        :param nPieces: The number of images that we use to create the moving bg, default is 2, since is the min value to create the moving bg effect.
        """
        if type(screenPosition) is not list:
            raise TypeError(f'Screen position should be a list type, not a {type(screenPosition)}.')
        else:
            self.movingSpeed = movingSpeed
            self.bgParts = []
            for i in range(nPieces):
                newPosition = [screenPosition[0], screenPosition[1] + i*abs(screenPosition[1])]
                self.bgParts.append(BackGround_Part(imageName, movingSpeed, i+1, newPosition, resizeImageForResolution))

        self.currentImage = self.bgParts[0].Image
        self.currentPosition = self.bgParts[0].screenPosition


    def Move(self, extraSpeed=False):
        """
        Moving the background throught the screen, on the y-axis.
        :param extraSpeed: In case that we want to move it different than Background.movingSpeed.
        :return: New (x,y) position.
        """
        pixelsMove = self.movingSpeed + extraSpeed
        self.currentPosition[1] += pixelsMove
        
        return self.currentPosition

    def __getitem__(self, itemKey):
        try:
            return self.bgParts[itemKey]
        except IndexError:
            GetBackgroundError(f'Error while getting the background number {itemKey}, the number of backgrounds is {len(self.bgParts)}.')

    def __str__(self):
        bgString = ''
        for i in range(len(self.bgParts)):
            bgString += str(self.bgParts[i])
            bgString += str('\n')
        return bgString

    def __len__(self):
        return len(self.bgParts)