#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xml.sax.handler
from variables import *

import pygame
from pygame.locals import *

class LevelLoader(xml.sax.handler.ContentHandler):
   """For loading levels from XML-files. More info: http://docs.python.org/lib/module-xml.sax.handler.html"""

   # List all available levels with absolute paths
   # The list is sorted, so just use next item in list to load next level
   levels = filter(os.path.isfile, [os.path.join(DIR_LEVELS, entry) for entry in os.listdir(DIR_LEVELS)])

   def __init__(self):
      self.level = None # set in self.load()
      self.col = 0
      self.row = 0
   
   def load(self, filename):
      """Open file and parse contents. Returns new level object."""
      self.level = Level()
      self.col = 0
      self.row = 0
      
      parser = xml.sax.make_parser()
      parser.setContentHandler(self) # Set current object to parse contents of file
      parser.parse(filename)
      return self.level # We have a new level
   
   def startElement(self, name, attributesObject):
      if name == "row": # a new row
         self.col = 0
      elif name == "cell": # a tile
         # Create normal dict from attribute object (http://docs.python.org/lib/attributes-objects.html)
         # we pass this variable on to other functions
         attributes = {}
         for attr, value in attributesObject.items():
            attributes[attr] = value
         
         cords = (self.col, self.row)
         type = int(attributes.pop("type", 0)) # Get and remove, or return 0 (2nd arg)
         self.level.add(cords, type, attributes)

   def endElement(self, name): # called at end of element (<element /> or <element></element>)
      if name == "row":
         self.row += 1
      elif name == "cell":
         self.col += 1

#    This method is not used right now.
#       
#    def characters(self, content):
#       # Content may be a Unicode-string
#       pass

class Level(object):
   """Level class for levels in the game."""

   def __init__(self):
      self.tiles = pygame.sprite.Group()
      self.noneTiles = pygame.sprite.Group()
      self.backgroundTiles = pygame.sprite.Group()
   
   def get(self, cords, isPixels=False):
      """Returns tile at specified column and row (or x and y px) position in map."""
      
      if isPixels:
         cords = self.getCordsFromPixels(cords)
      
      col, row = cords
      
      for tile in self.tiles:
         if tile.col == col and tile.row == row:
            return tile
      
      # If there's no tile at the coordinates (outside of screen for example)
      # then return dummy-tile (prevents errors)
      return NoneTile(cords)
   
   def add(self, cords, type, otherTileArgs):
      """Add a new tile to map."""
      
      # Note: otherTileArgs is a dict with ONLY string-values (may have to convert)
      # It will override the arguments in Tile.tiles array.
      
      tileClass, tileArgs = Tile.tiles[type]
      tileClass = eval("%sTile" % (tileClass, )) # Get tile class
      tileArgs.update(otherTileArgs) # add (and overwrite) key/value pairs
      
      tile = tileClass(cords, **tileArgs)
      
      self.tiles.add(tile)
      
      if tile.__class__ is NoneTile:
         self.noneTiles.add(tile)
      elif tile.__class__ is BackgroundTile:
         self.backgroundTiles.add(tile)
      
   def draw(self, screen):
      # First we remove all none tiles from self.tiles.
      # If we don't, we'll get an error (has no image attribute)
      self.tiles.remove(self.noneTiles)
      self.tiles.draw(screen)
      self.tiles.add(self.noneTiles) # add them again
      
   def getCordsFromPixels(self, pos):
      """Returns column and row position calculated from X and Y position."""
      
      x, y = pos
      return (int(x/Tile.WIDTH), int(y/Tile.HEIGHT))

class Tile(pygame.sprite.Sprite):
   """Generic tile class. Tiles have an image and is not walkable by default.
   
   Inherit from this class to make new kinds of tiles.
   """

   WIDTH, HEIGHT = (20, 20) # Width and height of tiles

   # Available tiles.
   # Format: (classname's prefix, dict with arguments passed to class)
   tiles = [("None", {}),
            ("", {"image": "tile-ground-middle.png"}),
            ("", {"image": "tile-ground-left.png"}),
            ("", {"image": "tile-ground-right.png"}),
            ("", {"image": "tile-ground-bottom.png"}),
            ("Background", {"image": "tile-tree-bottom.png"}),
            ("Background", {"image": "tile-tree-top.png"}),
            ("Background", {"image": "tile-bush.png"})]
   
   def __init__(self, cords, image, *args):
      pygame.sprite.Sprite.__init__(self)
      
      self.image = loadImgPng(image) # lazy loading of images. Todo: comment more. explain
      self.newPos(cords)
      self.walkable = False
   
   def newPos(self, cords):
      """Change position of tile in map. Column and row position. Also sets self.rect"""
      
      self.col, self.row = cords
      self.rect = pygame.Rect(Tile.WIDTH*self.col, Tile.HEIGHT*self.row, Tile.WIDTH, Tile.HEIGHT)

class NoneTile(Tile):
   """The none tile have no image and is walkable. Used in places where there isn't any other tile."""
   
   def __init__(self, cords):
      pygame.sprite.Sprite.__init__(self) # Don't use Tile.__init__() because it loads an image.
      
      self.image = None
      self.newPos(cords) # We have to set this manually (we don't use Tile.__init__())
      self.walkable = True

class BackgroundTile(Tile):
   """The background tiles have an image, but are walkable."""

   def __init__(self, cords, image):
      Tile.__init__(self, cords, image)
      
      self.walkable = True