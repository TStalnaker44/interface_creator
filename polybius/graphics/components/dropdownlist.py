"""
Author: Justin Pusztay, Trevor Stalnaker
File: dropdownlist.py

A class that creates and manages a check box object

TO DO
------
Set the text will need to update the width and the height of the
actual image when the text is changed as that changes the size.

Setting the dimensions have to take that into account.
"""

import pygame
from polybius.graphics.utils.textgraphic import TextGraphic
from polybius.utils import EventWrapper, Font
from .button import Button
from polybius.utils.vector2D import Vector2

class DropDownList():

    def __init__(self, position, options,
                 font = None,
                 backgroundColor = (255,255,255),
                 selectedIndex = 0, fontColor=(0,0,0), borderColor=(0,0,0),
                 antialias=True,
                 buttonBorderWidth = 1,
                 selectedColor = (0,0,0),
                 control=EventWrapper(pygame.MOUSEBUTTONDOWN, 1, []),
                 cursor=pygame.mouse):

        self._position = position
        self._options = options
        self._selectedIndex = selectedIndex
        
        # Attributes for individual selection buttons
        self._font = Font("Arial",16) if font == None else font
        self._backgroundColor = backgroundColor
        self._fontColor = fontColor
        self._borderColor = borderColor

        self._antialias = antialias
        self._buttonBorderWidth = buttonBorderWidth
        self._selectedColor = selectedColor
        self._control = control
        self._cursor = cursor # when putting this in create buttons it breaks

        self._isClicked = False

        self.createButtons()

    def createButtons(self):
        longestOption = max(self._options, key=len)
        dims = Vector2(*self._font.size(longestOption)) + Vector2(7,0) # magic number
        self._header = Button(self._options[self.getSelectedIndex()],
                              self._position,self._font,self._backgroundColor,
                              (0,0),self._fontColor,self._borderColor,
                                self._buttonBorderWidth,
                                self._antialias,self._control,self._cursor,
                              dims = dims)

        x = self.getPosition()[0] + self._header.getWidth()
        y = self.getPosition()[1] 
        
        self._downArrow = Button("v",
                      (x,y),self._font,self._backgroundColor,
                      (5,0),self._fontColor,self._borderColor, # magic number
                        self._buttonBorderWidth,
                        self._antialias,self._control,self._cursor)

        self._buttons = list()
        x = self.getPosition()[0]
        y = self.getPosition()[1] + self._header.getHeight()

        dims = dims + Vector2(self._downArrow.getWidth(),0)

        for i,text in enumerate(self._options):
            button = Button(text,(x,y),self._font,self._backgroundColor,
                            (0,0),self._fontColor,self._borderColor,
                            self._buttonBorderWidth,
                            self._antialias,self._control,self._cursor,
                            dims=dims)
            self._buttons.append(button)

            y += button.getHeight()

    def draw(self,surf):
        self._header.draw(surf)
        self._downArrow.draw(surf)
        if self._isClicked:
            for button in self._buttons:
                button.draw(surf)

    def handleEvent(self, event):
        self._header.handleEvent(event, self.toggleMenu)
        self._downArrow.handleEvent(event, self.toggleMenu)
        if self._isClicked:
            for b in self._buttons:
                b.handleEvent(event, self._changeHeader, args=(b.getText(),))

    def toggleMenu(self):
        self._isClicked = not self._isClicked

    def setSelection(self, option):
        self._header.setText(option)

    def _changeHeader(self, option):
        self.setSelection(option)
        self._isClicked = False

    def getSelection(self):
        return self._header.getText()

    def getPosition(self):
        return self._position

    def getSelectedIndex(self):
        return self._selectedIndex

            
        
