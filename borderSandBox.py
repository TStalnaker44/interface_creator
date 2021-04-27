
import pygame
from polybius.abstractGame import AbstractGame
from polybius.graphics.utils.borders import Borders

class Sandbox(AbstractGame):

    def __init__(self):
        AbstractGame.__init__(self, (1000,600), "Sandbox")
        
        self._borderSurf = pygame.Surface((400,200))
        self._borderSurf.fill((244, 244, 115))
        self._borders = Borders([10,10,10,8],
                                [(0,0,0),(0,0,0),(0,0,0),(0,0,0)],
                                ["double","double","double","solid"])
        self._borders.draw(self._borderSurf)

    def draw(self, screen):
        screen.blit(self._borderSurf, (300, 100))
        

g = Sandbox()
g.run()
