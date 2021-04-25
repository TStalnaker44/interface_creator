"""
Author: Justin Pusztay, Trevor Stalnaker
File: radiobutton.py

A class that creates and manages a check box object

TO DO
------
Set the text will need to update the width and the height of the
actual image when the text is changed as that changes the size.

Setting the dimensions have to take that into account.
"""

import pygame
from polybius.graphics.utils.textgraphic import TextGraphic
from .multilinetextbox import MultiLineTextBox
from polybius.utils import EventWrapper, Font

class RadioButtons():

    def __init__(self, position, options,
                 radius = 10,
                 vertical = True,
                 font = None,
                 bubbleColor = (255,255,255),
                 selectedIndex = -1, fontColor=(0,0,0), borderColor=(0,0,0),
                 textPadding = 5,
                 padding = 5,
                 antialias=True,
                 buttonBorderWidth = .1,
                 selectedCircleRadius = .5,
                 selectedColor = (0,0,0),
                 control=EventWrapper(pygame.MOUSEBUTTONDOWN, 1, []),
                 cursor=pygame.mouse):
        """
        selectedIndex is the index of the button that is selected. Inputting a -1 means there
        are no buttons currently selected. 
        """

        
        # Attributes for the collection of radio buttons
        self._position = position
        self._options = options
        self._padding = padding
        self._selectedIndex = selectedIndex
        self._vertical = vertical
        
        # Attributes for individual radio buttons
        self._font = Font("Arial",16) if font == None else font
        self._radius = radius
        self._bubbleColor = bubbleColor
        self._fontColor = fontColor
        self._borderColor = borderColor
        self._textPadding = textPadding
        self._antialias = antialias
        self._buttonBorderWidth = buttonBorderWidth
        self._selectedCircleRadius = selectedCircleRadius
        self._selectedColor = selectedColor
        self._control = control
        self._cursor = cursor

        self.createButtons()

    def createButtons(self):
        self._buttons = list()
        x, y = self.getPosition()
        for i,text in enumerate(self._options):
            button = RadioButton((x,y), text, self._radius,
                                 self._font, self._bubbleColor,
                                 i == self._selectedIndex,
                                 self._fontColor, self._borderColor,
                                 self._textPadding, self._antialias,
                                 self._buttonBorderWidth, self._selectedCircleRadius,
                                 self._selectedColor, self._control, self._cursor)
            self._buttons.append(button)
            if self._vertical:
                y += button.getHeight() + self._padding
            else:
                x += button.getWidth() + self._padding

    def addButton(self, buttonText):
        self._options.append(buttonText)
        self.createButtons()

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
                        
    def getFont(self):
        return self._font

    def setFont(self, font):
        self._font = font
        for b in self._buttons:
            b.setFont(font)
        self.createButtons()

    def getBubbleRadius(self, radius):
        return self._radius

    def setBubbleRadius(self, radius):
        self._raduis = radius
        for b in self._buttons:
            b.setBubbleRadius(radius)
        self.createButtons()

    def getBubbleColor(self):
        return self._bubbleColor

    def setBubbleColor(self, color):
        self._bubbleColor = color
        for b in self._buttons:
            b.setBackgroundColor(color)

    def getFontColor(self):
        return self._fontColor

    def setFontColor(self, color):
        self._fontColor = color
        for b in self._buttons:
            b.setFontColor(color)

    def getBorderColor(self):
        return self._borderColor

    def setBorderColor(self, color):
        self._borderColor = self._borderColor
        for b in self._buttons:
            b.setBorderColor(color)

    def getTextPadding(self):
        return self._textPadding

    def setTextPadding(self, padding):
        self._textPadding = padding
        for b in self._buttons:
            b.setTextPadding(padding)
        self.createButtons()

    def getButtonBorderWidth(self):
        return self._buttonBorderWidth

    def setButtonBorderWidth(self, width):
        self._buttonBorderWidth = width
        for b in self._buttons:
            b.setBorderWidth(width)

    def getSelectedCircleRadius(self):
        return self._selectedCircleRadius

    def setSelectedCircleRadius(self, radius):
        self._selectedCircleRadius = radius
        for b in self._buttons:
            b.setSelectedCircleRadius(radius)

    def getSelectedColor(self):
        return self._selectedColor

    def setSelectedColor(self, color):
        self._selectedColor = color
        for b in self._buttons:
            b.setSelectedColor(color)

    def getPosition(self):
        return self._position

    def setPosition(self, pos):
        self._position = pos

    def getOptions(self):
        return self._options

    def setOptions(self, options):
        self._options = options
        self.createButtons()

    # TO-DO: Add methods that calculate the height and width of the multisprite

class RadioButton(TextGraphic):

    def __init__(self, position, text = "", radius = 10, font = None,
                 bubbleColor=(255,255,255),
                 isSelected = False, fontColor=(0,0,0), borderColor=(0,0,0),
                 textPadding = 5,
                 antialias=True,
                 buttonBorderWidth = .1,
                 selectedCircleRadius = .5,
                 selectedColor = (0,0,0),
                 control=EventWrapper(pygame.MOUSEBUTTONDOWN, 1, []),
                 cursor=pygame.mouse):
        """
        Initializes the widget with a variety of parameters.

        The button border width is a percentage of the total radius, so to have
        it be 10% the variable should be set to 0.1

        The selected Circle radius is a percentage of the total radius so to have it
        be 50% of the larger circle it should be set to 0.5
        """

        font = Font("Arial",16) if font == None else font
        super().__init__(position, text, font, fontColor, antialias)

        # Set the initial size of the surface
        self._radius = radius
        self._textPadding = textPadding
        self.updateDimensions()

        self._backgroundColor = bubbleColor
        self._borderColor = borderColor
        self._borderWidth = buttonBorderWidth
        self._selectedCircleRadius = selectedCircleRadius
        self._selectedColor = selectedColor
        
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

    def updateGraphic(self):
        """Update the button after parameters have been changed"""

        # Create Initial Surface
        surf = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        surf.convert_alpha()
                                  
        # Draw the Circle Border                     
        pygame.draw.circle(surf,self._borderColor,(self._radius,self._radius),self._radius)
                              
        # Draw the Inner Circle
        pygame.draw.circle(surf,self._backgroundColor,(self._radius,self._radius),self._radius*(1-self._borderWidth))
                              
        # Draw the Selected Circle Icon
        if self._isSelected:
            pygame.draw.circle(surf,self._selectedColor,(self._radius,self._radius),self._radius*self._selectedCircleRadius)

        # Create and draw the internal textbox
        t = MultiLineTextBox(self._text, (2*self._radius + self._textPadding,0), self._font,
                    self._fontColor, antialias=self._antialias)

        height = t.getHeight() // 2
        t.setY(self._radius - height)
        t.draw(surf)

        self._image = surf

    def updateDimensions(self):
        w,h = self._font.size(self._text)
        self._height = max(2*self._radius,h)
        self._width = 2*self._radius + w + self._textPadding
        
    def getSelectedCircleRadius(self):
        return self._selectedCircleRadius

    def setSelectedCircleRadius(self, radius):
        self._selectedCircleRadius = radius
        self.updateGraphic()

    def getTextPadding(self):
        return self._textPadding

    def setTextPadding(self, padding):
        self._textPadding = padding
        self.updateGraphic()

    def getBubbleRadius(self):
        return self._radius

    def setBubbleRadius(self, radius):
        self._raduis = radius
        self.updateDimensions()
        self.updateGraphic()

    def getSelectedColor(self):
        return self._selectedColor

    def setSelectedColor(self, color):
        self._selectedColor = color
        self.updateGraphic()
    
        

