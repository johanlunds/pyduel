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
   
   def startElement(self, name, attributes):
      if name == "row": # a new row
         self.col = 0
      elif name == "cell": # a tile
         tile = Tile(int(attributes["type"]), (self.col, self.row))
         self.level.add(tile)

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
      return Tile(0, cords)
   
   def add(self, tile):
      """Add a new tile to map."""
      
      self.tiles.add(tile)
      
   def draw(self, screen):
      self.tiles.draw(screen)
      
   def getCordsFromPixels(self, pos):
      """Returns column and row position calculated from X and Y position."""
      
      x, y = pos
      return (int(x/Tile.WIDTH), int(y/Tile.HEIGHT))

class Tile(pygame.sprite.Sprite):

   WIDTH, HEIGHT = (20, 20) # Width and height of tiles

   # Available tiles.
   tiles = (None, "tile-ground-middle.png",  "tile-ground-left.png", "tile-ground-right.png", "tile-ground-bottom.png")  
   #forgroundTiles = ("tile-tree-bottom.png", "tile-tree-top.png", "tile-bush.png",  ) 
   
   def __init__(self, type, cords):
      pygame.sprite.Sprite.__init__(self)
      
      if Tile.tiles[type] is not None: # Check so we don't try to load empty image
         self.image = loadImgPng(Tile.tiles[type])
         self.walkable = False
      else:
         self.image = pygame.Surface((Tile.WIDTH, Tile.HEIGHT))
         self.walkable = True
      
      self.newPos(cords)
   
   def newPos(self, cords):
      """Change position of tile in map. Column and row position. Also sets self.rect"""
      
      self.col, self.row = cords
      self.rect = pygame.Rect(Tile.WIDTH*self.col, Tile.HEIGHT*self.row, Tile.WIDTH, Tile.HEIGHT)
