
import pygame
from polybius.graphics import MultiLineTextBox, Button, TextInput

PARAMETERS = {Button:["Text","Font","Position","BG Color","Padding",
                      "Font Color","Border Color", "Border Width"],
              TextInput:[]}

class ParameterDisplay():

    def __init__(self, pos=(0,0)):

        self._pos = pos 

        self._backdrop = pygame.Surface((190,570))
        self._backdrop.fill((200,200,200))

        
        self.createLabels(Button)
        

    def createLabels(self, widgetType):
        self._inputFields = []
        x, y = self._pos[0] + 5, self._pos[1] + 10
        font = pygame.font.SysFont("Arial", 16)
        text = "\n".join(PARAMETERS[widgetType])    
        self._labels = MultiLineTextBox(text,
                                        (x,y),
                                        font,
                                        alignment="center",
                                        linespacing=11,
                                        antialias=True)

        x = self._labels.getX() + self._labels.get_width() + 5
        y = self._labels.getY()
        dimensions = (100,font.size("A")[1]+5)
        for label in PARAMETERS[widgetType]:
            field = TextInput((x,y),
                              font,
                              dimensions)
            self._inputFields.append(field)
            y += dimensions[1] + 6
            
    def draw(self, screen):
        screen.blit(self._backdrop, self._pos)
        self._labels.draw(screen)
        for field in self._inputFields:
            field.draw(screen)

    def handleEvent(self, event):
        for field in self._inputFields:
            field.handleEvent(event)

        
