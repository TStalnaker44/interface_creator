"""
Author: Justin Pusztay, Trevor Stalnaker
File: radiobutton.py

A class that creates and manages a check box object

TO DO
------
Set the text will need to update the width and the height of the
actual image when the text is changed as that changes the size.

Setting the demensions have to take that into account.
"""

import pygame
from polybius.graphics.utils.textgraphic import TextGraphic
from .multilinetextbox import MultiLineTextBox
from polybius.utils import EventWrapper, Font


class RadioButtons(TextGraphic):

    def __init__(self, position, options, radius,
                 vertical = True,
                 font = None,
                 bubbleColor = (255,255,255),
                 isSelectedIndex = -1, fontColor=(0,0,0), borderColor=(0,0,0),
                 textPadding = 5,
                 padding = 5,
                 antialias=True,
                 buttonBorderWidth = .1,
                 selectedCircleRadius = .5,
                 control=EventWrapper(pygame.MOUSEBUTTONDOWN, 1, []),
                 cursor=pygame.mouse):
        """
        isSelectedIndex is the index of the button that is selected. Inputting a -1 means there
        are no buttons currently selected. 
        """

        self._pos = position
        self._padding = padding
        font = Font("Arial",16) if font == None else font
        self._backgroundColor = None
        self._isSelectedIndex = isSelectedIndex
        super().__init__(position, "", font, fontColor, antialias)

        self._buttons = list()
        x, y = position
        for i,text in enumerate(options):
            if vertical:
                button = RadioButton((x,y),text,radius,font,bubbleColor,
                                     i == self._isSelectedIndex,
                                     fontColor,borderColor,textPadding,antialias,buttonBorderWidth,
                                     selectedCircleRadius,control,cursor)
  
                self._buttons.append(button)
                y += button.getHeight() + self._padding
            else:
                button = RadioButton((x,y),text,radius,font,bubbleColor,
                                     i == self._isSelectedIndex,
                                     fontColor,borderColor,textPadding,antialias,buttonBorderWidth,
                                     selectedCircleRadius,control,cursor)
  
                self._buttons.append(button)
                x += button.getWidth() + self._padding
                
    def draw(self,surf):
        for button in self._buttons:
            button.draw(surf)

    def handleEvent(self, event, offset=(0,0)):
        """Handles events on the check box"""
        for i,button in enumerate(self._buttons):
            button.handleEvent(event, offset)
            if button.isSelected():
                for b in self._buttons:
                    if b.isSelected() and b != button:
                        b.tickButton()         
                

class RadioButton(TextGraphic):

    def __init__(self, position, text = "", radius = 10, font = None,
                 bubbleColor=(255,255,255),
                 isSelected = False, fontColor=(0,0,0), borderColor=(0,0,0),
                 textPadding = 5,
                 antialias=True,
                 buttonBorderWidth = .1,
                 selectedCircleRadius = .5,
                 control=EventWrapper(pygame.MOUSEBUTTONDOWN, 1, []),
                 cursor=pygame.mouse):
        """
        Initializes the widget with a variety of parameters.

        The button border width is a percentage of the total radius, so to have
        it be 10% the variable should be set to 0.1

        The selected Circle radius is a percentage of the total radius so to have it
        be 50% of the larger circle it should be set to 0.5
        """

        self._pos = position
        font = Font("Arial",16) if font == None else font
        self._backgroundColor = (125,125,125)
        super().__init__(position, text, font, fontColor, antialias)

        w,h = self._font.size(text)
        self._textPadding = textPadding
        
        self._height = max(2*radius,h)
        self._width = 2*radius + w + self._textPadding
        self._radius = radius
        
        self._bubbleColor = bubbleColor
        self._borderColor = borderColor
        self._borderWidth = 0
        self._buttonBorderWidth = buttonBorderWidth
        self._selectedCircleRadius = selectedCircleRadius
        
        # Set the controls for interacting with the button
        self._press = control

        # Set the item that interacts with the button (the mouse by default)
        self._cursor = cursor

        self._defaultCheck = isSelected
        self._isSelected = isSelected

        self.updateGraphic()

    def setDimensions(self, radius):
        self._height = radius
        self._width = radius
        self.updateGraphic()

    def tickButton(self):
        """
        Checks or unchecks the check box
        """
        self._isSelected = not self._isSelected
        self.updateGraphic()
        
    def isSelected(self):
        """Returns ticked status of check box."""
        return self._isSelected
            
    def handleEvent(self, event, offset=(0,0)):
        """Handles events on the check box"""
        rect = self.getCollideRect()
        rect = rect.move(offset[0],offset[1])
        if self._press.check(event):
            if rect.collidepoint(self._cursor.get_pos()):
                if not self.isSelected():
                    self.tickButton()

    def internalUpdate(self, surf):
        """Update the button after parameters have been changed"""

        # Draws the circles
        # this is the outline circle
        pygame.draw.circle(surf,(0,0,0),(self._radius,self._radius),self._radius)
        # this is the inner non clicked circle
        pygame.draw.circle(surf,self._bubbleColor,(self._radius,self._radius),self._radius*(1-self._buttonBorderWidth))
        # draws selected circle if clicked
        if self._isSelected:
            pygame.draw.circle(surf,(12,233,89),(self._radius,self._radius),self._radius*self._selectedCircleRadius)

        # Create and draw the internal textbox
        t = MultiLineTextBox(self._text, (2*self._radius + self._textPadding,0), self._font,
                    self._fontColor, antialias=self._antialias)

        height = t.getHeight() // 2
        t.setY(self._radius - height)
        t.draw(surf)

