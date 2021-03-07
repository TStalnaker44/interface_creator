"""
Author: Trevor Stalnaker
File: textinput.py

A class that creates and manages textual input boxes
"""

from polybius.graphics.utils.abstractgraphic import AbstractGraphic
from polybius.utils import Timer, EventWrapper
from .textbox import TextBox
import pygame, string



class TextInput(AbstractGraphic):

    def __init__(self, position, font, dimensions, color=(0,0,0),
                 borderWidth=2, backgroundColor=(255,255,255),
                 borderColor=(0,0,0), borderHighlight=(100,100,200),
                 backgroundHighlight=(225,225,255), maxLen=10,
                 numerical=False, highlightColor=(0,0,0), defaultText="",
                 clearOnActive=False, allowNegative=False, antialias=True,
                 allowSymbols=False):
        """Initializes the widget with a variety of parameters"""
        super().__init__(position)
        self._width = dimensions[0]
        self._height = dimensions[1]
        self._defaultBorderWidth = borderWidth
        self._defaultBorderColor = borderColor
        self._borderHighlight = borderHighlight
        self._defaultBackgroundColor = backgroundColor
        self._backgroundHighlight = backgroundHighlight
        self._backgroundColor = backgroundColor
        self._font = font
        self._textbox = TextBox(defaultText,(0,0),font,color,antialias)
        self._maxLen = maxLen
        self._active = False
        self._clearOnActive = clearOnActive
        self._numerical = numerical
        self._allowNegative = allowNegative
        self._borderColor = self._defaultBorderColor
        self._borderWidth = borderWidth
        self._color = color
        self._highlightColor = highlightColor
        self._antialias = antialias
        self._allowSymbols = allowSymbols
        
        self._pointer = 0
        self._cursorTimer = Timer(.5)
        self._displayCursor = False

        self._ki = KeyIdentifier()

        self.updateGraphic()

    def isActive(self):
        return self._active

    def displayActive(self):
        """Sets the display mode to active"""
        self._borderColor = self._borderHighlight
        self._borderWidth = self._defaultBorderWidth + 1
        self._backgroundColor = self._backgroundHighlight
        self._textbox.setFontColor(self._highlightColor)
        if self._clearOnActive:
            self._textbox.setText("")
            self._pointer = 0
        self.updateGraphic()

    def displayPassive(self):
        """Sets the display mode to passive"""
        self._borderColor = self._defaultBorderColor
        self._borderWidth = self._defaultBorderWidth
        self._backgroundColor = self._defaultBackgroundColor
        self._textbox.setFontColor(self._color)
        self.updateGraphic()

    def _makeActive(self, text):
        self._active = True
        self._pointer = len(text)
        self.displayActive()

    def _makeInActive(self):
        self._active = False
        self.displayPassive()
        
    def handleEvent(self, event, *args, offset=(0,0), func=None,
                    clearOnEnter=False):
        """Handle events on the text input"""
        text = self._textbox.getText()
        rect = self.getCollideRect()
        rect = rect.move(offset[0], offset[1])
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            if rect.collidepoint(event.pos):
                self._makeActive(text)
            else:
                self._makeInActive()
                         
        elif event.type == pygame.KEYDOWN and self._active:

            # Check if backspace was pressed
            if event.key == 8:
                newText = text[:self._pointer-1] + text[self._pointer:]
                self._textbox.setText(newText)
                self._pointer = max(0,self._pointer - 1)

            # Move the input cursor left and right
            if event.key == pygame.K_RIGHT:
                self._pointer = min(len(text), self._pointer+1)
            if event.key == pygame.K_LEFT:
                self._pointer = max(0, self._pointer-1)
            
            if len(text) < self._maxLen: 
                newChar = self._ki.getChar(event)
                if self._numerical:
                    if not newChar.isnumeric():
                        if (not newChar == "-") or not self._allowNegative:
                            newChar = ""
                elif not self._allowSymbols:
                    if newChar in string.punctuation:
                        newChar = ""                   
                if newChar != "":
                    newText = text[:self._pointer] + newChar + text[self._pointer:]
                    self._textbox.setText(newText)
                    self._pointer += 1
                     
            # Check if the enter key was pressed
            if event.key == 13 or event.key == pygame.K_KP_ENTER:
                self._active = False
                self.displayPassive()
                if func != None:
                    func(*args)
                if clearOnEnter:
                    self._textbox.setText("")
                    self._pointer = 0
            self.updateGraphic()
        
    def getInput(self):
        """Get the current input text"""
        return self._textbox.getText()

    def setText(self, text):
        """Set the text displayed in the input bar"""
        self._textbox.setText(text)
        self._pointer = len(text)
        self.updateGraphic()

    def getFont(self):
        return self._font

    def getFontColor(self):
        return self._color

    def getBorderColor(self):
        return self._defaultBorderColor

    def getBorderWidth(self):
        return self._defaultBorderWidth

    def getBackgroundColor(self):
        return self._defaultBackgroundColor

    def setFontColor(self, color):
        self._color = color
        self._textbox.setFontColor(color)
        self.updateGraphic()

    def setFont(self, font):
        self._font = font
        self._textbox.setFont(font)
        self.updateGraphic()

    def setBackgroundColor(self, color):
        self._defaultBackgroundColor = color
        self._backgroundColor = color
        self.updateGraphic()

    def setBorderColor(self, color):
        self._defaultBorderColor = color
        self._borderColor = color
        self.updateGraphic()

    def setBorderWidth(self, width):
        self._defaultBorderWidth = width
        self._borderWidth = width
        self.updateGraphic()

    def setBorderHighlight(self, color):
        self._borderHighlight = color

    def setBackgroundHighlight(self, color):
        self._backgroundHighlight = color

    def setDimensions(self, dims):
        self._width = dims[0]
        self._height = dims[1]
        self.updateGraphic()

    def update(self, ticks):
        self._cursorTimer.update(ticks, self.toggleCursor)

    def toggleCursor(self):
        self._displayCursor = not self._displayCursor
        self.updateGraphic()

    def getPixelWidth(self, text):
        font = self._font
        width, height = font.size(text)
        return width

    def calculateCursorPosition(self):
        top = self._textbox.getY()
        bottom = top + self._textbox.getHeight() - 4
        text = self._textbox.getText()[:self._pointer]
        x_pos = self._textbox.getX() + self.getPixelWidth(text)
        return ((x_pos, top),(x_pos, bottom))

