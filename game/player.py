#!/usr/bin/env python
# -*- coding: utf-8 -*-

from variables import *

import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):

   def __init__(self, image, keys):
      pygame.sprite.Sprite.__init__(self)
      
      self.image, self.rect = image, image.get_rect()
      self.keyLeft, self.keyRight, self.keyUp = self.keys = keys
      self.xSpeed, self.ySpeed = (1, 0) # xSpeed right = positive; ySpeed up = positive
      self.jumped = False
   
   def update(self):
      pass
      
   def move(self, key):
      if key not in self.keys: return
      
      oldRect = pygame.Rect(self.rect)
      
      if key == self.keyUp and not self.jumped:
         self.ySpeed = 3
         self.jumped = True
      elif key == self.keyLeft:
         self.rect.move(-self.xSpeed, 0)
      elif key == self.keyRight:
         self.rect.move(self.xSpeed, 0)
      
      self.ySpeed -= GRAVITY
      self.rect.move(0, -self.ySpeed) # Because of ySpeed up being positive
      
      # http://www.pygame.org/docs/ref/sprite.html groupcollide() etc...
