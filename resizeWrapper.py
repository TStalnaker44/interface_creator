
import pygame

class ResizeWrapper():

    def __init__(self, widget, point, targetEdges):
        self._widget = widget
        self._initialWidth = widget.getWidth()
        self._initialHeight = widget.getHeight()
        self._initialPosition = widget.getPosition()
        self._point = point
        self._targetEdges = targetEdges

    def getWidget(self):
        return self._widget

    def getInitialWidth(self):
        return self._initialWidth

    def getInitialHeight(self):
        return self._initialHeight

    def getPoint(self):
        return self._point

    def getStartX(self):
        return self._point[0]

    def getStartY(self):
        return self._point[1]

    def getTargetEdges(self):
        return self._targetEdges

    def getInitialX(self):
        return self._initialPosition[0]

    def getInitialY(self):
        return self._initialPosition[1]

    def resize(self):
        
        x, y = pygame.mouse.get_pos()
        
        delta_x = x - self.getStartX()
        if "R" in self.getTargetEdges():
            newX = self.getInitialX()
            newWidth = self.getInitialWidth() + delta_x
        elif "L" in self.getTargetEdges():
            newX = self.getInitialX() + delta_x
            newX = min(newX, self.getInitialX()+self.getInitialWidth())
            newWidth = self.getInitialWidth() - delta_x
        else:
            newX = self.getInitialX()
            newWidth = self.getInitialWidth()

        delta_y = y - self.getStartY()
        if "B" in self.getTargetEdges():
            newY = self.getInitialY()
            newHeight = self.getInitialHeight() + delta_y
        elif "T" in self.getTargetEdges():
            newY = self.getInitialY() + delta_y
            newY = min(newY, self.getInitialY()+self.getInitialHeight())
            newHeight = self.getInitialHeight() - delta_y
        else:
            newY = self.getInitialY()
            newHeight = self.getInitialHeight()

        newHieght = max(0, newHeight)
        newWidth = max(0, newWidth)

        pos = (newX, newY)
        dims = (newWidth, newHeight)

        self.getWidget().setPosition(pos)
        self.getWidget().setDimensions(dims)

        
