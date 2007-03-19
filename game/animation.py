#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame
from pygame.locals import *

from variables import *

class Animation:
   def __init__(self, filename, size, ammount):
      self.size = size
      self.frames = loadFrames(filename, ammount, size)
      self.currentFrame = 0

   def changeFrame(frame):
      self.currentFrame = frame
   
   def getCurrentFrame(self):
      return self.frames[self.currentFrame]


def loadFrames(filename, ammount, size, flip=True):
   frameWidth,frameHeight = size
   images = []
   images.append(loadImgPng(filename))
   if flip == True:
      images.append(pygame.transform.flip(loadImgPng(filename), True, False))
   frames = []
   for image in images:
      for i in range(ammount):
         rect = pygame.rect.Rect(i*frameWidth, 0, frameWidth, frameHeight)
         frame = image.subsurface(rect)
         frames.append(frame)
   return frames 
      

