"""
Author: Trevor Stalnaker
File Name: drawable.py

A super class with methods for interacting with visual game components
"""

import pygame
from polybius.utils import Vector2
from polybius.managers.frameManager import FRAMES
from polybius.utils.rectmanager import getRects, moveRects

class Drawable():

    # Class Variable
    WINDOW_OFFSET = Vector2(0,0)

    @classmethod
    def updateOffset(cls, trackingObject, screenSize, worldSize):
        """
       Calculates the offset for the camera
       """
        Drawable.WINDOW_OFFSET = Vector2(max(0,
                                   min(trackingObject.getX() + \
                                   (trackingObject.getWidth() // 2) - \
                                   (screenSize[0] // 2),
                                    worldSize[0] - screenSize[0])),
                                max(0,
                                    min(trackingObject.getY() + \
                                    (trackingObject.getHeight() // 2) - \
                                    (screenSize[1] // 2),
                                    worldSize[1] - screenSize[1])))
           
    @classmethod
    def adjustMousePos(cls, mousePos):
        """
        Given a mouse position relative to the screen coordinates, this method returns
        the mouse position adjusted to world coordinates using WINDOW_OFFSET
        """
        return Vector2(mousePos[0], mousePos[1]) + Drawable.WINDOW_OFFSET

    def __init__(self, imageName, position, offset=None, worldBound=True):
        """
        Sets up the drawable instance variables. If rect is None, then the entire
        image is used, otherwise the sub-area indicated by rect is used. If transparent
        is true, a color key is set from the pixel at position (0,0), otherwise no
        transparency key is set.
        """
        if imageName != "":
            self._imageName = imageName
            self._image = FRAMES.getFrame(self._imageName, offset)
            self._defaultImage = self._image
            self._mask = pygame.mask.from_surface(self._image)
        self._position = Vector2(position[0], position[1])
        self._worldBound = worldBound
        self._isFlipped = False
        self._collideRects = None
        self._flippedCollideRects = None
        self._isScaled = False
        self._scaleValue = 1
        self._isRotated = False
        self._rotation = 0

        # Create wrappers for getWidth and getHeight
        # to make them more consistent with pygame
        self.get_width = self.getWidth
        self.get_height = self.getHeight
       
    def getWidth(self):
        """Returns the width of the image surface"""
        return self._image.get_rect().size[0]

    def getHeight(self):
        """Returns the height of the image surface"""
        return self._image.get_rect().size[1]

    def getPosition(self):
        """Returns the current position"""
        return self._position

    def setPosition(self, newPosition):
        """Updates the position of the drawable to a new position"""
        if type(newPosition) == tuple:
            self._position = Vector2(*newPosition)
        else:
            self._position = newPosition

    def setX(self, newX):
        """Updates the x coordinate of the drawable"""
        self._position = Vector2(newX, self._position[1])

    def setY(self, newY):
        """Updates the y coordinate of the drawable"""
        self._position = Vector2(self._position[0], newY)

    def getX(self):
        """Returns the x coordinate of the current position"""
        return self._position[0]

    def getY(self):
        """Returns the y coordinate of the current position"""
        return self._position[1]

    def getSize(self):
        """Returns the size of the image surface. Returns a tuple"""
        return self._image.get_rect().size

    def getCollideRect(self):
        """Returns a Rect variable representing the collision
        area of the current object
        """
        return self._image.get_rect().move(self.getX(), self.getY())

    def getCollideRects(self):
        if self.isFlipped():
            if self._flippedCollideRects == None:
                self._flippedCollideRects = getRects(self._image)
            return self._flippedCollideRects
        else:
            if self._collideRects == None:
                self._collideRects = getRects(self._image)
            return self._collideRects

    def collidesWith(self, other):
        rects = self.getCollideRects()
        rects = moveRects(rects, self.getPosition())
        otherRects = other.getCollideRects()
        otherRects = moveRects(otherRects, other.getPosition())
        for r1 in rects:
            for r2 in otherRects:
                if r1.colliderect(r2):
                    return True
        return False

    def collidesWithPoint(self, point):
        rects = self.getCollideRects()
        rects = moveRects(rects, self.getPosition())
        for r in rects:
            if r.collidepoint(point):
                return True
        return False

    def getTrueBottom(self):
        """Returns the lowest non-transparent
        y-value of the image, ie the distance in
        pixels from the top of the image to the
        bottom of the sprite"""
        return max(self._mask.outline(), key=lambda x: x[1])[1]

    def draw(self, surface):
        """Draws the object's image at the current position on the given surface"""
        if self._worldBound:
            (x,y) = Vector2(self._position[0],self._position[1]) - Drawable.WINDOW_OFFSET
        else:
            (x,y) = self._position
        surface.blit(self._image, (x,y))

    def flip(self):
        """Flip the object's image"""
        self._isFlipped = not self._isFlipped
        self._image = pygame.transform.flip(self._image, True, False)
        self._mask = pygame.mask.from_surface(self._image)

    def isFlipped(self):
        """Returns a boolean value revealing if the object has been flipped"""
        return self._isFlipped

    def isScaled(self):
        """Returns a boolean value revealing if the object has been scaled"""
        return self._isScaled

    def scale(self,scalar):
        """
        Returns a scaled version of the image.
        """
        self._image = pygame.transform.scale(self._image,(round(scalar*self.getSize()[0]),
                                                         round(scalar*self.getSize()[1])))
        self._mask = pygame.mask.from_surface(self._image)
        self._scaleValue = scalar
        self._isScaled = True

        # Update the saved width and height of the image
        self._width  = self.getWidth()
        self._height = self.getHeight()

    def setRotation(self, angle):
        self._isRotated = True
        self._rotation = angle
        image = pygame.transform.rotate(self._defaultImage, angle)
        center = self._defaultImage.get_rect().center
        rect = image.get_rect(center=center)
        #self.setPosition(rect.topleft)
        self._image = image
        self._mask = pygame.mask.from_surface(self._image)
        
    def rotate(self, angle):
        """
        Angle is in degrees.
        """
        self._isRotated = True
        self._rotation += angle
        image = pygame.transform.rotate(self._image, angle)
        center = self._image.get_rect().center
        rect = image.get_rect(center=center)
        #self.setPosition(rect.topleft)
        self._image = image
        self._mask = pygame.mask.from_surface(self._image)
        
    def isRotated(self):
        return self._isRotated

    def getImage(self):
        """Returns the drawable's current image"""
        return self._image

    def getDefaultImage(self):
        """Returns the drawable's default / starter image"""
        return self._defaultImage

    def setWorldBound(self, boolean):
        """Determines if drawable should be fixed or world bound"""
        self._worldBound = boolean

    def makePickleSafe(self):
        """Make the drawbale object pickle safe"""
        self._image = pygame.image.tostring(self._image, "RGBA")

    def undoPickleSafe(self):
        """Return the drawable object to its original form after pickling"""
        self._image = pygame.image.fromstring(self._image,
                                              (self._width, self._height),
                                              "RGBA")