##    def calculatePointerPlacement(self, eventPos, rect):
##        print("hello")
##        eventx = eventPos[0]
##        basex = rect.x
##        text = self._textbox.getText()
##        tbWidth = self._textbox.getWidth()
##        checkedValues = []
##        minPlacement = 0
##        maxPlacement = len(text)
##        while True:
##            pointer = (minPlacement + maxPlacement) // 2
##            normalx = basex + self.getPixelWidth(text[:pointer])
##            pointerx = (basex + tbWidth)//2 - (normalx // 2)
##            print(pointer)
##            print("Px:", pointerx)
##            print("Ex:",eventx)
##            if eventx < pointerx:
##                maxPlacement = pointer
##            elif eventx > pointerx:
##                minPlacement = pointer
##            else:
##                self._pointer = pointer
##                print("here")
##                break
##            if pointer in checkedValues:
##                self._pointer = pointer
##                break
####                # Find the closest pointer (one to the left and right of optimal)
####                distances = [abs(self.findPointerXCoordinate(p, basex, text)-eventx)
####                  for p in range(pointer-1, pointer+2)]
####                minimum = min(distances)
####                self._pointer = (pointer-1) + distances.index(minimum)
####                "print woah"
####                break
##            checkedValues.append(pointer)

##    def findPointerXCoordinate(self, pointer, basex, text):
##        return basex + self.getPixelWidth(text[:pointer-1])

    def internalUpdate(self, surf):
        """Update the widget's display"""
        self._textbox.center(surf, (1/2,1/2))
        self._textbox.draw(surf)
        if self._displayCursor and self._active:
            top, bottom = self.calculateCursorPosition()
            pygame.draw.line(surf, (0,0,0), top, bottom)

