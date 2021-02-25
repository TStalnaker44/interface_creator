
import pygame
from polybius.abstractGame import AbstractGame
from polybius.graphics import Button

class Game(AbstractGame):

    def __init__(self):
        AbstractGame.__init__(self, (500,500), "New Game")
        self.getScreen().fill((255,0,0))

        self._font = pygame.font.SysFont("Times New Roman", 20)
        
        self._buttons = []
        self._dragging = None

        self._testMode = False
    
    def draw(self, screen):
        self.getScreen().fill((255,0,0))
        for b in self._buttons:
            b.draw(screen)

    def handleEvent(self, event):
        if self._testMode:
            for b in self._buttons:
                b.handleEvent(event, self.doNothing)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and \
               event.button == 3:
                self.makeButton(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and \
               event.button == 1:
                for b in self._buttons:
                    if b.getCollideRect().collidepoint(event.pos):
                        self._dragging = (b, event.pos)
                        
    def update(self, ticks):
        self.updateElementDragging()
            
    def doNothing(self):
        pass

    def updateElementDragging(self):
        if self._dragging != None:
            b, previous = self._dragging
            current = pygame.mouse.get_pos()
            delta_x = current[0] - previous[0]
            delta_y = current[1] - previous[1]
            b.setPosition((b.getX()+delta_x,
                          b.getY()+delta_y))
            self._dragging = (b, current)
            if not pygame.mouse.get_pressed()[0]:
                self._dragging = None
                
    def makeButton(self, pos):
        b = Button("Press Me", pos, self._font, (0,0,0),
                              (100,120,80), 20, 100)
        self._buttons.append(b)

g = Game()
g.run()
