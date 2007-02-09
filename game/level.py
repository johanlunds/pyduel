#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pygame
from pygame.locals import *

class Level(object):
   """Level class for levels in the game. Real levels should inherit from this one."""

   def __init__(self):
      self.tiles = pygame.sprite.Group()
   
   def paint(self):
      #place the tiles, this should be (re)moved
      for i in range(50):
         tile = pygame.image.load(os.path.join(DIR_GRAPH, "tile.png")).convert_alpha()
         if i < 10:
            tile.rect.top = 190+i
            tile.rect.left = 20*i
         elif i < 20:
            tile.rect.top = 300
            tile.rect.left = (20*i)+220
         elif i < 30:
            tile.rect.top = 200-i
            tile.rect.left = (20*i)+450
         else:
            tile.rect.top = 400
            tile.rect.left = (20*i)+120
         self.tiles.add(tile)
