
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

    def __init__(self, widths, colors, styles):

        assert len(widths)==len(colors)==4==len(styles)

        self._borders = {}
        labels = ["left","top","right","bottom"]
        for i, label in enumerate(labels):
            width = widths[i]
            color = colors[i]
            vertical = label in ("left", "right")
            borderType = Borders.stringToType[label]
            borderStyle = styles[i]
            self._borders[label] = Border(width, color, vertical,
                                          borderType, borderStyle)

    def getBorders(self):
        return self._borders

    def getBorder(self, side):
        return self._borders[side.lower()]

    def draw(self, surf):

        width = surf.get_width()
        height = surf.get_height()

        # Get Borders
        top = self.getBorder("top")
        bottom = self.getBorder("bottom")
        left = self.getBorder("left")
        right = self.getBorder("right")

        # Top Line
        points = [(0,0), (width,0),
                  (width-right.getWidth(), top.getWidth()),
                  (left.getWidth(), top.getWidth())]
        top.draw(surf, points)

        # Bottom Line
        points = [(left.getWidth(),height - bottom.getWidth()),
                  (width-right.getWidth(), height - bottom.getWidth()),
                  (width, height),
                  (0,height)]
        bottom.draw(surf, points)

        # Left Line
        points = [(0,0),
                  (left.getWidth(),top.getWidth()),
                  (left.getWidth(), height-bottom.getWidth()),
                  (0, height)]
        left.draw(surf, points)

        # Right Line
        points = [(width-right.getWidth(), top.getWidth()),
                  (width,0),
                  (width,height),
                  (width-right.getWidth(), height-bottom.getWidth())]
        right.draw(surf, points)

class Border():

    def __init__(self, width, color, vertical, borderType,
                 borderStyle="dashed"):
        self._width = width
        self._color = color
        self._borderType = borderType
        self._borderStyle = borderStyle.lower()
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

    def getBorderStyle(self):
        return self._borderStyle

    def setBorderStyle(self, style):
        self._borderStyle = style.lower()

    def draw(self, surf, points):
        if self.getBorderStyle() == "solid":
            pygame.draw.polygon(surf, self.getColor(), points)
        elif self.getBorderStyle() == "dashed":
            self._drawSegments(surf, points)
        elif self.getBorderStyle() == "double":
            self._drawDouble(surf, points)
        elif self.getBorderStyle() == "dotted":
            pass

    def _drawSegments(self, surf, points):
        #TO-DO Improve border join meetings
        if self._vertical:
            span = surf.get_height()
        else:
            span = surf.get_width()
        dash_unit = 4
        dashes = (span + dash_unit) // (3 * dash_unit)
        shiftAmount = (abs(span - (dashes * dash_unit * 3)) // 2)-1
        if self._vertical:
            s = pygame.Surface((self.getWidth(),2*dash_unit))
            s.fill(self.getColor())
            if self.getBorderType() == BorderTypes.LEFT:
                x = 0
            else:
                x = surf.get_width() - self.getWidth()
            for y in range(0, span, dash_unit*3):
                surf.blit(s, (x,y-shiftAmount))
        else:
            s = pygame.Surface((2*dash_unit,self.getWidth()))
            s.fill(self.getColor())
            if self.getBorderType() == BorderTypes.TOP:
                y = 0
            else:
                y = surf.get_height() - self.getWidth()
            for x in range(0, span, dash_unit*3):
                surf.blit(s, (x-shiftAmount,y))

    def _drawDouble(self, surf, points):
        height = surf.get_height()
        width = surf.get_height()
        ul,ur,br,bl = points
        if self._vertical:
            q1X = (ur[0]-ul[0])//4
            q3X = (3 * (ur[0]-ul[0]))//4
            q1Y = (ur[1]-ul[1])//4
            q3Y = (3 * (ur[1]-ul[1]))//4
            if self.getBorderType() == BorderTypes.LEFT:
                firstPoints = [ul,
                               (q1X,q1Y),
                               (q1X, height - q1Y),
                               bl]
                secondPoints = [(q3X,q3Y),
                                ur,
                                (br[0],height-q3Y),
                                (q3X, br[1])]
            else:
                firstPoints = [ul,
                               (ul[0]+q1X,ul[1]+q1Y),
                               (ul[0]+q1X, bl[1]-q1Y),
                               bl]
                secondPoints = [(ul[0]+q3X,ul[1]+q3Y),
                                ur,
                                br,
                                (ul[0]+q3X, bl[1]-q3Y)]
        else:
            q1X = (bl[0]-ul[0])//4
            q3X = (3 * (bl[0]-ul[0]))//4
            q1Y = (bl[1]-ul[1])//4
            q3Y = (3 * (bl[1]-ul[1]))//4
            if self.getBorderType() == BorderTypes.TOP:
                
                firstPoints = [ul,ur,
                               (ur[0]-q1X, ur[1]+q1Y),
                               (q1X, ur[1]+q1Y)]
                secondPoints = [(q3X, ur[1]+q3Y),
                                (ur[0]-q3X-1, ur[1]+q3Y),
                                br,bl]
            else:

                firstPoints = [ul,ur,
                               (ur[0]-q1X, ur[1]+q1Y),
                               (q1X, ur[1]+q1Y)]
                secondPoints = [(q3X, ur[1]+q3Y),
                                (ur[0]-q3X, ur[1]+q3Y),
                                br,bl]
                
        pygame.draw.polygon(surf, self.getColor(), firstPoints)
        pygame.draw.polygon(surf, self.getColor(), secondPoints)
            
      
