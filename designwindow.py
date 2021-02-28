
import pygame, copy
from polybius.graphics import Button, TextInput, TextBox
from polybius.graphics import MultiLineTextBox, ProgressBar
from polybius.graphics import Panel
from polybius.utils import EventWrapper, Font
from parameterDisplay import ParameterDisplay

class DesignWindow():

    def __init__(self, pos=(0,0), dims=(600,600)):

        self._pos = pos
        self._dims = dims
        self._window = pygame.Surface(self._dims)

        self._p = ParameterDisplay((800, 15))

        self._panels = []
        self._buttons = []
        self._textInputs = []
        self._textBoxes = []
        self._multiTextBoxes = []
        self._progressBars = []

        self.makeTypeToListDict()
        
        self._dragging = None
        self._selected = None
        self._copyTemplate = None

        self._snap = True
        self._snapSensitivity = 5
        self._snappingLines = [None, None]

        self._dragEvent = EventWrapper(pygame.MOUSEBUTTONDOWN, 1)
        self._copyEvent = EventWrapper(pygame.KEYDOWN, pygame.K_c, [pygame.KMOD_CTRL])
        self._pasteEvent = EventWrapper(pygame.KEYDOWN, pygame.K_v, [pygame.KMOD_CTRL])

    def makeTypeToListDict(self):
        self._types = {Button:self._buttons,
                     TextInput:self._textInputs,
                     TextBox:self._textBoxes,
                     MultiLineTextBox:self._multiTextBoxes,
                     ProgressBar:self._progressBars,
                     Panel:self._panels}

    def draw(self, screen):
        self._window.fill((255,255,255))
        for w in self.getAllWidgets():
            w.draw(self._window)
        self.drawSnappingLines()
        self.drawBoxAroundSelected()
        screen.blit(self._window, self._pos)
        self._p.draw(screen)

    def drawSnappingLines(self):
        for line in self._snappingLines:
            if line != None:
                pygame.draw.line(self._window, (0,0,255),
                                 line[0], line[1], 1)
    def drawBoxAroundSelected(self):
        if self._selected != None:
            rect = pygame.Rect(self._selected.getX()-5,
                               self._selected.getY()-5,
                               self._selected.getWidth()+10,
                               self._selected.getHeight()+10)
            pygame.draw.rect(self._window, (255,0,0), rect, 4)
        

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
                    for w in self.getAllWidgets():
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
        elif t == MultiLineTextBox: self._multiTextBoxes.append(w)
        elif t == ProgressBar: self._progressBars.append(w)

    def update(self, ticks):
        self.updateElementDragging()
        if self._selected == None:
            self._p.reset()
        else:
            self._p.update(ticks)
        if self._p._delete:
            self.deleteWidget()
            self._p._delete = False


    def deleteWidget(self):
        w = self._selected
        self._types[type(w)].remove(w)
        self._selected = None

    def updateInterface(self, ticks):
        for t in self._textInputs:
            t.update(ticks)

    def getAllWidgets(self):
        return self._panels + self._buttons + self._textInputs + \
               self._textBoxes + self._multiTextBoxes + \
               self._progressBars

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
                self._snappingLines = [None, None]

    def handleSnapping(self):
        widgets = self.getAllWidgets()
        self._snappingLines[0] = self.verticalLineSnapping(widgets)
        self._snappingLines[1] = self.horizontalLineSnapping(widgets)

    def verticalLineSnapping(self, widgets):
        wCenter = self.findCenter(self._selected)
        for w in widgets:
            if w != self._selected:
                center = self.findCenter(w)
                if abs(wCenter[0] - center[0]) < self._snapSensitivity:
                    x = center[0] - (self._selected.getWidth()//2)
                    self._selected.setPosition((x,self._selected.getY()))
                    return ((wCenter[0],0),(wCenter[0],self._dims[1]))
        return None

    def horizontalLineSnapping(self, widgets):
        wCenter = self.findCenter(self._selected)
        for w in widgets:
            if w != self._selected:
                center = self.findCenter(w)
                if abs(wCenter[1] - center[1]) < self._snapSensitivity:
                    y = center[1] - (self._selected.getHeight()//2)
                    self._selected.setPosition((self._selected.getX(),y))
                    return ((0,wCenter[1]), (self._dims[0],wCenter[1]))
        return None

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

    def makeMultiLineText(self, pos):
        t = MultiLineTextBox("Multi-Line Text", pos, Font("Arial",16))
        self._multiTextBoxes.append(t)

    def makeProgressBar(self, pos):
        bar = ProgressBar(pos, 50, 100, 50)
        self._progressBars.append(bar)

    def makePanel(self, pos):
        p = Panel(pos)
        self._panels.append(p)

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
        retString += "from polybius.graphics import MultiLineTextBox, ProgressBar\n"
        retString += "from polybius.utils import Font\n\n"
        return retString

    def writeWidgetsList(self):
        retString = ""
        for b in self._buttons:
            retString += "self._buttons.append("
            retString += self.getButtonDeclaration(b)
            retString += ")\n"
        for t in self._textInputs:
            retString += "self._textInputs.append("
            retString += self.getTextInputDeclaration(t)
            retString += ")\n"
        for t in self._textBoxes:
            retString += "self._textBoxes.append("
            retString += self.getTextBoxDeclaration(t)
            retString += ")\n"
        for t in self._multiTextBoxes:
            retString += "self._multiTextBoxes.append("
            retString += self.getMultiLineTextBoxDeclaration(t)
            retString += ")\n"
        for bar in self._progressBars:
            retString += "self._progressBars.append("
            retString += self.getProgressBarDeclaration(bar)
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

    def getMultiLineTextBoxDeclaration(self, tbox):
        text = "'" + tbox.getText() + "'"
        pos = tbox.getPosition()
        pos = ("(%d,%d)" % (pos[0], pos[1]))
        font = ("Font('%s',%s)" % (tbox.getFont().getFontName(),
                                   tbox.getFont().getFontSize()))
        fontColor = "fontColor=" + str(tbox.getFontColor())
        backgroundColor = "backgroundColor=" + str(tbox.getBackgroundColor())
        alignment = "alignment='" + str(tbox.getAlignment()) + "'"
        padding = "padding=" + str(tbox.getPadding())
        spacing = "linespacing=" + str(tbox.getLineSpacing())
        template = "MultiLineTextBox(" + ("%s,\n\t"*8)[:-3] + ")"
        return (template % (text, pos, font, fontColor, backgroundColor,
                            padding, spacing, alignment))

    def getProgressBarDeclaration(self, bar):
        pos = bar.getPosition()
        pos = ("(%d,%d)" % (pos[0], pos[1]))
        length = bar.getLength()
        maxStat = bar.getMaxStat()
        actStat = bar.getActiveStat()
        borderWidth = "borderWidth=" + str(bar.getBorderWidth())
        borderColor = "borderColor=" + str(bar.getBorderColor())
        backgroundColor = "backgroundColor=" + str(bar.getBackgroundColor())
        barColor = "barColor=" + str(bar.getBarColor())
        height = "height=" + str(bar.getHeight())
        alignment = "alignment='" + str(bar.getAlignment()) + "'"
        template = "ProgressBar(" + ("%s,\n\t"*10)[:-3] + ")"
        return (template % (pos, length, maxStat, actStat, borderWidth,
                            borderColor, backgroundColor, barColor,
                            height, alignment))
        
        

    
