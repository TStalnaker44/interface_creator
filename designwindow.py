
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
        
        self._dragging = []
        self._selected = []
        self._copyTemplates = []

        self._snap = True
        self._snapSensitivity = 5
        self._snappingLines = [None, None]
        self._selectBoxCoords = None

        self.defineEvents()

        font = Font("Impact", 20)
        x = self._p._pos[0] + (self._p._backdrop.get_width() // 2 - font.size("Delete")[0] // 2)
        y = self._p._pos[1] + self._p._backdrop.get_height() - font.get_height() - 20
        self._deleteButton = Button("Delete",
                                    (x,y),
                                    font,
                                    backgroundColor=(160,160,160),
                                    borderColor=(100,100,100),
                                    borderWidth=2,
                                    padding=(10,5))

    def defineEvents(self):
        self._dragEvent = EventWrapper(pygame.MOUSEBUTTONDOWN, 1)
        self._mouseUpEvent = EventWrapper(pygame.MOUSEBUTTONUP, 1)
        self._selectAllEvent = EventWrapper(pygame.KEYDOWN, pygame.K_a, [pygame.KMOD_CTRL])
        self._copyEvent = EventWrapper(pygame.KEYDOWN, pygame.K_c, [pygame.KMOD_CTRL])
        self._pasteEvent = EventWrapper(pygame.KEYDOWN, pygame.K_v, [pygame.KMOD_CTRL])
        self._ctrlClick = EventWrapper(pygame.MOUSEBUTTONDOWN, 1, [pygame.KMOD_CTRL])
        self._deleteEvent = EventWrapper(pygame.KEYDOWN, pygame.K_DELETE)

        self._shiftLeftEvent = EventWrapper(pygame.KEYDOWN, pygame.K_LEFT)
        self._shiftRightEvent = EventWrapper(pygame.KEYDOWN, pygame.K_RIGHT)
        self._shiftUpEvent = EventWrapper(pygame.KEYDOWN, pygame.K_UP)
        self._shiftDownEvent = EventWrapper(pygame.KEYDOWN, pygame.K_DOWN)

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
        self.drawBoxesAroundSelected()
        self.drawSelectionBox()
        screen.blit(self._window, self._pos)
        self._p.draw(screen)
        if len(self._selected) > 0:
            self._deleteButton.draw(screen)

    def drawSelectionBox(self):
        if self._selectBoxCoords != None:
            m_pos = pygame.mouse.get_pos()
            m_pos = (m_pos[0] - self._pos[0],
                     m_pos[1] - self._pos[1])
            rect = self.getRectFromCorners(self._selectBoxCoords,m_pos)
            pygame.draw.rect(self._window, (0,0,255), rect, 2)

    def drawSnappingLines(self):
        for line in self._snappingLines:
            if line != None:
                pygame.draw.line(self._window, (0,0,255),
                                 line[0], line[1], 1)
                
    def drawBoxesAroundSelected(self):
        if len(self._selected) > 0:
            for sel in self._selected:
                rect = pygame.Rect(sel.getX()-5,
                                   sel.getY()-5,
                                   sel.getWidth()+10,
                                   sel.getHeight()+10)
                pygame.draw.rect(self._window, (255,0,0), rect, 4)
        
    def handleTestModeEvents(self, event):
        for w in self._widgets:
            if type(w) == Button:
                w.handleEvent(event, lambda: None, offset=self._pos)
            if type(w) == TextInput:
                w.handleEvent(event, offset=self._pos)

    def handleCreateModeEvents(self, event):
        if self._copyEvent.check(event):
            if len(self._selected) > 0:
                self._copyTemplates = self._selected
        if self._pasteEvent.check(event):
            if len(self._copyTemplates) > 0:
                self.paste()
        if self._selectAllEvent.check(event):
            self.selectAll()
        if self._deleteEvent.check(event):
            self.deleteWidgets()
        if not self._p.isActive():
            if self._shiftLeftEvent.check(event): self.shift((-1,0))
            if self._shiftRightEvent.check(event): self.shift((1,0))
            if self._shiftUpEvent.check(event): self.shift((0,-1))
            if self._shiftDownEvent.check(event): self.shift((0,1))
        self.handleWidgetSelection(event)                         
        self._p.handleEvent(event)
        if len(self._selected) > 0:
            self._deleteButton.handleEvent(event, self.deleteWidgets)
        if self._selectBoxCoords != None and self._mouseUpEvent.check(event):
            self.makeSelection()
            self._selectBoxCoords = None

    def makeSelection(self):
        m_pos = pygame.mouse.get_pos()
        m_pos = (m_pos[0] - self._pos[0],
                 m_pos[1] - self._pos[1])
        rect = self.getRectFromCorners(self._selectBoxCoords,m_pos)
        self._selected = []
        for w in self._widgets:
            if w.getCollideRect().colliderect(rect):
                self._selected.append(w)

    def getRectFromCorners(self, c1, c2):
        x1, y1 = c1
        x2, y2 = c2
        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x1-x2)
        height = abs(y1-y2)
        return pygame.Rect((left, top), (width, height))

    def handleWidgetSelection(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            rect = self._window.get_rect()
            point = (event.pos[0] - self._pos[0],
                     event.pos[1] - self._pos[1])
            if rect.collidepoint(point):
                drag = self._dragEvent.check(event)
                ctrl = self._ctrlClick.check(event)
                temp = [s for s in self._selected]
                temp2 = [d for d in self._dragging]
                if drag and not ctrl:
                    self._selected = []
                    self._dragging = []
                selected = None
                dragging = None
                for w in self._widgets:
                    if w.getCollideRect().collidepoint(point):
                        dragging = (w, event.pos)
                        selected = w
                if selected != None:
                    if ctrl and selected in self._selected:
                        self._selected.remove(selected)
                    elif selected in temp:
                        self._selected = temp
                    else:
                        self._selected.append(selected)
                else:
                    self._selectBoxCoords = (event.pos[0] - self._pos[0] ,
                                             event.pos[1] - self._pos[1])
                self._dragging = [(s, event.pos) for s in self._selected]  

    def paste(self):
        self._selected = []
        for widget in self._copyTemplates:
            w = copy.copy(widget)
            w.setPosition((w.getX() + 50, w.getY() + 50))
            self._widgets.append(w)
            self._selected.append(w)

    def selectAll(self):
        self._selected = []
        for w in self._widgets:
            self._selected.append(w)
        if len(self._selected) == 1:
            self._p.createLabels(self._selected[0], self._widgets.index(self._selected[0]))

    def shift(self, amount):
        for w in self._selected:
            x, y = w.getPosition()
            x += amount[0]
            y += amount[1]
            w.setPosition((x,y))
        if len(self._selected) == 1:
            self._p.createLabels(self._selected[0], self._widgets.index(self._selected[0]))
                   
    def update(self, ticks):
        self.updateElementDragging()
        if len(self._selected) != 1:
            self._p.reset()
        else:
            self._p.update(ticks)
        if self._p._updateZ:
            self.changeZ()
            self._p._updateZ = False

    def deleteWidgets(self):
        for w in self._selected:
            self._widgets.remove(w)
        self._selected = []
        self._dragging = []

    def updateInterface(self, ticks):
        for w in self._widgets:
            if type(w) == TextInput:
                w.update(ticks)

    def updateElementDragging(self):
        for i in range(len(self._dragging)):
            b, previous = self._dragging[i]
            current = pygame.mouse.get_pos()
            delta_x = current[0] - previous[0]
            delta_y = current[1] - previous[1]
            b.setPosition((b.getX()+delta_x,
                          b.getY()+delta_y))
            self._dragging[i] = (b, current)
            if len(self._selected) == 1:
                self._p.createLabels(self._selected[0], self._widgets.index(self._selected[0]))
            if self._snap:
                self.handleSnapping()
        if not pygame.mouse.get_pressed()[0]:
            self._dragging = []
            self._snappingLines = [None, None]

    def changeZ(self):
        self._widgets.remove(self._selected[0])
        self._widgets.insert(self._p._z, self._selected[0])

    def handleSnapping(self):   
        if len(self._selected) > 0:
            self._snappingLines[0] = self.verticalLineSnapping()
            self._snappingLines[1] = self.horizontalLineSnapping()

    def verticalLineSnapping(self):
        left, top, width, height = self.getMultiSpriteDims()
        cen = (left + (width//2), top + (height//2))
        for w in self._widgets:
            if not w in self._selected:
                center = self.findCenter(w)
                if abs(cen[0] - center[0]) < self._snapSensitivity:
                    x = center[0] - width//2
                    for sel in self._selected:
                        offset = sel.getX() - left
                        sel.setPosition((offset + x, sel.getY()))
                    return ((cen[0],0),(cen[0],self._dims[1]))
        return None

    def horizontalLineSnapping(self):
        left, top, width, height = self.getMultiSpriteDims()
        cen = (left + (width//2), top + (height//2))
        for w in self._widgets:
            if not w in self._selected:
                center = self.findCenter(w)
                if abs(cen[1] - center[1]) < self._snapSensitivity:
                    y = center[1] - height//2
                    for sel in self._selected:
                        offset = sel.getY() - top
                        sel.setPosition((sel.getX(), offset + y))
                    return ((0,cen[1]), (self._dims[0],cen[1]))
        return None

    def findCenter(self, widget):
        x = widget.getX() + (widget.getWidth()//2)
        y = widget.getY() + (widget.getHeight()//2)
        return (x,y)

    def getMultiSpriteDims(self):
        left = self._selected[0].getX()
        right = self._selected[0].getX() + self._selected[0].getWidth()
        top = self._selected[0].getY()
        bottom = self._selected[0].getY() + self._selected[0].getHeight()
        for w in self._selected:
            left = min(left, w.getX())
            right = max(right, w.getX()+w.getWidth())
            top = min(top, w.getY())
            bottom = max(bottom, w.getY() + w.getHeight())
        width = right - left
        height = bottom - top
        center = ((left + width//2), top + (height//2))
        return (left, top, width, height)
    
    def addWidget(self, widgetType):
        widgetType = eval(widgetType)
        w = widgetType(*self._parameters[widgetType])
        self._widgets.append(w)

    def save(self, filePath):
        with open(filePath, "w") as file:
            for w in self._widgets:
                dec = declarations.getDeclaration(w)
                dec = dec.replace("\n","").replace("\t","")
                file.write(dec + "\n")

    def load(self, filePath):
        self._widgets= []
        self._selected = []
        with open(filePath, "r") as file:
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

    
        

    
