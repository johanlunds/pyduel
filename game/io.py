#/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import pygame
from pygame.locals import *

#Returns the key from the keyboard input, None if nothing is pressed and quits if exit is pressed
def getKbdInput():
   for event in pygame.event.get():
      if event.type == pygame.QUIT: 
         sys.exit()
      if event.type == KEYDOWN:
         if event.key == K_LEFT:
            return('LEFT')
         if event.key == K_RIGHT:
            return('RIGHT')
       
   return None;
