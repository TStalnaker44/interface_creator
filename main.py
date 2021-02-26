
import pygame
from polybius.abstractGame import AbstractGame
from polybius.graphics import Button, TextInput
from polybius.utils import EventWrapper
from designwindow import DesignWindow

class Game(AbstractGame):

    def __init__(self):
        AbstractGame.__init__(self, (800,600), "New Game")
        self.getScreen().fill((50,50,50))

        self._design = DesignWindow(pos=(200,10), dims=(590,580))

        self._design.addFont("font1","Arial",16)

        self._testMode = False
        
        self._toggleModeEvent = EventWrapper(pygame.KEYDOWN, pygame.K_m)

        self.createUI()
        
    def createUI(self):
        
        exportFont = pygame.font.SysFont("Impact", 24)

        dims = exportFont.size("Enter Create Mode")
        padding = (10,0)
        dims = (dims[0]+padding[0], dims[1]+padding[1])
        x = (self._design._pos[0] // 2) - (dims[0])//2
        y = 10
        self._modeButton = Button("Enter Test Mode", (x,y), exportFont,
                                    padding=padding,
                                    backgroundColor=(180,180,180),
                                    borderColor=(100,100,100),
                                    borderWidth=2,
                                    dims=dims)
        
        x = (self._design._pos[0] // 2) - (exportFont.size("Export")[0]+10)//2
        y = self.getScreen().get_height()-exportFont.size("Export")[1]-10
        self._exportButton = Button("Export", (x,y), exportFont,
                                    padding=(5,0),
                                    backgroundColor=(240,0,0),
                                    borderColor=(100,0,0),
                                    borderWidth=2)

        

    def draw(self, screen):
        self._design.draw(screen)
        self._exportButton.draw(screen)
        self._modeButton.draw(screen)

    def handleEvent(self, event):
        # Toggle between test and create modes
        self._modeButton.handleEvent(event, self.toggleModes)
        if self._testMode:
            self._design.handleTestModeEvents(event)
        else:
            self._design.handleCreateModeEvents(event)
            
        self._exportButton.handleEvent(event, self.export)

    def toggleModes(self):
        self._testMode = not self._testMode
        if self._testMode:
            self._modeButton.setText("Enter Create Mode")
        else:
            self._modeButton.setText("Enter Test Mode")
            
    def update(self, ticks):
        self._design.updateElementDragging()

    def export(self):
        self._design.export()



g = Game()
g.run()
