
import pygame
from polybius.graphics import MultiLineTextBox, Button, TextInput, TextBox
from polybius.graphics import ProgressBar, Panel
from polybius.utils import Font

PARAMETERS = {Button:["Text","Font","Font Size", "X Coordinate",
                      "Y Coordinate", "BG Color","Horizontal Padding",
                      "Vertical Padding", "Font Color","Border Color",
                      "Border Width"],
              TextInput:["Default Text","Font", "Font Size",
                         "X Coordinate", "Y Coordinate",
                         "Height", "Width",
                         "Font Color","BG Color", "Border Color",
                         "BG Sel.", "Border Sel.", "Border Width", "Max Length"],
              TextBox:["Text","Font","Font Size", "Font Color",
                       "X Coordinate", "Y Coordinate"],
              MultiLineTextBox:["Text","Font","Font Size", "Font Color",
                                "X Coordinate", "Y Coordinate", "BG Color",
                                "Horizontal Padding", "Vertical Padding",
                                "Line Spacing", "Alignment"],
              ProgressBar:["X Coordinate", "Y Coordinate", "Length", "Height",
                           "Max Stat", "Active Stat", "Border Color", "Border Width",
                           "BG Color", "Bar Color", "Alignment"],
              Panel:["X Coordinate", "Y Coordinate", "Height", "Width",
                     "BG Color", "Border Color", "Border Width"]}

VALUES = {"Text":"widget.getText()",
          "Font":"widget.getFont().getFontName()",
          "Font Size":"widget.getFont().getFontSize()",
          "X Coordinate":"widget.getX()",
          "Y Coordinate":"widget.getY()",
          "BG Color":"widget._backgroundColor",
          "Horizontal Padding":"widget._padding[0]",
          "Vertical Padding":"widget._padding[1]",
          "Font Color":"widget.getFontColor()",
          "Border Color":"widget.getBorderColor()",
          "Border Width":"widget.getBorderWidth()",
          "Default Text":"widget.getInput()",
          "Max Length":"widget._maxLen",
          "Border Sel.":"widget._borderHighlight",
          "Height":"widget.getHeight()",
          "Width":"widget.getWidth()",
          "BG Sel.":"widget._backgroundHighlight",
          "Line Spacing":"widget.getLineSpacing()",
          "Alignment":"widget.getAlignment()",
          "Length":"widget.getLength()",
          "Max Stat":"widget.getMaxStat()",
          "Active Stat":"widget.getActiveStat()",
          "Bar Color":"widget.getBarColor()"}

NORMAL_INPUT = ("Text","Font", "Default Text", "Alignment")
INT_ONLY = ("Font Size","X Coordinate", "Y Coordinate", "Border Width",
            "Horizontal Padding", "Vertical Padding", "Max Length",
            "Height", "Width", "Line Spacing", "Max Stat", "Active Stat",
            "Length")
COLOR_INPUT = ("BG Color", "Font Color", "Border Color","Border Sel.","BG Sel.",
               "Bar Color")

