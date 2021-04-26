
from enum import Enum
import pygame

class BorderStyles(Enum):
    STANDARD = 1

class BorderTypes(Enum):
    LEFT   = 1
    TOP    = 2
    RIGHT  = 3
    BOTTOM = 4

class Borders():

    stringToType = {"left":BorderTypes.LEFT,
                "top":BorderTypes.TOP,
                "right":BorderTypes.RIGHT,
                "bottom":BorderTypes.BOTTOM}

    def __init__(self, widths, colors):#, styles):

        assert len(widths)==len(colors)==4#==len(styles)

        self._borders = {}
        labels = ["left","top","right","bottom"]
        for i, label in enumerate(labels):
            width = widths[i]
            color = colors[i]
            vertical = label in ("left", "right")
            borderType = Borders.stringToType[label]
            self._borders[label] = Border(width, color, vertical, borderType)

    def getBorders(self):
        return self._borders

    def getBorder(self, side):
        return self._borders[border.lower()]

    def draw(self, surf):
        for border in self._borders.values():
            border.draw(surf)

class Border():

    def __init__(self, width, color, vertical, borderType,
                 borderStyle=BorderStyles.STANDARD):
        self._width = width
        self._color = color
        self._borderType = borderType
        self._borderStyle = borderStyle
        self._vertical = vertical

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

    def draw(self, surf):
        
        if self._vertical:
            dims = (self.getWidth(), surf.get_height())
        else:
            dims = (surf.get_width(), self.getWidth())
            
        border = pygame.Surface(dims)
        border.fill(self.getColor())
        
        btype = self.getBorderType()
        if btype in (BorderTypes.LEFT, BorderTypes.TOP):
            pos = (0,0)
        elif btype == BorderTypes.RIGHT:
            x = surf.get_width() - self.getWidth()
            pos = (x,0)
        elif btype == BorderTypes.BOTTOM:
            y = surf.get_height() - self.getWidth()
            pos = (0,y)
            
        surf.blit(border, pos)
        
