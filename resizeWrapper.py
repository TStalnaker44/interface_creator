
class ResizeWrapper():

    def __init__(self, widget, point):
        self._widget = widget
        self._initialWidth = widget.getWidth()
        self._initialHeight = widget.getHeight()
        self._point = point

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
