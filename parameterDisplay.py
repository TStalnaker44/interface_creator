
import pygame
from polybius.graphics import MultiLineTextBox, Button, TextInput

PARAMETERS = {Button:["Text","Font","Font Size", "X Coordinate",
                      "Y Coordinate", "BG Color","Horizontal Padding",
                      "Vertical Padding", "Font Color","Border Color",
                      "Border Width"],
              TextInput:[]}

VALUES = {"Text":"widget.getText()",
          "Font":"widget.getFont().getFontName()",
          "Font Size":"widget.getFont().getFontSize()",
          "X Coordinate":"widget.getX()",
          "Y Coordinate":"widget.getY()",
          "BG Color":"widget._backgroundColor",
          "Horizontal Padding":"widget._padding[0]",
          "Vertical Padding":"widget._padding[1]",
          "Font Color":"widget._fontColor",
          "Border Color":"widget._borderColor",
          "Border Width":"widget._borderWidth"}

NORMAL_INPUT = ("Text", "Font")
INT_ONLY = ("Font Size","X Coordinate", "Y Coordinate", "Border Width",
            "Horizontal Padding", "Vertical Padding")
COLOR_INPUT = ("BG Color", "Font Color", "Border Color")

class ParameterDisplay():

    def __init__(self, pos=(0,0)):

        self._pos = pos 

        self._backdrop = pygame.Surface((190,570))
        self._backdrop.fill((200,200,200))

        self._labels = []
        self._inputFields = []

        #self.createLabels(Button("This is TEXT",(0,0),pygame.font.SysFont("Arial",22)))
        

    def createLabels(self, widget):
        self._labels = []
        self._inputFields = []
        widgetType = type(widget)        
        labelx, labely = self._pos[0] + 5, self._pos[1] + 10
        font = pygame.font.SysFont("Arial", 16)
        rgbFont = pygame.font.SysFont("Arial", 16)
        dimensions = (100,font.size("A")[1]+5)
        num_dims = (50, font.size("A")[1]+5)
        for label in PARAMETERS[widgetType]:
            
            t = MultiLineTextBox(label,(labelx,labely),font)
            self._labels.append(t)
            
            if label in NORMAL_INPUT:
                fieldx = font.size("Font")[0] + t.getX() + 10
                containerWidth = self._pos[0] + self._backdrop.get_width()
                dimensions = (containerWidth - fieldx - 5,
                              font.size("A")[1]+5)
                field = TextInput((fieldx,labely), font, dimensions,
                                  maxLen=20,
                                  defaultText=eval(VALUES[label]))
                
            if label in INT_ONLY:
                fieldx = t.getWidth() + t.getX() + 10
                containerWidth = self._pos[0] + self._backdrop.get_width()
                dimensions = (containerWidth - fieldx - 5,
                              font.size("A")[1]+5)
                default = str(eval(VALUES[label]))
                field = TextInput((fieldx,labely), font, dimensions,
                                  maxLen=4, numerical=True, defaultText=default)
                
            if label in COLOR_INPUT:
                fieldx = t.getWidth() + t.getX() + 10
                defaults = eval(VALUES[label])
                field = RGBInput((fieldx, labely), rgbFont, defaults)
            self._inputFields.append(field)
            labely += dimensions[1] + 6

    def reset(self):
        self._labels = []
        self._inputFields = []
            
    def draw(self, screen):
        screen.blit(self._backdrop, self._pos)
        for label in self._labels:
            label.draw(screen)
        for field in self._inputFields:
            field.draw(screen)

    def handleEvent(self, event):
        for field in self._inputFields:
            field.handleEvent(event)

    def update(self, ticks):
        for field in self._inputFields:
##            if type(field) == RGBInput:
            field.update(ticks)

class RGBInput():

    def __init__(self, pos, font, defaultValues=(0,0,0)):

        x = pos[0]
        y = pos[1]
        dims = font.size("255")
        dims = (dims[0]+8, dims[1]+5)
        self._r = TextInput((x,y), font, dims,
                            maxLen=3, numerical=True,
                            defaultText=str(defaultValues[0]))
        self._g = TextInput((x+dims[0]+2,y), font, dims,
                            maxLen=3, numerical=True,
                            defaultText=str(defaultValues[1]))
        self._b = TextInput((x+(2*(dims[0]+2)),y), font, dims,
                            maxLen=3, numerical=True,
                            defaultText=str(defaultValues[2]))

    def draw(self, screen):
        self._r.draw(screen)
        self._g.draw(screen)
        self._b.draw(screen)

    def handleEvent(self, event):
        self._r.handleEvent(event)
        self._g.handleEvent(event)
        self._b.handleEvent(event)

    def update(self, ticks):
        self._r.update(ticks)
        self._g.update(ticks)
        self._b.update(ticks)

        
