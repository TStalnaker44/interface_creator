
import pygame
from polybius.abstractGame import AbstractGame
from polybius.utils.abstractPlayer import AbstractPlayer

class Sandbox(AbstractGame):

    def __init__(self):
        
        AbstractGame.__init__(self, (1000,600), "Sandbox")

        surf = pygame.Surface((100,100))
        surf.fill((255,0,0))
        movement = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        self._player = AbstractPlayer(surf, (10,10), movement)

    def draw(self, screen):
        self._player.draw(screen)

    def handleEvent(self, event):
        self._player.handleEvent(event)
        print(self._player._movement)

    def update(self, ticks):
        self._player.update(ticks, (0,0))

g = Sandbox()
g.run()
