
import pygame
from polybius.graphics.basics.drawable import Drawable

class AbstractGraphic(Drawable):

    def __init__(self, position, border_radius=0):

        super().__init__("", position, worldBound=False)
        self._keepCenter = False
        self._borderRadius = border_radius

    def center(self, surface=None, cen_point=(1/2,1/2), multisprite=False):

        # Get the fractional coordinates to center around
        cen_x, cen_y = cen_point

        # Determine the dimensions of the surface
        if surface == None: #include normal pygame surfaces here as well
            surface = pygame.display.get_surface()
        
        surf_x = surface.get_width()
        surf_y = surface.get_height()

        # Get half the dimensions of the graphic
        x = self.getWidth() // 2
        y = self.getHeight() // 2

        # Calculate the new x and y position
        if cen_x != None:
            x_pos = int(surf_x * cen_x) - x
        else:
          x_pos = self.getX()
        if cen_y != None:
            y_pos = int(surf_y * cen_y) - y
        else:
            y_pos = self.getY()

        # Handle the offset caused by a multisprite setup
        if multisprite:
            if cen_x!=None: x_pos += surface.getX()
            if cen_y!=None: y_pos += surface.getY()
                    
        self.setPosition((x_pos, y_pos))

    def keepCentered(self, surface=None, cen_point=(1/2,1/2), multisprite=False):
        self._centeringData = (surface, cen_point, multisprite)
        self._keepCenter = True
        self.center(*self._centeringData)

    def turnCenteringOff(self):
        self._keepCenter = False

    def shiftRGBValues(self, color, amount):
        """Shift a tuple of rgb values by a tuple of amounts"""
        assert len(color) == 3
        assert len(amount) == 3
        r,g,b = color
        i,j,k = amount
        return (max(0,min(r+i,255)),
                max(0,min(g+j,255)),
                max(0,min(b+k,255)))

    def updateCentering(self):
        if self._keepCenter:
            self.center(*self._centeringData)

    def updateGraphic(self):
        """A default method for updating a graphic"""

        # Create the canvas that everything will be drawn on
        surfBack = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        surfBack.convert_alpha()

        # Draw the base layer (what will become the border)
        borderRect = pygame.Rect((0,0), (self._width, self._height))
        pygame.draw.rect(surfBack, self._borderColor, borderRect,
                         border_radius=self._borderRadius)

        # Draw the primary surface
        w = max(0, self._width-(self._borderWidth*2))
        h = max(0, self._height-(self._borderWidth*2))
        surf = pygame.Surface((w,h), pygame.SRCALPHA)
        surf.convert_alpha()

        # Apply the background color if not transparent
        if self._backgroundColor != None:
            innerRect = pygame.Rect((0,0),(w,h))
            pygame.draw.rect(surf,self._backgroundColor,
                             innerRect, border_radius=self._borderRadius)
        
        # Add widgets to the primary surface according to kind
        self.internalUpdate(surf)

        # Draw the primary surface onto the base layer
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))

        # Set the image to the created surface
        self._image = surfBack

        # Update the centering on the graphic
        self.updateCentering()

    def getBackgroundColor(self):
        return self._backgroundColor

    def getBorderColor(self):
        return self._borderColor

    def getBorderWidth(self):
        return self._borderWidth

    def setBackgroundColor(self, color):
        self._backgroundColor = color
        self.updateGraphic()

    def setBorderColor(self, color):
        self._borderColor = color
        self.updateGraphic()

    def setBorderWidth(self, width):
        self._borderWidth = width
        self.updateGraphic()

    def getBorderRadius(self):
        return self._borderRadius

    def setBorderRadius(self, radius):
        self._borderRadius = radius
        self.updateGraphic()

    def internalUpdate(self, surf):
        """A placeholder method that can be replaced in child classes"""
        pass
        
        
