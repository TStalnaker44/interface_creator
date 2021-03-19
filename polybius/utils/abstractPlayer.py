
import pygame
from polybius.graphics.basics import Animated
from polybius.utils.vector2D import Vector2

class AbstractPlayer(Animated):

    def __init__(self, image, pos, movementKeys, asymmetrical=False):

        if type(image) == str:
            Animated.__init__(self, image, pos)
        elif type(image) == pygame.Surface:
            Animated.__init__(self, "", pos)
            self._image = image
        else:
            raise Exception("Unknown image type for player")
        
        self._velocity = Vector2(0,0)
        self._maxVelocity = 100
        self._acceleration = 0.5
        self._movementKeys = movementKeys ##[l,r,u,d]
        self._movement = {key:False for key in movementKeys}

        self._asymmetrical = asymmetrical

        self._nFrames = 1

##        self._fsm = playerFSM

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self._movementKeys:
                self._movement[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in self._movementKeys:
                self._movement[event.key] = False

    def stop(self):
        for k in self._movement.keys(): self._movement[k] = False

    def setVerticalMovement(self):
        if self._movement[self._movementKeys[2]]:
            self._velocity.y = -self._maxVelocity
##            self._fsm.changeState("walk")
        elif self._movement[self._movementKeys[3]]:
            self._velocity.y = self._maxVelocity
##            self._fsm.changeState("walk")
        else:
            self._velocity.y = 0

    def setHorizontalMovement(self):
        if self._movement[self._movementKeys[0]]:
            self._velocity.x = -self._maxVelocity
            #self._fsm.changeState("walk")
            if self._asymmetrical and not self.isFlipped():
                self.flip()
        elif self._movement[self._movementKeys[1]]:
            self._velocity.x = self._maxVelocity
            #self._fsm.changeState("walk")
            if self._asymmetrical and self.isFlipped():
                self.flip()
        else:
            self._velocity.x = 0

    def manageMovement(self):
        self.setVerticalMovement()
        self.setHorizontalMovement()
##        if self._velocity.x==0 and self._velocity.y==0:
##            self._fsm.changeState("stop")
        self.scaleVelocity()

    def scaleVelocity(self):
        if self._velocity.magnitude() > self._maxVelocity:
            self._velocity.scale(self._maxVelocity)

    def updatePosition(self, ticks, worldInfo):
        newPosition = self._position + (self._velocity * ticks)
##        if newPosition[0] < bounds[0][0]:
##            self._pos[0] = bounds[0][1]
##        if newPosition[0] > bounds[0][1]:
##           self._pos[0] = bounds[0][0]
##        if newPosition[1] < bounds[1][0]:
##           self._pos[1] = bounds[1][1]
##        if newPosition[1] > bounds[1][1]:
##           self._pos[1] = bounds[1][0]
        self._position += (self._velocity * ticks)

    def update(self, ticks, worldInfo):
        self.manageAnimations(ticks)
        self.manageMovement()
        self.updatePosition(ticks, worldInfo)

    ## Abstract Methods ##
    def manageAnimations(self, ticks): pass

    
