
import pygame
from polybius.graphics import Button, TextInput
from polybius.utils import EventWrapper

class DesignWindow():

    def __init__(self, pos=(0,0), dims=(600,600)):

        self._pos = pos
        self._dims = dims
        self._window = pygame.Surface(self._dims)

        # Create font dictionaries
        self._font2Name = {}
        self._name2Font = {}
        self._widget2Font = {}

        self._buttons = []
        self._textInputs = []
        self._dragging = None

        self._makeButtonEvent = EventWrapper(pygame.MOUSEBUTTONDOWN, 3)
        self._makeTextInputEvent = EventWrapper(pygame.MOUSEBUTTONDOWN, 3, [pygame.KMOD_CTRL])
        self._dragEvent = EventWrapper(pygame.MOUSEBUTTONDOWN, 1)

    def draw(self, screen):
        self._window.fill((255,255,255))
        for b in self._buttons:
            b.draw(self._window)
        for t in self._textInputs:
            t.draw(self._window)
        screen.blit(self._window, self._pos)

    def handleTestModeEvents(self, event):
        for b in self._buttons:
            b.handleEvent(event, lambda: None, offset=self._pos)
        for t in self._textInputs:
            t.handleEvent(event, offset=self._pos)

    def handleCreateModeEvents(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            rect = self._window.get_rect()
            point = (event.pos[0] - self._pos[0],
                     event.pos[1] - self._pos[1])
            if rect.collidepoint(point):
                if self._dragEvent.check(event):
                    for w in self._buttons + self._textInputs:
                        if w.getCollideRect().collidepoint(point):
                            self._dragging = (w, event.pos)

    def updateElementDragging(self):
        if self._dragging != None:
            b, previous = self._dragging
            current = pygame.mouse.get_pos()
            delta_x = current[0] - previous[0]
            delta_y = current[1] - previous[1]
            b.setPosition((b.getX()+delta_x,
                          b.getY()+delta_y))
            self._dragging = (b, current)
            if not pygame.mouse.get_pressed()[0]:
                self._dragging = None

    def makeButton(self, pos):
        text = "Button"
        font = self._name2Font["font1"]
        b = Button(text, pos, font,
                   (100,120,80), (5,0))
        self._buttons.append(b)
        self._widget2Font[b] = font

    def makeTextInput(self, pos):
        font = self._name2Font["font1"]
        t = TextInput(pos, font, (100,25))
        self._textInputs.append(t)
        self._widget2Font[t] = font

    def addFont(self, name, font, size):
        f = pygame.font.SysFont(font, size)
        self._font2Name[f] = (name, font, size)
        self._name2Font[name] = f

    def export(self):
        retString = self.writeImports()
        retString += "class Interface(AbstractInterface):\n\n"
        retString += "\tdef __init__(self):\n"
        retString += "\t\tAbstractInterface.__init__(self)\n"
        for name, font, size in self._font2Name.values():
            retString += ("\t\t%s = pygame.font.SysFont('%s', %s)\n" %
                          ("self._"+name, font, size))
        
        for line in self.writeWidgetsList().split("\n"):
            retString += "\t\t" + line + "\n"
        with open("export.py", "w") as file:
            for line in retString:
                file.write(line)
        

    def writeImports(self):
        retString = "import pygame\n"
        retString += "from polybius.abstractInterface import AbstractInterface\n"
        retString += "from polybius.graphics import Button, TextInput\n\n"
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
        return retString

    def getButtonDeclaration(self, button):
        txt = button.getText()
        pos = button.getPosition()
        pos = ("(%d,%d)" % (pos[0], pos[1]))
        backgroundColor = "backgroundColor=" + str(button._backgroundColor)
        padding = "padding=" + str(button._padding)
        font = ("self._%s" % (self._font2Name[self._widget2Font[button]][0],))
        return ("Button('%s', %s, %s, %s, %s)" %
                (txt, pos, font, backgroundColor, padding))

    def getTextInputDeclaration(self, tinput):
        dims = (tinput.getWidth(), tinput.getHeight())
        pos = tinput.getPosition()
        pos = ("(%d,%d)" % (pos[0], pos[1]))
        font = ("self._%s" % (self._font2Name[self._widget2Font[tinput]][0],))
        return ("TextInput(%s, %s, %s)" % (pos, font, dims))
        

    
