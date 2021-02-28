
import pygame
from polybius.abstractGame import AbstractGame
from polybius.graphics import Button, TextInput
from polybius.utils import EventWrapper
from designwindow import DesignWindow

class Game(AbstractGame):

    def __init__(self):
        AbstractGame.__init__(self, (1000,600), "New Game")
    
        self._design = DesignWindow(pos=(200,10), dims=(590,580))

        self._widgetTypes = [("Panel",self._design.makePanel),
                             ("Button",self._design.makeButton),
                             ("Text Input",self._design.makeTextInput),
                             ("Text Box",self._design.makeTextBox),
                             ("MultiLine Text",self._design.makeMultiLineText),
                             ("Progress Bar", self._design.makeProgressBar)]

        self._testMode = False
        
        self.createUI()
        
    def createUI(self):
        self.createModeButton()
        self.createExportButton()
        self.createAddButtons()

    def createAddButtons(self):
        addFont = pygame.font.SysFont("Impact", 20)
        buttonHeight = addFont.size("A")[1]
        buttonWidth = 180
        x = self._design._pos[0] // 2 - buttonWidth // 2
        start = 75
        self._addButtons = []
        for i, k in enumerate(self._widgetTypes):
            k = k[0]
            y = start + (i * (buttonHeight + 10))
            b = Button("Add " + k,
                       (x,y),
                       addFont,
                       padding=(5,0),
                       backgroundColor=(140,140,140),
                       borderColor=(80,80,80),
                       borderWidth=2,
                       dims=(buttonWidth, buttonHeight))
            self._addButtons.append(b)

    def createExportButton(self):
        exportFont = pygame.font.SysFont("Impact", 24)
        x = (self._design._pos[0] // 2) - (exportFont.size("Export")[0]+10)//2
        y = self.getScreen().get_height()-exportFont.size("Export")[1]-10
        self._exportButton = Button("Export", (x,y), exportFont,
                                    padding=(5,0),
                                    backgroundColor=(240,0,0),
                                    borderColor=(100,0,0),
                                    borderWidth=2)

    def createModeButton(self):
        exportFont = pygame.font.SysFont("Impact", 24)
        dims = exportFont.size("Enter Create Mode")
        padding = (10,0)
        dims = (dims[0]+padding[0], dims[1]+padding[1])
        x = (self._design._pos[0] // 2) - (dims[0])//2
        y = 15
        self._modeButton = Button("Enter Test Mode", (x,y), exportFont,
                                    padding=padding,
                                    backgroundColor=(180,180,180),
                                    borderColor=(100,100,100),
                                    borderWidth=2,
                                    dims=dims)

    def draw(self, screen):
        self.getScreen().fill((50,50,50))
        self._design.draw(screen)
        self._exportButton.draw(screen)
        self._modeButton.draw(screen)
        for b in self._addButtons:
            b.draw(screen)

    def handleEvent(self, event):
        # Toggle between test and create modes
        self._modeButton.handleEvent(event, self.toggleModes)
        if self._testMode:
            self._design.handleTestModeEvents(event)
        else:
            self._design.handleCreateModeEvents(event)      
        self._exportButton.handleEvent(event, self.export)
        for i, b in enumerate(self._addButtons):
            b.handleEvent(event, self._widgetTypes[i][1], ((100,100),))
        

    def toggleModes(self):
        self._testMode = not self._testMode
        if self._testMode:
            self._modeButton.setText("Enter Create Mode")
        else:
            self._modeButton.setText("Enter Test Mode")
            
    def update(self, ticks):
        self._design.update(ticks)
        if self._testMode:
            self._design.updateInterface(ticks)

    def export(self):
        self._design.export()



g = Game()
g.run()
