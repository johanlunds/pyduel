#/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import pygame
from pygame.locals import *
import loadresources 

#this the charactor class, the one which holds the controllable objects
class Charactor(pygame.sprite.Sprite):
   def __init__(self, imageFile):
      pygame.sprite.Sprite.__init__(self) 
      self.image, self.rect = loadresources.load_image(imageFile,-1)
      self.sprite = pygame.sprite.RenderPlain(self)