class KeyIdentifier():

    #TO-DO: Caps Lock and Num Lock checks do no work quite right

    def __init__(self):

        self._numSymbols = ")!@#$%^&*("

        self._symbolKeys = [ord(p) for p in string.punctuation]

        self._symbols = {EventWrapper(pygame.KEYDOWN, i+48, [pygame.KMOD_SHIFT]):s
                           for i, s in enumerate(")!@#$%^&*(")}

        for x in range(10):
            self._symbols[EventWrapper(pygame.KEYDOWN, x+48)] = str(x)
            self._symbols[EventWrapper(pygame.KEYDOWN, x+256,
                                       [pygame.KMOD_NUM])] = str(x)

        for x in range(27):
            self._symbols[EventWrapper(pygame.KEYDOWN, x+97)] = chr(x+97)
            self._symbols[EventWrapper(pygame.KEYDOWN, x+97, [pygame.KMOD_SHIFT])] = chr(x+65)
            self._symbols[EventWrapper(pygame.KEYDOWN, x+97, [pygame.KMOD_CAPS])] = chr(x+65)
            
        self._symbols[EventWrapper(pygame.KEYDOWN, 91)] = "["
        self._symbols[EventWrapper(pygame.KEYDOWN, 92)] = "\\"
        self._symbols[EventWrapper(pygame.KEYDOWN, 93)] = "]"
        
        self._symbols[EventWrapper(pygame.KEYDOWN, 44)] = ","
        self._symbols[EventWrapper(pygame.KEYDOWN, 46)] = "."
        self._symbols[EventWrapper(pygame.KEYDOWN, 47)] = "/"
        self._symbols[EventWrapper(pygame.KEYDOWN, 59)] = ";"
        self._symbols[EventWrapper(pygame.KEYDOWN, 39)] = "'"
        self._symbols[EventWrapper(pygame.KEYDOWN, 96)] = "`"
        self._symbols[EventWrapper(pygame.KEYDOWN, 61)] = "="
        self._symbols[EventWrapper(pygame.KEYDOWN, 45)] = "-"
        
        self._symbols[EventWrapper(pygame.KEYDOWN, 44, [pygame.KMOD_SHIFT])] = "<"
        self._symbols[EventWrapper(pygame.KEYDOWN, 46, [pygame.KMOD_SHIFT])] = ">"
        self._symbols[EventWrapper(pygame.KEYDOWN, 47, [pygame.KMOD_SHIFT])] = "?"
        self._symbols[EventWrapper(pygame.KEYDOWN, 91, [pygame.KMOD_SHIFT])] = "{"
        self._symbols[EventWrapper(pygame.KEYDOWN, 93, [pygame.KMOD_SHIFT])] = "}"
        self._symbols[EventWrapper(pygame.KEYDOWN, 61, [pygame.KMOD_SHIFT])] = "+"
        self._symbols[EventWrapper(pygame.KEYDOWN, 96, [pygame.KMOD_SHIFT])] = "~"
        self._symbols[EventWrapper(pygame.KEYDOWN, 92, [pygame.KMOD_SHIFT])] = "|"
        self._symbols[EventWrapper(pygame.KEYDOWN, 39, [pygame.KMOD_SHIFT])] = '"'
        self._symbols[EventWrapper(pygame.KEYDOWN, 59, [pygame.KMOD_SHIFT])] = ":"
        self._symbols[EventWrapper(pygame.KEYDOWN, 45, [pygame.KMOD_SHIFT])] = "_"

        self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_KP_PLUS)] = "+"
        self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_KP_MINUS)] = "-"
        self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_KP_DIVIDE)] = "/"
        self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_KP_MULTIPLY)] = "*"
        self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_KP_PERIOD)] = "."
        self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_SPACE)] = " "

        self._wrappers = [w for w in self._symbols.keys()]
        self._wrappers.sort(key=lambda x: len(x.getMods()))
        self._wrappers.reverse()

    def getChar(self, event):     
        for wrapper in self._wrappers:
            if wrapper.check(event):
                print(self._symbols[wrapper])
                return self._symbols[wrapper]
        return ""
        
