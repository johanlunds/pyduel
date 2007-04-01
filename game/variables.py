#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Define variables and constants used all over in the game."""

import os, sys

import pygame
from pygame.locals import *

GRAVITY = 1 # Move to level files?

# Change working directory so that the paths work correctly
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

DIR_GRAPH = os.path.join("data", "graphic")
DIR_SOUND = os.path.join("data", "sound")
DIR_MUSIC = os.path.join("data", "music")
DIR_FONT = os.path.join("data", "font")
DIR_LEVELS = "levels"

# Used in game initiation. May be removed later
CAPTION = "PyDuel"
RESOLUTION = RES_WIDTH, RES_HEIGHT = (640, 480)
ICON = None # No icon right now

UP, RIGHT, DOWN, LEFT = range(4) # Directions

MAX_HEALTH = 100 # for players

loadImg = lambda path: pygame.image.load(os.path.join(DIR_GRAPH, path)).convert()
loadImgPng = lambda path: pygame.image.load(os.path.join(DIR_GRAPH, path)).convert_alpha()

class SurroundingTiles(object):
   """Help class. Holds variables for surrounding (and center) tiles."""
   
   def __init__(self, rect, scene):
      self.forRect = rect
      self.getFunc = scene.level.get # Function used to fetch tiles
      self.setCenter()
      self.setSides()
      self.setCorners()
      
   def setCenter(self):
      rect = self.forRect
      self.center = self.getFunc((rect.centerx, rect.centery))
      
   def setSides(self):
      rect = self.forRect
      self.left = self.getFunc((rect.left, rect.centery))
      self.right = self.getFunc((rect.right, rect.centery))
      self.top = self.getFunc((rect.centerx, rect.top))
      self.bottom = self.getFunc((rect.centerx, rect.bottom))
      
   def getSides(self):
      return (self.top, self.right, self.bottom, self.left) # Return in clockwise order
   
   def setCorners(self):
      rect = self.forRect
      self.topLeft = self.getFunc((rect.left, rect.top))
      self.topRight = self.getFunc((rect.right, rect.top))
      self.bottomLeft = self.getFunc((rect.left, rect.bottom))
      self.bottomRight = self.getFunc((rect.right, rect.bottom))
   
   def getCorners(self):
      # Return in clockwise order, starting with topleft (maybe should be topright)
      return (self.topLeft, self.topRight, self.bottomRight, self.bottomLeft)
