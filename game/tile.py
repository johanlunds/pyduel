#!/usr/bin/env python
# -*- coding: utf-8 -*-

from variables import *

import pygame
from pygame.locals import *

class Tile(pygame.sprite.Sprite):
   """Generic tile class. Don't use this directly, inherit from this one.
   
   If you're making a tile for the "normal" layer, inherit from NormalTile instead.
   """

   WIDTH, HEIGHT = (20, 20) # Width and height of tiles

   # Tile defaults. Refers to index in tiles array
   default = 0
   ladderDefault = 11

   # Available tiles.
   # Format: (classname's prefix, dict with arguments passed to class)
   tiles = [("None", {}),
            ("Normal", {"image": "tile-ground-middle.png"}),
            ("Normal", {"image": "tile-ground-left.png"}),
            ("Normal", {"image": "tile-ground-right.png"}),
            ("Normal", {"image": "tile-ground-bottom.png"}),
            ("Background", {"image": "tile-tree-bottom.png"}),
            ("Background", {"image": "tile-tree-top.png"}),
            ("Background", {"image": "tile-bush.png"}),
            ("Cloud", {"image": "tile-ground-cloud-middle.png"}),
            ("Cloud", {"image": "tile-ground-cloud-left.png"}),
            ("Cloud", {"image": "tile-ground-cloud-right.png"}),
            ("Ladder", {"image": "tile-ladder.png"})]
   
   def __init__(self, cords, image, *args):
      pygame.sprite.Sprite.__init__(self)
      
      self.image = loadImgPng(image) # lazy loading of images.
      self.newPos(cords)
   
   def newPos(self, cords):
      """Change position of tile in map. Column and row position. Also sets self.rect"""
      self.col, self.row = cords
      self.rect = pygame.Rect(Tile.WIDTH*self.col, Tile.HEIGHT*self.row, Tile.WIDTH, Tile.HEIGHT)

class NormalTile(Tile):
   """The normal (ground) tile. Is not walkable by default.
   
   Inherit from this tile if you're using the tile in the "normal" layer.
   """
   
   def __init__(self, cords, image):
      Tile.__init__(self, cords, image)
      
      self.isWalkable = False
      self.isCloud = False
      # Child tiles
      self.ladder = None

class NoneTile(NormalTile):
   """The none tile have no image and is walkable. Used in places where there isn't any other tile."""
   
   def __init__(self, cords):
      pygame.sprite.Sprite.__init__(self) # Don't use NormalTile.__init__() because it loads an image.
      
      self.image = None
      self.newPos(cords) # We have to set this manually (we don't use NormalTile.__init__())
      self.isWalkable = True
      self.isCloud = False
      self.ladder = None

class BackgroundTile(NormalTile):
   """The background tiles have an image, but are walkable."""

   def __init__(self, cords, image):
      NormalTile.__init__(self, cords, image)
      
      self.isWalkable = True

class CloudTile(NormalTile):
   """Cloud tiles can be entered from any direction, except from the top."""
   
   def __init__(self, cords, image):
      NormalTile.__init__(self, cords, image)
      
      self.isWalkable = True
      self.isCloud = True
      
class LadderTile(Tile): # Ladder tiles is not in "normal" layer, so inherit from Tile
   """Ladder tiles can be climbed on."""
   
   def __init__(self, cords, image):
      Tile.__init__(self, cords, image)
