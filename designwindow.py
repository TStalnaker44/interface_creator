
import pygame, copy
from polybius.graphics import Button, TextInput, TextBox
from polybius.graphics import MultiLineTextBox, ProgressBar
from polybius.graphics import Panel, Incrementer
from polybius.utils import EventWrapper, Font
from parameterDisplay import ParameterDisplay
import declarations

class DesignWindow():

    def __init__(self, pos=(0,0), dims=(600,600)):

        self._pos = pos
        self._dims = dims
        self._window = pygame.Surface(self._dims)

        self._p = ParameterDisplay((800, 15))
        
        self._widgets = []

        self.makeParametersDictionary()
        
        self._dragging = None
        self._selected = None
        self._copyTemplate = None

        self._snap = True
        self._snapSensitivity = 5
        self._snappingLines = [None, None]

        self._dragEvent = EventWrapper(pygame.MOUSEBUTTONDOWN, 1)
        self._copyEvent = EventWrapper(pygame.KEYDOWN, pygame.K_c, [pygame.KMOD_CTRL])
        self._pasteEvent = EventWrapper(pygame.KEYDOWN, pygame.K_v, [pygame.KMOD_CTRL])

    def makeParametersDictionary(self):
        font = Font("Arial", 16)
        pos = (100,100)
        self._parameters = {Button:("Button", pos, font, (100,120,80), (5,0)),
                          TextInput:(pos, font, (100,25)),
                          TextBox:("Text", pos, font),
                          MultiLineTextBox:("Multi-Line Text", pos, font),
                          ProgressBar:(pos, 50, 100, 50),
                          Panel:(pos,),
                          Incrementer:(pos,font,font,(30,30),(20,20),5,[1])}

    def draw(self, screen):
        self._window.fill((255,255,255))
        for w in self._widgets:
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
        for w in self._widgets:
            if type(w) == Button:
                w.handleEvent(event, lambda: None, offset=self._pos)
            if type(w) == TextInput:
                w.handleEvent(event, offset=self._pos)

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
                    for w in self._widgets:
                        if w.getCollideRect().collidepoint(point):
                            self._dragging = (w, event.pos)
                            self._selected = w
        self._p.handleEvent(event)

    def paste(self):
        w = copy.copy(self._copyTemplate)
        w.setPosition((100,100))
        self._widgets.append(w)

    def update(self, ticks):
        self.updateElementDragging()
        if self._selected == None:
            self._p.reset()
        else:
            self._p.update(ticks)
        if self._p._delete:
            self.deleteWidget()
            self._p._delete = False
        if self._p._updateZ:
            self.changeZ()
            self._p._updateZ = False


    def deleteWidget(self):
        w = self._selected
        self._widgets.remove(w)
        self._selected = None

    def updateInterface(self, ticks):
        for w in self._widgets:
            if type(w) == TextInput:
                w.update(ticks)

    def updateElementDragging(self):
        if self._dragging != None:
            b, previous = self._dragging
            current = pygame.mouse.get_pos()
            delta_x = current[0] - previous[0]
            delta_y = current[1] - previous[1]
            b.setPosition((b.getX()+delta_x,
                          b.getY()+delta_y))
            self._dragging = (b, current)
            self._p.createLabels(self._selected, self._widgets.index(self._selected))
            if self._snap:
                self.handleSnapping()
            if not pygame.mouse.get_pressed()[0]:
                self._dragging = None
                self._snappingLines = [None, None]

    def changeZ(self):
        self._widgets.remove(self._selected)
        self._widgets.insert(self._p._z, self._selected)

    def handleSnapping(self):
        self._snappingLines[0] = self.verticalLineSnapping()
        self._snappingLines[1] = self.horizontalLineSnapping()

    def verticalLineSnapping(self):
        wCenter = self.findCenter(self._selected)
        for w in self._widgets:
            if w != self._selected:
                center = self.findCenter(w)
                if abs(wCenter[0] - center[0]) < self._snapSensitivity:
                    x = center[0] - (self._selected.getWidth()//2)
                    self._selected.setPosition((x,self._selected.getY()))
                    return ((wCenter[0],0),(wCenter[0],self._dims[1]))
        return None

    def horizontalLineSnapping(self):
        wCenter = self.findCenter(self._selected)
        for w in self._widgets:
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

    def addWidget(self, widgetType):
        widgetType = eval(widgetType)
        w = widgetType(*self._parameters[widgetType])
        self._widgets.append(w)

    def save(self, fileName="save.txt"):
        with open(fileName, "w") as file:
            for w in self._widgets:
                dec = declarations.getDeclaration(w)
                dec = dec.replace("\n","").replace("\t","")
                file.write(dec + "\n")

    def load(self, fileName="save.txt"):
        self._widgets= []
        self._selected = None
        with open(fileName, "r") as file:
            for line in file:
                self._widgets.append(eval(line))
        
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
        retString += "from polybius.utils import Font\n"
        types = set([type(w) for w in self._widgets])
        for t in types:
            className = t.__name__
            retString += ("from polybius.graphics import %s\n" % (className,))
        retString += "\n"
        return retString

    def writeWidgetsList(self):
        retString = ""
        for w in self._widgets:
            template = "self._widgets.append(%s)\n"
            dec = declarations.getDeclaration(w)
            retString += (template % (dec,))
        return retString

    
        

    
