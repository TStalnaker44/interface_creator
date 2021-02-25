
import pygame
from polybius.abstractGame import AbstractGame
from polybius.graphics import Button

class Game(AbstractGame):

    def __init__(self):
        AbstractGame.__init__(self, (500,500), "New Game")
        self.getScreen().fill((255,0,0))

        font = pygame.font.SysFont("Times New Roman", 20)
        self._button = Button("Press Me", (100,100), font, (0,0,0),
                              (100,120,80), 20, 100)

        self._time = 0
        
    def draw(self, screen):
        self.getScreen().fill((255,0,0))
        self._button.draw(screen)

    def handleEvent(self, event):
        self._button.handleEvent(event, self.doNothing)

    def update(self, ticks):
        self._time += ticks

    def doNothing(self):
        print(self._time)

g = Game()
g.run()
