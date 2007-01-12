#/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import pygame
from pygame.locals import *
import loadresources 

#this the charactor class, the one which holds the controllable objects
class Sprite(pygame.sprite.Sprite):
   def __init__(self, imageFile):
      pygame.sprite.Sprite.__init__(self) 
      self.image, self.rect = loadresources.load_image(imageFile,(255,0,255))
      self.rendered = pygame.sprite.RenderPlain(self)


class Background:
   def __init__(self):
      self.sprite = pygame.Surface([640,480])
      self.sprite = self.sprite.convert()
      self.sprite.fill((10, 30, 10))



