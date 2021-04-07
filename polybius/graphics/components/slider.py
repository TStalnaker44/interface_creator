
import pygame
from polybius.graphics.utils.abstractgraphic import AbstractGraphic
from polybius.graphics import Panel
from polybius.utils import EventWrapper

class Slider(AbstractGraphic):

    def __init__(self, position, defaultValue=50, minValue=0, maxValue=100,
                 railDimensions=(100,5), railColor=(120,120,120),
                 handleColor=(60,60,60), handleDimensions=(5,15)):
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
        self._handle = Panel((defaultValue,0), (5,15), handleColor, borderWidth=1)

        self._mouseDown = EventWrapper(pygame.MOUSEBUTTONDOWN,1)
        
        self.updateGraphic()

    def getValue(self):
        return self._value

    def setValue(self, value):
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
                print("wooo hoooo hoooo")

##    def draw(self, screen):
##        super().draw(screen)
##        self._handle.draw(screen)

    def internalUpdate(self, surf):
        rail = pygame.Surface(self._railDims)
        rail.fill(self._railColor)
        x_pos = self._handleDims[0] // 2
        y_pos = (self._handleDims[1] // 2) - (self._railDims[1]//2)
        surf.blit(rail, (x_pos, y_pos))
        self._handle.draw(surf)
