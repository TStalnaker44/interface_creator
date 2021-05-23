
import pygame
from polybius.graphics import Drawable

##TO-DO: This still doesn't work perfectly, but for stationary game worlds, it's good

def makeDraggable(cls):

    if not issubclass(cls, Drawable):
        raise Exception("Class must inherit from Drawable or one of its subclasses")

    og_init = cls.__init__
    def newInit(self, *args, **kwargs):
        setattr(self, "_dragging", False)
        setattr(self, "_draggingOn", True)
        og_init(self, *args, **kwargs)
    cls.__init__ = newInit

    def turnDraggingOn(self):
        self._draggingOn = True
    cls.turnDraggingOn = turnDraggingOn

    def turnDraggingOff(self):
        self._draggingOn = False
    cls.turnDraggingOff = turnDraggingOff

    def isDraggingOn(self):
        return self._draggingOn
    cls.isDraggingOn = isDraggingOn
        
    def drag(self):
        previous = self._previous
        current = pygame.mouse.get_pos()
        delta_x = current[0] - previous[0]
        delta_y = current[1] - previous[1]
        self.setPosition((self.getX()+delta_x,
                          self.getY()+delta_y))
        self._previous = current
    cls.drag = drag

    og_handleEvent = cls.handleEvent
    def handleDraggingEvent(self, event, *args, **kwargs):
        og_handleEvent(self, event, *args, **kwargs)
        if self._draggingOn:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousePos = Drawable.adjustMousePos(event.pos)
                    if self.collidesWithPoint((mousePos[0], mousePos[1])):
                        self._previous = pygame.mouse.get_pos()
                        self._dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self._dragging = False
            if self._dragging:
                self.drag()
    cls.handleEvent = handleDraggingEvent

    return cls
