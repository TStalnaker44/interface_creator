
import pygame
from polybius.abstractGame import AbstractGame
from polybius.abstractLevel import AbstractLevel
from polybius.graphics import Drawable
from polybius.utils.abstractPlayer import AbstractPlayer
from polybius.managers import FRAMES

class Sandbox(AbstractGame):

    def __init__(self):
        AbstractGame.__init__(self, (1000,600), "Sandbox")
        self._level = Main(self.getScreenSize())
        self.addLevel("main", self._level)
        self._level2 = Main(self.getScreenSize())
        self.addLevel("main2", self._level2)
        self.switchTo("main")

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN and \
           event.key == pygame.K_u:
            if self._level == self.getCurrentLevel():
                self.switchTo("main2")
            else:
                self.switchTo("main")
        
class Main(AbstractLevel):

    def __init__(self, screenSize):

        AbstractLevel.__init__(self, screenSize)
        surf = pygame.Surface((100,100))
        surf.fill((255,0,0))
        FRAMES.prepareImage("dude.png", colorKey=True)
        FRAMES.prepareImage("background.png", (5000,5000))
        self._back = Drawable("background.png", (0,0))
        self._player1 = StickMan((10,10))
        movement = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]
        self._player2 = AbstractPlayer(surf, (25,25), movement)
        self.setTrackingObject(self._player1)
        self.setWorldSize((5000,5000))

    def draw(self, screen):
        self._back.draw(screen)
        self._player1.draw(screen)
        self._player2.draw(screen)

    def handleEvent(self, event):
        self._player1.handleEvent(event)
        self._player2.handleEvent(event)
        if event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE:
            current = self.getTrackingObject()
            if current == self._player1:
                self.setTrackingObject(self._player2)
            else:
                self.setTrackingObject(self._player1)

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
