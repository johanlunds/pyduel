#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pygame
from pygame.locals import *

"""Define variables and constants used all over in the game."""

GRAVITY = 0.05 # Move to level files?

DIR_GRAPH = os.path.join("data", "graphic")
DIR_SOUND = os.path.join("data", "sound")
DIR_MUSIC = os.path.join("data", "music")
DIR_FONT = os.path.join("data", "font")
DIR_LEVELS = "levels"

loadImg = lambda path: pygame.image.load(os.path.join(DIR_GRAPH, path)).convert()
loadImgPng = lambda path: pygame.image.load(os.path.join(DIR_GRAPH, path)).convert_alpha()

# Used in game initiation. May be removed later
CAPTION = "PyDuel"
RESOLUTION = RES_WIDTH, RES_HEIGHT = (640, 480)
ICON = None # No icon right now

UP, RIGHT, DOWN, LEFT = range(4)
