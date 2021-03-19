
import pygame
from polybius.abstractGame import AbstractGame
from polybius.utils.abstractPlayer import AbstractPlayer
from polybius.managers import FRAMES


class Sandbox(AbstractGame):

    def __init__(self):
        
        AbstractGame.__init__(self, (1000,600), "Sandbox")

        surf = pygame.Surface((100,100))
        surf.fill((255,0,0))
        FRAMES.prepareImage("dude.png", colorKey=True)
        self._player1 = StickMan((10,10))
        movement = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]
        self._player2 = AbstractPlayer(surf, (25,25), movement)

    def draw(self, screen):
        self._player1.draw(screen)
        self._player2.draw(screen)

    def handleEvent(self, event):
        self._player1.handleEvent(event)
        self._player2.handleEvent(event)

    def update(self, ticks):
        self._player1.update(ticks, (0,0))
        self._player2.update(ticks, (0,0))

class StickMan(AbstractPlayer):

    def __init__(self, pos):
        movement = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        super().__init__("dude.png", pos, movement, True)

    def manageAnimations(self, ticks):
        state = self.getCurrentState()
        if state == "standing":
            self.setRowOnSpriteSheet(1)
            self.setFramesInRow(1)
        if state == "walking":
            self.setRowOnSpriteSheet(0)
            self.setFramesInRow(2)
        self.updateAnimation(ticks)

g = Sandbox()
g.run()
