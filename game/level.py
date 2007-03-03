#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xml.sax.handler
from variables import *

import pygame
from pygame.locals import *

class LevelLoader(xml.sax.handler.ContentHandler):
   """For loading levels from XML-files. More info: http://docs.python.org/lib/module-xml.sax.handler.html"""

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
         self.row += 1
         self.col = 0
      if name == "cell": # a tile
         tile = Tile(int(attributes["type"]), self.col, self.row)
         self.level.add(tile)
         self.col += 1

#    These methods are not used right now.
#       
#    def characters(self, content):
#       # Content may be a Unicode-string
#       pass
#    
#    def endElement(self, name):
#       pass

class Level(object):
   """Level class for levels in the game."""

   maxLevels = 1 # scan dir after *.map or some like that. To do!

   def __init__(self):
      self.tiles = pygame.sprite.Group()
      # self.currentLevel = 1 # number of currentLevel. Not used right now
   
   def get(self, col, row):
      """Returns tile at specified column and row position in map."""
      for tile in self.tiles.sprites():
         if tile.col == col and tile.row == row:
            return tile
   
   def add(self, tile):
      """Add a new tile to map."""
      self.tiles.add(tile)
      
   def draw(self, screen):
      self.tiles.draw(screen)

class Tile(pygame.sprite.Sprite):

   WIDTH, HEIGHT = (20, 20) # Width and height of tiles
   
   # Available tiles.
   tiles = (None, "tile-ground-middle.png",  "tile-ground-left.png", "tile-ground-right.png", "tile-ground-bottom.png")  
   #forgroundTiles = ("tile-tree-bottom.png", "tile-tree-top.png", "tile-bush.png",  ) 
   
   def __init__(self, number, col, row):
      pygame.sprite.Sprite.__init__(self)
      
      if Tile.tiles[number] is not None: # Check so we don't try to load empty image
         image = loadImgPng(Tile.tiles[number])
         self.image = image
         self.isNone = False
      else:
         self.image = pygame.Surface((Tile.WIDTH, Tile.HEIGHT))
         self.isNone = True
      
      self.newPos(col, row)
   
   def newPos(self, col, row):
      """Change position of tile in map. Column and row position. Also sets self.rect"""
      
      self.col = col
      self.row = row
      self.rect = pygame.Rect(Tile.WIDTH*self.col, Tile.HEIGHT*self.row, Tile.WIDTH, Tile.HEIGHT)
