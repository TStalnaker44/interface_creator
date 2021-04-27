
import pygame
from polybius.abstractGame import AbstractGame
from polybius.graphics.utils.borders import Borders

class Sandbox(AbstractGame):

    def __init__(self):
        AbstractGame.__init__(self, (1000,600), "Sandbox")
        
        self._borderSurf = pygame.Surface((400,200))
        self._borderSurf.fill((244, 244, 115))
        self._borders = Borders([4,4,4,4],
                                [(0,0,255),(0,0,0),(0,0,255),(0,0,0)],
                                ["solid","dashed","solid","dashed"])

    def draw(self, screen):
        self._borders.draw(self._borderSurf)
        screen.blit(self._borderSurf, (300, 100))
        

g = Sandbox()
g.run()
