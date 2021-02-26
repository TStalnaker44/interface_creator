
import pygame
from polybius.abstractGame import AbstractGame
from polybius.graphics import Button, TextInput
from polybius.utils import EventWrapper
from export import Interface

class Game(AbstractGame):

    def __init__(self):
        AbstractGame.__init__(self, (500,500), "New Game")
        self.getScreen().fill((255,0,0))

        self._font2Name = {}
        self._name2Font = {}
        self._widget2Font = {}

        self.addFont("font1","Arial",16)
        
        self._buttons = []
        self._textInputs = []
        self._dragging = None

        self._testMode = False

        self._exportEvent = EventWrapper(pygame.KEYDOWN,
                                         pygame.K_SPACE)

        self._toggleModeEvent = EventWrapper(pygame.KEYDOWN, pygame.K_m)

        self._makeButtonEvent = EventWrapper(pygame.MOUSEBUTTONDOWN, 3)
        self._makeTextInputEvent = EventWrapper(pygame.MOUSEBUTTONDOWN, 3, [pygame.KMOD_CTRL])

        self._count = 0

        self._i = Interface()
    
    def draw(self, screen):
        self.getScreen().fill((255,0,0))
        for b in self._buttons:
            b.draw(screen)
        for t in self._textInputs:
            t.draw(screen)
        self._i.draw(screen)

    def handleEvent(self, event):
        # Toggle between test and create modes
        if self._toggleModeEvent.check(event):
            self._testMode = not self._testMode
        if self._testMode:
            self.handleTestModeEvents(event)
        else:
            self.handleCreateModeEvents(event)

    def handleTestModeEvents(self, event):
        for b in self._buttons:
            b.handleEvent(event, self.doNothing)
        for t in self._textInputs:
            t.handleEvent(event)
        self._i.handleEvent(event)

    def handleCreateModeEvents(self, event): 
        if self._makeTextInputEvent.check(event):
            self.makeTextInput(event.pos)
        elif self._makeButtonEvent.check(event):
            self.makeButton(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and \
           event.button == 1:
            for w in self._buttons + self._textInputs:
                if w.getCollideRect().collidepoint(event.pos):
                    self._dragging = (w, event.pos)
        if self._exportEvent.check(event):
            self.export()
              
    def update(self, ticks):
        self.updateElementDragging()
            
    def doNothing(self):
        pass

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
        text = "Button " + str(self._count)
        font = self._name2Font["font1"]
        b = Button(text, pos, font,
                   (100,120,80), (5,0))
        self._buttons.append(b)
        self._widget2Font[b] = font
        self._count += 1

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

g = Game()
g.run()
