#!/usr/bin/env python
# -*- coding: utf-8 -*-

from variables import *

import os, copy
import xml.sax.handler

# import tile classes (Tile, NoneTile etc)
from tile import *

import pygame
from pygame.locals import *

class LevelLoader(xml.sax.handler.ContentHandler):
   """For loading levels from XML-files. More info: http://docs.python.org/lib/module-xml.sax.handler.html"""

   # List all available levels with absolute paths
   # The list is sorted, so just use next item in list to load next level
   levels = [os.path.join(DIR_LEVELS, entry) for entry in os.listdir(DIR_LEVELS) if os.path.isfile(os.path.join(DIR_LEVELS, entry))]
   levels.sort()

   def __init__(self, scene):
      self.scene = scene
      self.level = None # set in self.load()
   
   def load(self, filename):
      """Open file and parse contents. Returns new level object."""
      self.level = Level(self.scene)
      self.elementTree = [] # Used to keep track of current element and it's parents
      self.propertiesForCell = {}
      self.propertiesForLayer = {}
      self.propertiesForMap = {}
      
      parser = xml.sax.make_parser()
      parser.setContentHandler(self) # Set current object to parse contents of file
      parser.parse(filename)
      return self.level # We have a new level
   
   def startElement(self, name, attributes):
      # Remember: attributes is not dict but attribute object (see xml.sax.handler.ContentHandler docs)
      # To convert we could use: attributes = dict(attributes.items()))
      
      self.elementTree.append(name)

      if name == "row":
         self.col = 0
      elif name == "layer":
         self.col, self.row = (0, 0)
         self.position = attributes.get("position", "implicit") # if not found return 2nd arg
         self.isPlayerLayer = False
         if attributes["name"] == "ladders":
            self.typeDefault = Tile.ladderDefault
         elif attributes["name"] == "items":
            self.typeDefault = Tile.itemDefault
         elif attributes["name"] == "players": # available player start positions
            self.isPlayerLayer = True
         else:
            self.typeDefault = Tile.default
      elif name == "cell":
         # save attributes. used when cell element ends. 
         self.cellAttributes = copy.copy(attributes) # need to copy object (see xml.sax.handler.ContentHandler docs)
      elif name == "property":
         # convert from possible unicode str
         self.propertyName = attributes["name"]
         self.propertyType = attributes.get("type", "int") # defaults to int (change to str?)
         if self.propertyType not in ("int", "float", "long", "str", "unicode", "eval"): # allowed types
            # we haven't got valid value, raise exception with msg and exit
            raise StandardError, 'Element "property" has attribute "type" with invalid value.'

   def endElement(self, name): # called at end of element (<element /> or <element></element>)
      self.elementTree.pop() # remove last item
   
      if name == "map":
         self.level.loaded()
      elif name == "row":
         self.row += 1
      elif name == "layer":
         self.propertiesForLayer = {} # reset
      elif name == "cell":
         if self.position == "explicit":
            # means we have col and row values in attributes
            cords = (int(self.cellAttributes["col"]), int(self.cellAttributes["row"]))
         else: # default
            cords = (self.col, self.row)
         
         if self.isPlayerLayer:
            self.level.startPos.append(cords)
         else:
            type = int(self.cellAttributes.get("type", self.typeDefault)) # Get and remove, or return 2nd arg
            self.level.add(cords, type, self.propertiesForCell)
         
         self.col += 1 # after we've added the tile
         self.propertiesForCell = {} # reset
      
   def characters(self, content):
      # Only used for property-elements right now
      
      if self.elementTree[-1] != "property": return # we're not in a property-element
      propertyFor = self.elementTree[-2] # second to last (-1 is the last)
      
      key = str(self.propertyName) # can be unicode wich don't work with keyword arguments
      # convert to right type. possible values: see self.startElement() for "property"
      value = eval(self.propertyType)(content)
      
      # we add the property to the right dictionary
      if propertyFor == "cell":
         self.propertiesForCell[key] = value
      elif propertyFor == "layer":
         self.propertiesForLayer[key] = value
      elif propertyFor == "map":
         self.propertiesForMap[key] = value

class Level(object):
   """Level class for levels in the game."""

   def __init__(self, scene, theme):
      self.scene = scene
      self.theme = theme
      self.startPos = [] # Available start positions. Format: (col, row)
      
      self.tilesArray = {}
      self.tiles = pygame.sprite.Group()
      self.noneTiles = pygame.sprite.Group()
      self.backgroundTiles = pygame.sprite.Group()
      self.cloudTiles = pygame.sprite.Group()
      self.ladderTiles = pygame.sprite.Group()
      self.itemTiles = pygame.sprite.Group()

   def draw(self, screen):
      # First we remove all none tiles from self.tiles.
      # If we don't, we'll get an error (has no image attribute)
      self.tiles.remove(self.noneTiles)
      self.tiles.draw(screen)
      self.tiles.add(self.noneTiles) # add them again
      
      self.ladderTiles.draw(screen) # because is not in "normal" layer
      self.itemTiles.draw(screen)
      
   def getPixelsFromCords(self, cords):
      """Returns X and Y position calculated from column and row position."""
      col, row = cords
      return (col*Tile.WIDTH, row*Tile.HEIGHT)
      
   def getCordsFromPixels(self, pos):
      """Returns column and row position calculated from X and Y position."""
      x, y = pos
      return (int(x/Tile.WIDTH), int(y/Tile.HEIGHT))
   
   def loaded(self):
      """Level has been loaded into Level-object."""
      # All tiles becomes a property
      # of the correct tile in self.tiles (col and row is compared)
      for ladder in self.ladderTiles:
         tile = self.get((ladder.col, ladder.row), True)
         tile.ladder = ladder
      for item in self.itemTiles:
         tile = self.get((item.col, item.row), True)
         tile.item = item
       
   def get(self, pos, isCords=False):
      """Returns tile at specified x and y (or column and row) position in map."""
      if isCords:
         cords = pos
      else:
         cords = self.getCordsFromPixels(pos)
      
      # We use self.tilesArray (dict) instead of self.tiles (sprite group)
      # because it's faster instead of looping through the whole group
      try:
         return self.tilesArray[cords]
      except KeyError:
         # If there's no tile at the coordinates (outside of screen for example)
         # then return dummy-tile (prevents errors)      
         return NoneTile(self, cords)
   
   def add(self, cords, type, otherTileArgs):
      """Add a new tile to map."""
      # Note: otherTileArgs is a dict with ONLY string-values (may have to convert)
      # It will override the arguments in Tile.tiles array.
      
      tileClass, tileArgs = Tile.tiles[type]
      tileClass = eval("%sTile" % (tileClass, )) # Get tile class
      tileArgs.update(otherTileArgs) # add (and overwrite) key/value pairs
      
      tile = tileClass(self, cords, **tileArgs)
      
      if tile.__class__ is NoneTile:
         self.noneTiles.add(tile)
      elif tile.__class__ is BackgroundTile:
         self.backgroundTiles.add(tile)
      elif tile.__class__ is CloudTile:
         self.cloudTiles.add(tile)
      elif tile.__class__ is LadderTile:
         self.ladderTiles.add(tile)
         return # We don't want to add to self.tiles
      elif tile.__class__ is ItemTile or issubclass(tile.__class__, ItemTile):
         self.itemTiles.add(tile)
         return
      
      self.tiles.add(tile)
      self.tilesArray[cords] = tile # used to find tiles based on pos in self.get()
