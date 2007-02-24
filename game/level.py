#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from variables import *

import pygame
from pygame.locals import *

class Level(object):
   """Level class for levels in the game. Real levels should inherit from this one."""

   def __init__(self, array):
      self.tiles = pygame.sprite.Group()
      self.levelArray = array

   def draw(self, screen):
      for i in range(RES_HEIGHT/TILE_HEIGHT):
         for j in range(RES_WIDTH/TILE_WIDTH):
            if self.levelArray[i][j] is 1:
               tile = Tile(pygame.image.load(os.path.join(DIR_GRAPH, "tile.png")).convert_alpha())
               tile.rect.top = i*TILE_HEIGHT
               tile.rect.left = j*TILE_WIDTH
               self.tiles.add(tile)
      self.tiles.draw(screen)

class Tile(pygame.sprite.Sprite):
   
   def __init__(self, image):
      pygame.sprite.Sprite.__init__(self)
      
      self.image, self.rect = image, image.get_rect()


