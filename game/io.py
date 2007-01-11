#/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import pygame
from pygame.locals import *

#Returns the key from the keyboard input, None if nothing is pressed and quits if exit is pressed
class Input:
   def __init__(self,keys):
      self.keyLeft, self.keyRight,  self.keyUp = keys
      self.keyLeftPressed = False
      self.keyRightPressed = False

   def getKbdInput(self, jumped):
      pygame.event.pump()
      keyInput = pygame.key.get_pressed()
      if keyInput[self.keyUp] and jumped==False:
         return 'JUMP'      
      if keyInput[self.keyLeft]:
         return 'LEFT'
      elif keyInput[self.keyRight]:
         return 'RIGHT'
      #check if we want to quit, either with esc or 
      if keyInput[K_ESCAPE]:
         sys.exit()

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
				sys.exit()

      
