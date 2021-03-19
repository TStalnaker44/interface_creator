import pygame
from polybius.graphics import Drawable

class AbstractGame():

    def __init__(self, displaySize, caption="Game", fullscreen=False):

        # Initialize the pygame modules
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        # Update the title for the window
        pygame.display.set_caption(caption)

        # Get the screen
        if fullscreen:
            self._screen = pygame.display.set_mode(displaySize, pygame.FULLSCREEN)
        else:
            self._screen = pygame.display.set_mode(displaySize)

        self._screenSize = displaySize
        self._worldSize = displaySize

        # Create an instance of the game clock
        self._gameClock = pygame.time.Clock()

        self._tracking=None
        
        self._running = True

    def run(self):
        while self._running:
            self._gameClock.tick()
            self._abstractDraw()
            self._abstractHandleEvents()
            self._abstractUpdate()
        pygame.quit()

    def endGame(self):
        self._running = False

    def getGameClock(self):
        return self._gameClock

    def getScreen(self):
        return self._screen

    def getTrackingObject(self):
        return self._tracking

    def setTrackingObject(self, obj):
        self._tracking = obj

    def setWorldSize(self, size):
        self._worldSize = size

    def _abstractDraw(self):
        self.getScreen().fill((255, 255, 255))
        self.draw(self._screen)
        pygame.display.flip()

    def _abstractHandleEvents(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                self.endGame()
            else:
                self.handleEvent(event)

    def _abstractUpdate(self):
        ticks = self._gameClock.get_time() / 1000
        self.update(ticks)
        if self._tracking != None:
            Drawable.updateOffset(self._tracking,
                                  self._screenSize,
                                  self._worldSize)
