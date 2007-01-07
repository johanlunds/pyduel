#/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import pygame
from pygame.locals import *

#this function should draw blit and and update the part of the screen that needs to be.
def draw(sprite, screen, rect):

   sprite.draw(screen)
   pygame.display.update(rect)
