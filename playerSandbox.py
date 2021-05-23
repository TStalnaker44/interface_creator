
import pygame
from polybius.abstractGame import AbstractGame
from polybius.utils.abstractPlayer import AbstractPlayer
from polybius.managers import FRAMES
from polybius.utils.draggable import makeDraggable

class Sandbox(AbstractGame):


    def __init__(self):

        AbstractGame.__init__(self, (1000,600), "Sandbox")
        FRAMES.prepareImage("dude.png", colorKey=True)
        self._player = StickMan((10,10))
        self._player2 = Square((40,40))

    def handleEvent(self, event):
        self._player.handleEvent(event)
        self._player2.handleEvent(event)

    def draw(self, screen):
        self._player.draw(screen)
        self._player2.draw(screen)

    def update(self, ticks):
        self._player.update(ticks, self.getScreenSize(), "bounce")
        self._player2.update(ticks, self.getScreenSize(), "torus")
    

@makeDraggable
class StickMan(AbstractPlayer):

    def __init__(self, pos):
        movement = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        AbstractPlayer.__init__(self, "dude.png", pos, movement, True)

    def manageAnimations(self, ticks):
        state = self.getCurrentState()
        if state == "standing":
            self.setRowOnSpriteSheet(1)
            self.setFramesInRow(1)
        if state == "walking":
            self.setRowOnSpriteSheet(0)
            self.setFramesInRow(2)
        self.updateAnimation(ticks)

@makeDraggable
class Square(AbstractPlayer):

    def __init__(self, pos):
        surf = pygame.Surface((100,100))
        surf.fill((255,0,0))
        movement = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]
        AbstractPlayer.__init__(self, surf, pos, movement, True)
        

g = Sandbox()
g.run()
