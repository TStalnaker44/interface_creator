
import pygame
from polybius.abstractGame import AbstractGame
from polybius.abstractLevel import AbstractLevel
from polybius.graphics import Drawable
from polybius.utils.abstractPlayer import AbstractPlayer
from polybius.managers import FRAMES
from polybius.utils.doubleclickevent import DoubleClickEvent
from polybius.graphics import Tabs
from polybius.utils import Font
from polybius.graphics import Checkbox, Slider, RadioButton, \
     RadioButtons,DropDownList, Button
from polybius.graphics import ImageButton
from polybius.graphics.utils.borders import Borders

class Sandbox(AbstractGame):

    def __init__(self):
        AbstractGame.__init__(self, (1000,600), "Sandbox")
        self._level = Main(self.getScreenSize())
        self.addLevel("main", self._level)
        self._level2 = Main(self.getScreenSize())
        self.addLevel("main2", self._level2)
        self.switchTo("main")
        
    def handleEvent(self, event):
        code = self._level.checkForExitCode()
        if code != None:
            self.switchTo("main2")
            return
        code = self._level2.checkForExitCode()
        if code != None:
            self.switchTo("main")
            return
        if event.type == pygame.KEYDOWN:
            print(event.key)

        
class Main(AbstractLevel):

    def __init__(self, screenSize):

        AbstractLevel.__init__(self, screenSize)
        surf = pygame.Surface((100,100))
        surf.fill((255,0,0))
        FRAMES.prepareImage("dude.png", colorKey=True)
        FRAMES.prepareImage("background.png", (5000,5000))
        self._back = Drawable("background.png", (0,0))
        self._player1 = StickMan((10,10))
        movement = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]
        self._player2 = AbstractPlayer(surf, (25,25), movement)
        self.setTrackingObject(self._player1)
        self.setWorldSize((5000,5000))
        self._doubleClickEvent = DoubleClickEvent(self._player2.getCollideRect())
        font = Font("Impact", 20)
        self._tabs = Tabs(["First", "Second"], (100,100), font, (255,255,255),
                          (0,0,0), (600,50), (255,0,0), (0,0,0), maxTabWidth=100)

        self._checkbox = Checkbox((200,200),symbol = "X",backgroundColor = (240,120,34),isChecked = True)
        self._radioButton = RadioButton((300,300),text = "Test the damn thing",radius = 30,textPadding = 5,font = font)
        self._slider = Slider((250,250), minValue=0, maxValue=100, defaultValue=50)

        options = ["Cat","Dog","Mouse","Cow"]
        self._radioButtons = RadioButtons((400,100),options,selectedIndex = 1,
                                          vertical=False, padding=15)
        self._radioButtons.setSelectedColor((255,0,0))
        self._radioButtons.setFont(font)
        self._radioButtons.addButton("Horse")

        self._dropdownlist = DropDownList((100,400),options)


        FRAMES.prepareImage("buttonImages/playButton.png", colorKey=True)
        FRAMES.prepareImage("buttonImages/playButtonPressed.png", colorKey=True)
        self._imageButton = ImageButton((350,500), "playButton.png",
                                        pressedImage="playButtonPressed.png")


        FRAMES.prepareImage("buttonImages/watchButton.png", colorKey=True)
        FRAMES.prepareImage("buttonImages/pressedWatchButton.png", colorKey=True)
        FRAMES.prepareImage("buttonImages/watchButtonHover.png", colorKey=True)
        self._imageButton2 = ImageButton((600,250), "watchButton.png",
                                        pressedImage="pressedWatchButton.png",
                                         hoverImage="watchButtonHover.png")

        self._borderSurf = pygame.Surface((200,200))
        self._borderSurf.fill((244, 244, 115))
        self._borders = Borders([2,2,2,2],[(0,0,255),(0,0,0),(0,0,0),(0,0,0)])
    def draw(self, screen):
        self._back.draw(screen)
        self._player1.draw(screen)
        self._player2.draw(screen)
##        self._tabs.draw(screen)
##        self._checkbox.draw(screen)
##        self._slider.draw(screen)
        self._radioButton.draw(screen)
        self._radioButtons.draw(screen)

        self._dropdownlist.draw(screen)
        
        self._imageButton.draw(screen)
        self._imageButton2.draw(screen)

        self._borders.draw(self._borderSurf)
        screen.blit(self._borderSurf, (300, 100))

##        x = 100
##        y = 400
##        dims = (100,100)
##        num = 5
##        for i in range(num+1):
##            rect = pygame.Rect((x,y),dims)
##            radius = int((i / num) * (dims[0]/2))
##            pygame.draw.rect(screen, (0,0,0), rect, border_radius=radius)
##            x += dims[0] + 50

    def handleEvent(self, event):
        self._player1.handleEvent(event)
        self._player2.handleEvent(event)
        self._checkbox.handleEvent(event)
        self._radioButton.handleEvent(event)
        self._radioButtons.handleEvent(event)
        self._dropdownlist.handleEvent(event)
        if event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE:
            current = self.getTrackingObject()
            if current == self._player1:
                self.setTrackingObject(self._player2)
            else:
                self.setTrackingObject(self._player1)
        if event.type == pygame.KEYDOWN and event.key==pygame.K_u:
            self.setExitCode((1,))

        if self._doubleClickEvent.check(event):
            print(self._tabs.getActive())
        self._tabs.handleEvent(event)
        if event.type == pygame.KEYDOWN and event.key==pygame.K_m:
            self._tabs.addTab("Third")

        self._slider.handleEvent(event)
        #print(self._slider.getValue())

        if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            self._slider.setValue(67)

        self._imageButton.handleEvent(event, self.doNothing)
        self._imageButton2.handleEvent(event, self.doNothing)

    def doNothing(self):
        pass

    def update(self, ticks):
        self._player1.update(ticks, self.getWorldSize(), "bounce")
        self._player2.update(ticks, self.getWorldSize(), "torus")

class StickMan(AbstractPlayer):

    def __init__(self, pos):
        movement = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        super().__init__("dude.png", pos, movement, True)

    def manageAnimations(self, ticks):
        state = self.getCurrentState()
        if state == "standing":
            self.setRowOnSpriteSheet(1)
            self.setFramesInRow(1)
        if state == "walking":
            self.setRowOnSpriteSheet(0)
            self.setFramesInRow(2)
        self.updateAnimation(ticks)

g = Sandbox()
g.run()
