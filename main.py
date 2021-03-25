
import pygame
from polybius.abstractGame import AbstractGame
from polybius.graphics import Button, TextInput
from polybius.graphics import FileMenu
from polybius.utils import EventWrapper
from designwindow import DesignWindow

import tkinter as tk
from tkinter import filedialog

class Game(AbstractGame):

    def __init__(self):
        AbstractGame.__init__(self, (1000,600), "New Game")
    
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
        self.createFileManagers()

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
        if self._save.getDisplay():
            self._save.draw(screen)
        if self._load.getDisplay():
            self._load.draw(screen)

    def handleEvent(self, event):
        # Toggle between test and create modes
        self._modeButton.handleEvent(event, self.toggleModes)
        if not (self._save.getDisplay() or self._load.getDisplay()):
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
            self._save.display()
            self._load.close()
        if self._loadEvent.check(event):
            path = filedialog.askopenfilename(filetypes=[("Text",".txt")])
            print(path)
            self._load.display()
            self._save.close()
        if self._save.getDisplay():
            path = filedialog.asksaveasfilename()
            print(path)
            sel = self._save.handleEvent(event, lambda: None)
            if sel != None: self.save(sel)
        if self._load.getDisplay():
            sel = self._load.handleEvent(event, lambda: None)
            if sel != None: self.load(sel)

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

    def save(self, sel):
        self._design.save(sel)

    def load(self, sel):
        self._design.load(sel)

    def export(self):
        self._design.export()



g = Game()
g.run()
