
import pygame
from polybius.graphics.basics import Animated
from polybius.utils.vector2D import Vector2

class AbstractPlayer(Animated):

    def __init__(self, pos, image, movementKeys):

        Animated.__init__(self, image, pos)
        self._velocity = Vector2(0,0)
        self._maxVelocity = 100
        self._acceleration = 0.5
        self._movementKeys = movementKeys ##[l,r,u,d]
        self._movement = {key:False for key in movementKeys}

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

    def setHorizontalMovement(self, asymmetrical=False):
        if self._movement[self._movementKeys[0]]:
            self._velocity.x = -self._maxVelocity
            #self._fsm.changeState("walk")
            if asymmetrical and not self.isFlipped():
                self.flip()
        elif self._movement[self._movementKeys[1]]:
            self._velocity.x = self._maxVelocity
            #self._fsm.changeState("walk")
            if asymmetrical and self.isFlipped():
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

    def updatePosition(self):
        pass

    def update(self, worldInfo):
        self.manageAnimations(ticks)
        self.manageMovement()
        self.updatePosition(ticks, worldInfo)

    ## Abstract Methods ##
    def manageAnimations(self, ticks): pass

    
