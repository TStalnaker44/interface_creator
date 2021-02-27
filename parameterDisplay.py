
import pygame
from polybius.graphics import MultiLineTextBox, Button, TextInput
from polybius.utils import Font

PARAMETERS = {Button:["Text","Font","Font Size", "X Coordinate",
                      "Y Coordinate", "BG Color","Horizontal Padding",
                      "Vertical Padding", "Font Color","Border Color",
                      "Border Width"],
              TextInput:["Default Text","Font", "Font Size",
                         "X Coordinate", "Y Coordinate",
                         "Height", "Width",
                         "Font Color","BG Color", "Border Color",
                         "Border Sel.", "Border Width", "Max Length"]}

VALUES = {"Text":"widget.getText()",
          "Font":"widget.getFont().getFontName()",
          "Font Size":"widget.getFont().getFontSize()",
          "X Coordinate":"widget.getX()",
          "Y Coordinate":"widget.getY()",
          "BG Color":"widget._backgroundColor",
          "Horizontal Padding":"widget._padding[0]",
          "Vertical Padding":"widget._padding[1]",
          "Font Color":"widget.getFontColor()",
          "Border Color":"widget._borderColor",
          "Border Width":"widget._borderWidth",
          "Default Text":"widget.getInput()",
          "Max Length":"widget._maxLen",
          "Border Sel.":"widget._borderHighlight",
          "Height":"widget.getHeight()",
          "Width":"widget.getWidth()"}

NORMAL_INPUT = ("Text", "Font", "Default Text")
INT_ONLY = ("Font Size","X Coordinate", "Y Coordinate", "Border Width",
            "Horizontal Padding", "Vertical Padding", "Max Length",
            "Height", "Width")
COLOR_INPUT = ("BG Color", "Font Color", "Border Color","Border Sel.")

class ParameterDisplay():

    def __init__(self, pos=(0,0)):

        self._pos = pos 

        self._backdrop = pygame.Surface((190,570))
        self._backdrop.fill((200,200,200))

        self._labels = []
        self._inputFields = {}

        self._widget = None

        font = Font("Impact", 20)
        x = self._pos[0] + (self._backdrop.get_width() // 2 - font.size("Update")[0] // 2)
        y = self._pos[1] + self._backdrop.get_height() - font.get_height() - 15
        self._updateButton = Button("Update",
                                    (x,y),
                                    font,
                                    backgroundColor=(160,160,160),
                                    borderColor=(100,100,100),
                                    borderWidth=2,
                                    padding=(10,5))

    def createLabels(self, widget):
        self._labels = []
        self._inputFields = {}
        self._widget = widget
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
                fieldx = font.size(label)[0] + t.getX() + 10
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
            self._inputFields[label] = field
            labely += dimensions[1] + 6

    def reset(self):
        self._labels = []
        self._inputFields = {}
        self._widget = None
            
    def draw(self, screen):
        screen.blit(self._backdrop, self._pos)
        if self._widget != None:
            self._updateButton.draw(screen)
        for label in self._labels:
            label.draw(screen)
        for field in self._inputFields.values():
            field.draw(screen)

    def handleEvent(self, event):
        for field in self._inputFields.values():
            field.handleEvent(event, func=self.updateWidget)
        if self._widget != None:
            self._updateButton.handleEvent(event, self.updateWidget)

    def update(self, ticks):
        for field in self._inputFields.values():
            field.update(ticks)

    def updateWidget(self):
        if type(self._widget) == Button:
            self.updateButton(self._widget)
            

    def updateButton(self, button):
        text = self._inputFields["Text"].getInput()
        xpos = int(self._inputFields["X Coordinate"].getInput())
        ypos = int(self._inputFields["Y Coordinate"].getInput())
        bgcolor = self._inputFields["BG Color"].getRGBValues()
        fontcolor = self._inputFields["Font Color"].getRGBValues()
        bordercolor = self._inputFields["Border Color"].getRGBValues()
        hpadding = int(self._inputFields["Horizontal Padding"].getInput())
        vpadding = int(self._inputFields["Vertical Padding"].getInput())
        borderwidth = int(self._inputFields["Border Width"].getInput())
        fontname = self._inputFields["Font"].getInput()
        fontsize = int(self._inputFields["Font Size"].getInput())
        
        button.setText(text)
        button.setPosition((xpos,ypos))
        button.setBackgroundColor(bgcolor)
        button.setFontColor(fontcolor)
        button.setBorderColor(bordercolor)
        button.setPadding((hpadding, vpadding))
        button.setBorderWidth(borderwidth)
        button.setFont(Font(fontname, fontsize))

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

    def handleEvent(self, event, func=None):
        self._r.handleEvent(event, func=func)
        self._g.handleEvent(event, func=func)
        self._b.handleEvent(event, func=func)

    def update(self, ticks):
        self._r.update(ticks)
        self._g.update(ticks)
        self._b.update(ticks)

    def getRGBValues(self):
        r = int(self._r.getInput())
        g = int(self._g.getInput())
        b = int(self._b.getInput())
        return (r,g,b)

        
