
import pygame
from polybius.graphics import Drawable

class Board(Drawable):

    def __init__(self, pos, tiles=None, colorMap=None, tileDims=(32,32),
                 tileMap=None):

        super().__init__("", pos)

        rowCount = len(tiles)
        columnCount = len(tiles[0])

        boardDims = (tileDims[0]*columnCount,
                     tileDims[1]*rowCount)

        # Create the board surface
        board = pygame.Surface(boardDims, pygame.SRCALPHA)
        board.convert_alpha()

        # Create a tile mapping if one was not provided
        if tileMap == None:
            tileMap = {}
            for k, v in colorMap.items():
                tile = pygame.Surface(tileDims)
                #tile.convert_alpha()
                if not v == None:
                    tile.fill(v)
                else:
                    tile = None 
                tileMap[k] = tile

        # Draw the board using the tiles
        for row in range(rowCount):
            for column in range(columnCount):
                ypos = row * tileDims[0]
                xpos = column * tileDims[1]
                tileType = tiles[row][column]
                tile = tileMap[tileType]
                if tile != None:
                    board.blit(tile, (xpos, ypos))

        # Save the board surface as this object's image
        self._image = board
