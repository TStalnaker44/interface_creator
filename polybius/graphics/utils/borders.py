
from enum import Enum
import pygame

class BorderTypes(Enum):
    STANDARD = 1
    
class Borders():

    def __init__(self, widths, colors):#, types):

        assert len(widths)==len(colors)==4#==len(types)

        self._borders = {}
        labels = ["left","top","right","bottom"]
        for i, label in enumerate(labels):
            width = widths[i]
            color = colors[i]
            self._borders[label] = Border(width, color)

    def getBorders(self):
        return self._borders

    def getBorder(self, side):
        return self._borders[border.lower()]

    def draw(self, surf):

        width = surf.get_width()
        height = surf.get_height()

        # Calculate the centers to draw lines around
        leftEdge = (self._borders["left"].getWidth()//2)
        if leftEdge % 2 == 0: leftEdge -= 1
        topEdge = (self._borders["top"].getWidth()//2)
        if topEdge % 2 == 0: topEdge -= 1
        rightEdge = width - ((self._borders["right"].getWidth()//2)+1)
        bottomEdge = height - ((self._borders["bottom"].getWidth()//2)+1)

        coords = {"top":[(0,topEdge),(width,topEdge)],
                  "right":[(rightEdge,0),(rightEdge,height)],
                  "bottom":[(width,bottomEdge),(0,bottomEdge)],
                  "left":[(leftEdge,height),(leftEdge,0)]}

        for label, border in self._borders.items():
            startPos, endPos = coords[label]
            border.draw(surf, startPos, endPos)

class Border():

    def __init__(self, width, color, borderType=BorderTypes.STANDARD):
        self._width = width
        self._color = color
        self._borderType = borderType

    def getWidth(self):
        return self._width

    def setWidth(self, width):
        self._width = width

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color

    def getBorderType(self):
        return self._borderType

    def setBorderType(self, borderType):
        self._borderType = borderType

    def draw(self, surf, startPos, endPos):
        pygame.draw.line(surf, self.getColor(),
                         startPos, endPos, self.getWidth())
        
