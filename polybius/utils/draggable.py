
import pygame
from polybius.graphics import Drawable

class Draggable():

    def __init__(self):
        if not isinstance(self, Drawable):
            raise Exception("Class must also inherit from Drawable or one of its descendents")
        self._dragging = False
        self._draggingOn = True

    def turnDraggingOn(self):
        self._draggingOn = True

    def turnDraggingOff(self):
        self._draggingOn = False

    def isDraggingOn(self):
        return self._draggingOn
        
    def drag(self):
        previous = self._previous
        current = pygame.mouse.get_pos()
        delta_x = current[0] - previous[0]
        delta_y = current[1] - previous[1]
        self.setPosition((self.getX()+delta_x,
                          self.getY()+delta_y))
        self._previous = current

    def handleDraggingEvent(self, event):
        if self._draggingOn:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.collidesWithPoint(event.pos):
                        self._previous = pygame.mouse.get_pos()
                        self._dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self._dragging = False
            if self._dragging:
                self.drag()
        
        
        

    
