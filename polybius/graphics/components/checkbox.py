"""
Author: Trevor Stalnaker, Justin Pusztay
File: checkbox.py

A class that creates and manages a check box object
"""

import pygame
from polybius.graphics.utils.textgraphic import TextGraphic
from .multilinetextbox import MultiLineTextBox
from polybius.utils import EventWrapper, Font

class Checkbox(TextGraphic):

    def __init__(self, position, font = None, symbol = 'X', backgroundColor=(255,255,255),
                 isChecked = False, fontColor=(0,0,0), borderColor=(0,0,0),
                 borderWidth=1, antialias=True,
                 control=EventWrapper(pygame.MOUSEBUTTONDOWN, 1, []),
                 cursor=pygame.mouse, dims=(20,20)):
        """Initializes the widget with a variety of parameters"""

        text = symbol if isChecked else ""
        font = Font("Arial",16) if font == None else font
        super().__init__(position, text, font, fontColor, antialias)

        self._symbol = symbol
        
        self._dims = dims
        self._width = dims[0]
        self._height = dims[1]
        
        self._backgroundColor = backgroundColor
        self._borderColor = borderColor
        self._borderWidth = borderWidth

        # Set the controls for interacting with the button
        self._press = control

        # Set the item that interacts with the button (the mouse by default)
        self._cursor = cursor

        self._defaultCheck = isChecked
        self._isChecked = isChecked

        self.updateGraphic()

    def setDimensions(self, dims):
        self._width = dims[0]
        self._height = dims[1]
        self.updateGraphic()

    def tickCheckbox(self):
        """
        Checks or unchecks the check box
        """
        if self.isChecked():
            self._text = ""
        else:
            self._text = self._symbol
        self._isChecked = not self._isChecked
        self.updateGraphic()
            
    def isChecked(self):
        """Returns ticked status of check box."""
        return self._isChecked

    def handleEvent(self, event, offset=(0,0)):
        """Handles events on the check box"""
        rect = self.getCollideRect()
        rect = rect.move(offset[0],offset[1])
        if self._press.check(event):
            if rect.collidepoint(self._cursor.get_pos()):
                self.tickCheckbox()
            

    def internalUpdate(self, surf):
        """Update the button after parameters have been changed"""

        # Use the current background color
        surf.fill(self._backgroundColor)

        # Create and draw the internal textbox
        t = MultiLineTextBox(self._text, (0,0), self._font,
                    self._fontColor, antialias=self._antialias)
        t.center(surf)
        t.draw(surf)

