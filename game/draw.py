#/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import pygame
from pygame.locals import *

#this function should draw blit and and update the part of the screen that needs to be.
def draw(objects, background, screen, rect):

   screen.blit(background, (0, 0))
   for o in objects:
      o.rendered.draw(screen)
   pygame.display.update(rect)
