
import pygame, copy
from polybius.graphics import Button, TextInput, TextBox
from polybius.utils import EventWrapper, Font
from parameterDisplay import ParameterDisplay

class DesignWindow():

    def __init__(self, pos=(0,0), dims=(600,600)):

        self._pos = pos
        self._dims = dims
        self._window = pygame.Surface(self._dims)

        self._p = ParameterDisplay((800, 15))

        self._buttons = []
        self._textInputs = []
        self._textBoxes = []
        
        self._dragging = None
        self._selected = None
        self._copyTemplate = None

        self._snap = True
        self._snappingLine = None

        self._dragEvent = EventWrapper(pygame.MOUSEBUTTONDOWN, 1)
        self._copyEvent = EventWrapper(pygame.KEYDOWN, pygame.K_c, [pygame.KMOD_CTRL])
        self._pasteEvent = EventWrapper(pygame.KEYDOWN, pygame.K_v, [pygame.KMOD_CTRL])

    def draw(self, screen):
        self._window.fill((255,255,255))
        for b in self._buttons:
            b.draw(self._window)
        for t in self._textInputs:
            t.draw(self._window)
        for t in self._textBoxes:
            t.draw(self._window)
        if self._snappingLine != None:
            pygame.draw.line(self._window,
                             (0,0,255),
                             self._snappingLine[0],
                             self._snappingLine[1],
                             1)
            self._window
        screen.blit(self._window, self._pos)
        self._p.draw(screen)
        

    def handleTestModeEvents(self, event):
        for b in self._buttons:
            b.handleEvent(event, lambda: None, offset=self._pos)
        for t in self._textInputs:
            t.handleEvent(event, offset=self._pos)

    def handleCreateModeEvents(self, event):

        if self._copyEvent.check(event):
            if self._selected != None:
                self._copyTemplate = self._selected
        if self._pasteEvent.check(event):
            if self._copyTemplate != None:
                self.paste()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            rect = self._window.get_rect()
            point = (event.pos[0] - self._pos[0],
                     event.pos[1] - self._pos[1])
            if rect.collidepoint(point):
                if self._dragEvent.check(event):
                    self._selected = None
                    widgets = self._buttons + self._textInputs + self._textBoxes
                    for w in widgets:
                        if w.getCollideRect().collidepoint(point):
                            self._dragging = (w, event.pos)
                            self._selected = w
        self._p.handleEvent(event)

    def paste(self):
        w = copy.copy(self._copyTemplate)
        w.setPosition((100,100))
        t = type(w)
        if t == Button: self._buttons.append(w)
        elif t == TextInput: self._textInputs.append(w)
        elif t == TextBox: self._textBoxes.append(w)

    def update(self, ticks):
        self.updateElementDragging()
        if self._selected == None:
            self._p.reset()
        else:
            self._p.update(ticks)

    def updateInterface(self, ticks):
        for t in self._textInputs:
            t.update(ticks)

    def updateElementDragging(self):
        if self._dragging != None:
            b, previous = self._dragging
            current = pygame.mouse.get_pos()
            delta_x = current[0] - previous[0]
            delta_y = current[1] - previous[1]
            b.setPosition((b.getX()+delta_x,
                          b.getY()+delta_y))
            self._dragging = (b, current)
            self._p.createLabels(self._selected)
            if self._snap:
                self.handleSnapping()
            if not pygame.mouse.get_pressed()[0]:
                self._dragging = None
                self._snappingLine = None

    def handleSnapping(self):
        wCenter = self.findCenter(self._selected)
        widgets = self._buttons + self._textInputs + self._textBoxes
        for w in widgets:
            if w != self._selected:
                center = self.findCenter(w)
                if abs(wCenter[0] - center[0]) < 5:
                    x = center[0] - (self._selected.getWidth()//2)
                    self._selected.setPosition((x,self._selected.getY()))
                    self._snappingLine = ((wCenter[0],0),
                                          (wCenter[0],self._dims[1]))
                    return
        self._snappingLine = None

    def findCenter(self, widget):
        x = widget.getX() + (widget.getWidth()//2)
        y = widget.getY() + (widget.getHeight()//2)
        return (x,y)
        
    def makeButton(self, pos):
        text = "Button"
        font = Font("Arial", 16)
        b = Button(text, pos, font,
                   (100,120,80), (5,0))
        self._buttons.append(b)

    def makeTextInput(self, pos):
        font = Font("Arial", 16)
        t = TextInput(pos, font, (100,25))
        self._textInputs.append(t)

    def makeTextBox(self, pos):
        t = TextBox("Text", pos, Font("Arial", 16))
        self._textBoxes.append(t)

    def export(self):
        retString = self.writeImports()
        retString += "class Interface(AbstractInterface):\n\n"
        retString += "\tdef __init__(self):\n"
        retString += "\t\tAbstractInterface.__init__(self)\n"        
        for line in self.writeWidgetsList().split("\n"):
            retString += "\t\t" + line + "\n"
        with open("export.py", "w") as file:
            for line in retString:
                file.write(line)
        

    def writeImports(self):
        retString = "import pygame\n"
        retString += "from polybius.abstractInterface import AbstractInterface\n"
        retString += "from polybius.graphics import Button, TextInput, TextBox\n"
        retString += "from polybius.utils import Font\n\n"
        return retString

    def writeWidgetsList(self):
        retString = ""
        for b in self._buttons:
            retString += "self._buttons.append("
            retString += self.getButtonDeclaration(b)
        retString += "\n"
        for t in self._textInputs:
            retString += "self._textInputs.append("
            retString += self.getTextInputDeclaration(t)
            retString += ")\n"
        for t in self._textBoxes:
            retString += "self._textBoxes.append("
            retString += self.getTextBoxDeclaration(t)
            retString += ")\n"
        return retString

    def getButtonDeclaration(self, button):
        txt = button.getText()
        pos = button.getPosition()
        pos = ("(%d,%d)" % (pos[0], pos[1]))
        backgroundColor = "backgroundColor=" + str(button._backgroundColor)
        fontColor = "fontColor=" + str(button._fontColor)
        borderColor = "borderColor=" + str(button._borderColor)
        borderWidth = "borderWidth=" + str(button._borderWidth)
        padding = "padding=" + str(button._padding)
        font = ("Font('%s',%s)" % (button.getFont().getFontName(),
                                   button.getFont().getFontSize()))
        return ("Button('%s',\n\t%s,\n\t%s,\n\t%s,\n\t%s,\n\t%s,\n\t%s,\n\t%s)" %
                (txt, pos, font, backgroundColor, fontColor, borderColor,
                 borderWidth, padding))

    def getTextInputDeclaration(self, tinput):
        dims = (tinput.getWidth(), tinput.getHeight())
        pos = tinput.getPosition()
        pos = ("(%d,%d)" % (pos[0], pos[1]))
        backgroundColor = "backgroundColor=" + str(tinput.getBackgroundColor())
        fontColor = "color=" + str(tinput.getFontColor())
        borderColor = "borderColor=" + str(tinput.getBorderColor())
        borderWidth = "borderWidth=" + str(tinput.getBorderWidth())
        borderHighlight = "borderHighlight=" + str(tinput._borderHighlight)
        backgroundHighlight = "backgroundHighlight=" + str(tinput._backgroundHighlight)
        maxlen = "maxLen=" + str(tinput._maxLen)
        text = "defaultText='" + tinput.getInput() + "'"
        font = ("Font('%s',%s)" % (tinput.getFont().getFontName(),
                                   tinput.getFont().getFontSize()))
        template = "TextInput(" + ("%s,\n\t"*11)[:-3] + ")"
        return (template % (pos, font, dims,
                           backgroundColor,
                           fontColor, borderColor,
                           borderWidth, borderHighlight,
                           backgroundHighlight, maxlen,
                           text))

    def getTextBoxDeclaration(self, tbox):
        text = tbox.getText()
        pos = tbox.getPosition()
        pos = ("(%d,%d)" % (pos[0], pos[1]))
        font = ("Font('%s',%s)" % (tbox.getFont().getFontName(),
                                   tbox.getFont().getFontSize()))
        fontColor = "fontColor=" + str(tbox.getFontColor())
        return ("TextBox('%s',\n\t%s,\n\t%s)" % (text, pos, font))
        

    
