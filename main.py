
import pygame
from polybius.abstractGame import AbstractGame
from polybius.graphics import Button, TextInput
from polybius.graphics import FileMenu
from polybius.utils import EventWrapper
from designwindow import DesignWindow
from cursors import resize_x

import tkinter as tk
from tkinter import filedialog

class Game(AbstractGame):

    def __init__(self):
        AbstractGame.__init__(self, (1000,600), "New Game")

        #pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    
        self._design = DesignWindow(pos=(200,10), dims=(590,580))

        self._widgetTypes = [("Panel","Panel"),
                             ("Button","Button"),
                             ("Text Input","TextInput"),
                             ("Text Box","TextBox"),
                             ("MultiLine Text","MultiLineTextBox"),
                             ("Progress Bar","ProgressBar")]
                             #("Incrementer","Incrementer")]

        self._testMode = False

        self._saveEvent = EventWrapper(pygame.KEYDOWN,
                                       pygame.K_s, [pygame.KMOD_CTRL])

        self._loadEvent = EventWrapper(pygame.KEYDOWN,
                                       pygame.K_o, [pygame.KMOD_CTRL])

        self._root = tk.Tk()
        self._root.withdraw()
        
        self.createUI()

    def createUI(self):
        self.createModeButton()
        self.createExportButton()
        self.createAddButtons()
        #self.createFileManagers()

    def createFileManagers(self):
        self._save = FileMenu((100,100), (500,400), menuType="save",
                              filePath="saves", extension=".txt")
        self._save.center()
        self._save.close()
        
        self._load = FileMenu((100,100), (500,400), menuType="load",
                              filePath="saves", extension=".txt")
        self._load.center()
        self._load.close()

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
            b.handleEvent(event, self._design.addWidget, (self._widgetTypes[i][1],))
        self.handleSavingAndLoading(event)

    def handleSavingAndLoading(self, event):
        if self._saveEvent.check(event):
            path = filedialog.asksaveasfilename(filetypes=[("Polybius Interface","*.pi")])
            pygame.event.clear() #Ignore events while dialog is open
            if path != "":
                self.save(path)
        if self._loadEvent.check(event):
            path = filedialog.askopenfilename(filetypes=[("Polybius Inferface","*.pi")])
            pygame.event.clear() #Ignore events while dialog is open
            if path != "":
                self.load(path)

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

    def save(self, path):
        self._design.save(path)

    def load(self, path):
        self._design.load(path)

    def export(self):
        self._design.export()

g = Game()
g.run()