class ParameterDisplay():

    def __init__(self, pos=(0,0)):

        self._pos = pos 

        self._backdrop = pygame.Surface((190,570))
        self._backdrop.fill((200,200,200))

        self._labels = []
        self._inputFields = {}

        self._widget = None
        self._delete = False

        font = Font("Impact", 20)
        x = self._pos[0] + (self._backdrop.get_width() // 2 - font.size("Delete")[0] // 2)
        y = self._pos[1] + self._backdrop.get_height() - font.get_height() - 20
        self._deleteButton = Button("Delete",
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
                                  defaultText=eval(VALUES[label]),
                                  allowSymbols=True)
                
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
        for label in self._labels:
            label.draw(screen)
        for field in self._inputFields.values():
            field.draw(screen)
        if self._widget != None:
            self._deleteButton.draw(screen)

    def handleEvent(self, event):
        for field in self._inputFields.values():
            field.handleEvent(event, func=self.updateWidget)
        if self._widget != None:
            self._deleteButton.handleEvent(event, func=self.flagDelete)

    def flagDelete(self):
        self._delete = True

    def update(self, ticks):
        for field in self._inputFields.values():
            field.update(ticks)

    def updateWidget(self):
        if type(self._widget) == Button:
            self.updateButton(self._widget)
        if type(self._widget) == TextInput:
            self.updateTextInput(self._widget)
        if type(self._widget) == TextBox:
            self.updateTextBox(self._widget)
        if type(self._widget) == MultiLineTextBox:
            self.updateMultiTextBox(self._widget)
        if type(self._widget) == ProgressBar:
            self.updateProgressBar(self._widget)
        if type(self._widget) == Panel:
            self.updatePanel(self._widget)

    def updatePanel(self, pan):
        xpos = int(self._inputFields["X Coordinate"].getInput())
        ypos = int(self._inputFields["Y Coordinate"].getInput())
        bgcolor = self._inputFields["BG Color"].getRGBValues()
        bordercolor = self._inputFields["Border Color"].getRGBValues()
        borderwidth = int(self._inputFields["Border Width"].getInput())
        width = int(self._inputFields["Width"].getInput())
        height = int(self._inputFields["Height"].getInput())

        pan.setPosition((xpos,ypos))
        pan.setDimensions((width,height))
        pan.setBackgroundColor(bgcolor)
        pan.setBorderColor(bordercolor)
        pan.setBorderWidth(borderwidth)

    def updateProgressBar(self, bar):
        xpos = int(self._inputFields["X Coordinate"].getInput())
        ypos = int(self._inputFields["Y Coordinate"].getInput())
        bgcolor = self._inputFields["BG Color"].getRGBValues()
        barcolor = self._inputFields["Bar Color"].getRGBValues()
        align = self._inputFields["Alignment"].getInput()
        bordercolor = self._inputFields["Border Color"].getRGBValues()
        borderwidth = int(self._inputFields["Border Width"].getInput())
        length = int(self._inputFields["Length"].getInput())
        height = int(self._inputFields["Height"].getInput())
        maxStat = int(self._inputFields["Max Stat"].getInput())
        actStat = int(self._inputFields["Active Stat"].getInput())

        bar.setPosition((xpos,ypos))
        if align.lower() in ("left", "right", "center"):
            bar.setAlignment(align)
        bar.setBackgroundColor(bgcolor)
        bar.setBarColor(barcolor)
        bar.setBorderColor(bordercolor)
        bar.setBorderWidth(borderwidth)
        bar.setLength(length)
        bar.setHeight(height)
        bar.setMaxStat(maxStat)
        bar.setActiveStat(actStat)

    def updateMultiTextBox(self, tbox):
        text = self._inputFields["Text"].getInput().replace("\\n","\n")
        xpos = int(self._inputFields["X Coordinate"].getInput())
        ypos = int(self._inputFields["Y Coordinate"].getInput())
        fontname = self._inputFields["Font"].getInput()
        fontsize = int(self._inputFields["Font Size"].getInput())
        fontcolor = self._inputFields["Font Color"].getRGBValues()
        bgcolor = self._inputFields["BG Color"].getRGBValues()
        hpadding = int(self._inputFields["Horizontal Padding"].getInput())
        vpadding = int(self._inputFields["Vertical Padding"].getInput())
        linespace = int(self._inputFields["Line Spacing"].getInput())
        align = self._inputFields["Alignment"].getInput()

        tbox.setText(text)
        tbox.setPosition((xpos,ypos))
        tbox.setFontColor(fontcolor)
        tbox.setFont(Font(fontname, fontsize))
        if all(color!="" for color in bgcolor):
            tbox.setBackgroundColor(bgcolor)
        tbox.setPadding((hpadding,vpadding))
        tbox.setLineSpacing(linespace)
        if align.lower() in ("left", "right", "center"):
            tbox.setAlignment(align)

    def updateTextBox(self, tbox):
        text = self._inputFields["Text"].getInput()
        xpos = int(self._inputFields["X Coordinate"].getInput())
        ypos = int(self._inputFields["Y Coordinate"].getInput())
        fontname = self._inputFields["Font"].getInput()
        fontsize = int(self._inputFields["Font Size"].getInput())
        fontcolor = self._inputFields["Font Color"].getRGBValues()

        tbox.setText(text)
        tbox.setPosition((xpos,ypos))
        tbox.setFontColor(fontcolor)
        tbox.setFont(Font(fontname, fontsize))

    def updateTextInput(self, tinput):
        text = self._inputFields["Default Text"].getInput()
        xpos = int(self._inputFields["X Coordinate"].getInput())
        ypos = int(self._inputFields["Y Coordinate"].getInput())
        width = int(self._inputFields["Width"].getInput())
        height = int(self._inputFields["Height"].getInput())
        bgcolor = self._inputFields["BG Color"].getRGBValues()
        fontcolor = self._inputFields["Font Color"].getRGBValues()
        bordercolor = self._inputFields["Border Color"].getRGBValues()
        bg_sel = self._inputFields["BG Sel."].getRGBValues()
        border_sel = self._inputFields["Border Sel."].getRGBValues()
        borderwidth = int(self._inputFields["Border Width"].getInput())
        fontname = self._inputFields["Font"].getInput()
        fontsize = int(self._inputFields["Font Size"].getInput())
        maxlen = int(self._inputFields["Max Length"].getInput())
        
        tinput.setText(text)
        tinput.setPosition((xpos,ypos))
        tinput.setBackgroundColor(bgcolor)
        tinput.setFontColor(fontcolor)
        tinput.setBorderColor(bordercolor)
        tinput.setBorderWidth(borderwidth)
        tinput.setBackgroundHighlight(bg_sel)
        tinput.setBorderHighlight(border_sel)
        tinput.setFont(Font(fontname, fontsize))
        tinput._maxLen = maxlen
        tinput.setDimensions((width,height))
            

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
        if defaultValues == None:
            defaultValues=("","","")
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
        r = self._r.getInput()
        r = int(r) if r.isdigit() else ''
        g = self._g.getInput()
        g = int(g) if g.isdigit() else ''
        b = self._b.getInput()
        b = int(b) if b.isdigit() else ''
        return (r,g,b)

        
