"""
Author: Trevor Stalnaker
File: slider.py

A class that models a slider bar.
"""
import pygame
from polybius.graphics.utils.abstractgraphic import AbstractGraphic
from polybius.graphics import Panel
from polybius.utils import EventWrapper

class Slider(AbstractGraphic):

    def __init__(self, position, defaultValue=50, minValue=0, maxValue=100,
                 railDimensions=(100,5), railColor=(120,120,120),
                 handleColor=(60,60,60), handleDimensions=(6,15)):
        AbstractGraphic.__init__(self, position)
        self._value = defaultValue
        self._minValue = minValue
        self._maxValue = maxValue
        self._railDims = railDimensions
        self._handleDims = handleDimensions
        self._width = railDimensions[0] + handleDimensions[0]
        self._height = max(railDimensions[1], handleDimensions[1])
        self._railColor = railColor
        self._backgroundColor = None
        self._borderWidth = 0
        self._borderColor = (0,0,0)

        handleX = ((defaultValue - minValue) / (maxValue - minValue)) * railDimensions[0]
        self._handle = Panel((handleX,0), (5,15), handleColor, borderWidth=1)

        self._mouseDown = EventWrapper(pygame.MOUSEBUTTONDOWN, 1)
        self._mouseUp = EventWrapper(pygame.MOUSEBUTTONUP, 1)
        self._onClickPosition = None
        self._dragging = False
        
        self.updateGraphic()

    def calculateValue(self):
        x = self._handle.getX()
        railLength = self._railDims[0]
        self._value = ((x / railLength) * (self._maxValue - self._minValue)) + self._minValue

    def getValue(self):
        return self._value

    def setValue(self, value):
        handleX = ((value - self._minValue) / (self._maxValue - self._minValue)) * self._railDims[0]
        self._handle.setX(handleX)
        self.updateGraphic()
        self._value = value

    def getMinValue(self):
        return self._minValue

    def getMaxValue(self):
        return self._maxValue

    def handleEvent(self, event):
        if self._mouseDown.check(event):
            x,y = event.pos
            eventPos = (x-self.getX(), y-self.getY())
            if self._handle.getCollideRect().collidepoint(eventPos):
                self._onClickPosition = pygame.mouse.get_pos()
                self._dragging = True
        if self._onClickPosition != None and self._mouseUp.check(event):
            self._dragging = False
            self._onClickPosition = None

        if self._dragging:
            previous = self._onClickPosition
            current = pygame.mouse.get_pos()
            delta_x = current[0] - previous[0]
            self._onClickPosition = current
            newX = min(max(0, self._handle.getX() + delta_x), self._width-self._handle.getWidth()-1)
            self._handle.setPosition((newX, self._handle.getY()))
            self.calculateValue()
            self.updateGraphic()

    def internalUpdate(self, surf):
        rail = pygame.Surface(self._railDims)
        rail.fill(self._railColor)
        x_pos = self._handleDims[0] // 2
        y_pos = (self._handleDims[1] // 2) - (self._railDims[1]//2)
        surf.blit(rail, (x_pos, y_pos))
        self._handle.draw(surf)
