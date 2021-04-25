"""
Author: Trevor Stalnaker
File: imagebutton.py

TO-DO
Factor out common code between ImageButton and Button into
an abstract button class
"""

import pygame
from polybius.graphics.utils.abstractgraphic import AbstractGraphic
from polybius.utils.eventwrapper import EventWrapper
from polybius.managers.frameManager import FRAMES

class ImageButton(AbstractGraphic):

    def __init__(self, position, image, hoverImage=None,
                 pressedImage=None,
                 control=EventWrapper(pygame.MOUSEBUTTONDOWN, 1, []),
                 cursor=pygame.mouse, handOnHover=True):

        super().__init__(position)
        self._image = FRAMES.getFrame(image)

        self._standardImage = self._image
        if hoverImage == None:
            self._hoverImage = self._image
        else:
            self._hoverImage = FRAMES.getFrame(hoverImage)
        if pressedImage == None:
            self._pressedImage = self._image
        else:
            self._pressedImage = FRAMES.getFrame(pressedImage)
        
        self._press = control
        self._release = EventWrapper(self._press.getType()+1,
                                     self._press.getKey(), [])
        self._cursor = cursor

        self._handOnHover = handOnHover
        self._hover = False

    def buttonPressed(self):
        self._image = self._pressedImage

    def setToDefaultStyling(self):
        self._image = self._standardImage

    def setHover(self):
        self._image = self._hoverImage
        if self._handOnHover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def handleEvent(self, event, func, args=None, offset=(0,0)):
        if args != None and type(args) not in (tuple, list):
            args = (args,)
        #rects = self.getCollideRects()
        #rect = rect.move(offset[0],offset[1])
        if self._press.check(event):
            if self.collidesWithPoint(self._cursor.get_pos()):
            #if rect.collidepoint():
                self.buttonPressed()
                if args == None: func()
                else: func(*args)
        elif self._release.check(event):
            self.setToDefaultStyling()
            self._hover = False
        elif self.collidesWithPoint(self._cursor.get_pos()):
            if not self._hover:
                self.setHover()
                self._hover = True
        else:
            if self._hover:
                self.setToDefaultStyling()
                if self._handOnHover:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self._hover = False

    def getStandardImage(self):
        return self._standardImage

    def getHoverImage(self):
        return self._hoverImage

    def getPressedImage(self):
        return self._pressedImage
        
