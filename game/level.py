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

   def __init__(self, scene):
      self.scene = scene
      self.level = None # set in self.load()
   
   def load(self, filename):
      """Open file and parse contents. Returns new level object."""
      self.level = Level(self.scene)
      self.propertiesForCell = {}
      self.propertiesForLayer = {}
      self.propertiesForMap = {}
      
      parser = xml.sax.make_parser()
      parser.setContentHandler(self) # Set current object to parse contents of file
      parser.parse(filename)
      return self.level # We have a new level
   
   def startElement(self, name, attributesObj):
      # Create normal dict from attribute object (http://docs.python.org/lib/attributes-objects.html)
      attributes = {}
      for attr, value in attributesObj.items():
         attributes[attr] = value
   
      # If we have a property element later, we have to know what the property is for
      if name in ("cell", "map", "layer"):
         self.propertiesFor = name

      if name == "row":
         self.col = 0
      elif name == "layer":
         self.col, self.row = (0, 0)
         self.position = attributes.get("position", "implicit") # if not found return 2nd arg
         if attributes["name"] == "ladders":
            self.addTileFunc = self.level.addLadder
         else:
            self.addTileFunc = self.level.add
      elif name == "cell":
         self.cellAttributes = attributes # used when cell element ends
      elif name == "property":
         # we add the property to the right dictionary
         if self.propertiesFor == "cell":
            self.propertiesForCell[attributes["name"]] = attributes["value"]
         elif self.propertiesFor == "layer":
            self.propertiesForLayer[attributes["name"]] = attributes["value"]
         elif self.propertiesFor == "map":
            self.propertiesForMap[attributes["name"]] = attributes["value"]

   def endElement(self, name): # called at end of element (<element /> or <element></element>)
      if name == "row":
         self.row += 1
      elif name == "layer":
         self.propertiesForLayer = {} # reset
      elif name == "cell":
         if self.position == "explicit":
            # means we have col and row values in attributes
            cords = (int(self.cellAttributes["col"]), int(self.cellAttributes["row"]))
         else: # default
            cords = (self.col, self.row)
            
         type = int(self.cellAttributes.pop("type", 0)) # Get and remove, or return 2nd arg
         # addTileFunc is set depending on layer (see self.startElement())
         self.addTileFunc(cords, type, self.propertiesForCell)
         
         self.col += 1 # after we've added the tile
         self.propertiesForCell = {} # reset

#    This method is not used right now.
#       
#    def characters(self, content):
#       # Content may be a Unicode-string
#       pass

class Level(object):
   """Level class for levels in the game."""

   def __init__(self, scene):
      self.scene = scene
      self.tiles = pygame.sprite.Group()
      self.noneTiles = pygame.sprite.Group()
      self.backgroundTiles = pygame.sprite.Group()
      self.cloudTiles = pygame.sprite.Group()

   def draw(self, screen):
      # First we remove all none tiles from self.tiles.
      # If we don't, we'll get an error (has no image attribute)
      self.tiles.remove(self.noneTiles)
      self.tiles.draw(screen)
      self.tiles.add(self.noneTiles) # add them again
      
   def getPixelsFromCords(self, cords):
      """Returns X and Y position calculated from column and row position."""
      col, row = cords
      return (col*Tile.WIDTH, row*Tile.HEIGHT)
      
   def getCordsFromPixels(self, pos):
      """Returns column and row position calculated from X and Y position."""
      x, y = pos
      return (int(x/Tile.WIDTH), int(y/Tile.HEIGHT))
       
   def get(self, cords, isCords=False):
      """Returns tile at specified x and y (or column and row) position in map."""
      if isCords:
         cords = pos
      else:
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
      
      if not type: type = Tile.default
      tileClass, tileArgs = Tile.tiles[type]
      tileClass = eval("%sTile" % (tileClass, )) # Get tile class
      tileArgs.update(otherTileArgs) # add (and overwrite) key/value pairs
      
      tile = tileClass(cords, **tileArgs)
      
      self.tiles.add(tile)
      
      if tile.__class__ is NoneTile:
         self.noneTiles.add(tile)
      elif tile.__class__ is BackgroundTile:
         self.backgroundTiles.add(tile)
      elif tile.__class__ is CloudTile:
         self.cloudTiles.add(tile)
   
   def addLadder(self, cords, type, otherTileArgs):
      pass

class Tile(pygame.sprite.Sprite):
   """Generic tile class. Tiles have an image and is not walkable by default.
   
   Inherit from this class to make new kinds of tiles.
   """

   WIDTH, HEIGHT = (20, 20) # Width and height of tiles

   # Tile defaults. Refers to index in tiles array
   default = 0

   # Available tiles.
   # Format: (classname's prefix, dict with arguments passed to class)
   tiles = [("None", {}),
            ("", {"image": "tile-ground-middle.png"}),
            ("", {"image": "tile-ground-left.png"}),
            ("", {"image": "tile-ground-right.png"}),
            ("", {"image": "tile-ground-bottom.png"}),
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
      self.isWalkable = False
      self.isCloud = False
   
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
      self.isWalkable = True
      self.isCloud = False

class BackgroundTile(Tile):
   """The background tiles have an image, but are walkable."""

   def __init__(self, cords, image):
      Tile.__init__(self, cords, image)
      
      self.isWalkable = True

class CloudTile(Tile):
   """Cloud tiles can be entered from any direction, except from the top."""
   
   def __init__(self, cords, image):
      Tile.__init__(self, cords, image)
      
      self.isWalkable = True
      self.isCloud = True
