#/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import pygame
from pygame.locals import *

#blit background in ereaseRects
def erease(background, screen, ereaseRects):
   for rect in ereaseRects:
      screen.blit(background, rect, rect)

      

#blit objects and update the the areas which need to be
def draw(objects, background, screen, draw):
   for o in objects:
      o.rendered.draw(screen)

   pygame.display.update(draw)
