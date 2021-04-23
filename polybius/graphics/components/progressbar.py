"""
Author: Trevor Stalnaker
File: progressbar.py

A GUI widget that can be used to model progress bars or health bars
"""

import pygame
from polybius.graphics.utils.abstractgraphic import AbstractGraphic

class ProgressBar(AbstractGraphic):

    def __init__(self, position, length, maxStat, actStat, borderWidth=1,
                 borderColor=(0,0,0), backgroundColor=(120,120,120),
                 barColor=(255,0,0), height=10, alignment="left"):
        """Initializes the widget with a variety of parameters"""
        super().__init__(position)
        self._width = length
        self._height = height
        self._maxStat = maxStat
        self._actStat = actStat
        self._borderWidth = borderWidth
        self._borderColor = borderColor
        self._backgroundColor = backgroundColor
        self._barColor = barColor
        assert alignment.lower() in ("left","center","right")
        self._alignment = alignment.lower()
        self.updateGraphic()

    def getBarColor(self):
        return self._barColor

    def setBarColor(self, color):
        self._barColor = color
        self.updateGraphic()

    def getAlignment(self):
        return self._alignment

    def setAlignment(self, align):
        self._alignment = align
        self.updateGraphic()

    def getMaxStat(self):
        return self._maxStat

    def setMaxStat(self, stat):
        self._maxStat = stat
        self.updateGraphic()

    def getActiveStat(self):
        return self._actStat

    def setActiveStat(self, stat):
        self._actStat = stat
        self.updateGraphic()

    def getLength(self):
        return self._width

    def setLength(self, l):
        self._width = l
        self.updateGraphic()

    def getHeight(self):
        return self._height
    
    def setHeight(self, height):
        self._height = height
        self.updateGraphic()

    def setProgress(self, actStat):
        """Sets the current progress of the bar based on an active stat"""
        self._actStat = actStat
        self.updateGraphic()

    def changeProgress(self, amount):
        """Changes the progess of the bar by a given amount"""
        if 0 < self._actStat + amount <= self._maxStat: 
            self._actStat += amount
            self.updateGraphic()

    def setDimensions(self, dims):
        self._width = dims[0]
        self._height = dims[1]
        self.updateGraphic()

    def internalUpdate(self, surf):
        
        barLength = round((self._actStat / self._maxStat) * \
                          (self._width - self._borderWidth*2))
        barDims = (barLength,self._height-self._borderWidth*2)

        # Create a surface to draw the bar to
        barSurf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        barSurf.convert_alpha()

        # This surface is used to map the transparencies
        mask = surf.copy()
        pxa = pygame.PixelArray(mask)
        pxa.replace(self._backgroundColor, (255,255,255))
        mask = pxa.make_surface()
        
        if self._alignment == "left": 
            pos = (0,0)     
        elif self._alignment == "center":
            x = surf.get_width() // 2 - barLength // 2
            pos = (x,0)   
        elif self._alignment == "right":
            x = surf.get_width() - barLength
            pos = (x, 0)

        rect = pygame.Rect(pos, barDims)
        pygame.draw.rect(barSurf, self._barColor, rect)
        barSurf.blit(mask, (0,0), None, pygame.BLEND_RGBA_MULT)
        surf.blit(barSurf, (0,0))
        
