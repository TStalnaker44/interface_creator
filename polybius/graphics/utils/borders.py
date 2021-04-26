
from enum import Enum

class BorderTypes(Enum):
    STANDARD = 1
    
class Borders():

    def __init__(self, widths, colors):#, types):

        assert len(widths)==len(colors)==4#==len(types)

        self._borders = {}
        labels = ["left","top","right","bottom"]
        for label in labels:
            width = widths[i]
            color = colors[i]
            self._borders[label] = Border(width, color)

    def getBorders(self):
        return self._borders

    def getBorder(self, side):
        return self._borders[border.lower()]
            

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
        
