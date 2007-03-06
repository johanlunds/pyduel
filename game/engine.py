#!/usr/bin/env python
# -*- coding: utf-8 -*-

from variables import *

import pygame
from pygame.locals import *

class Game(object):
   """Not very useful except from initializing a Pygame window and the game."""
   
   FRAMERATE = 75
   
   def __init__(self, resolution, caption=None, icon=None):
      pygame.init()
      if not (pygame.mixer or pygame.font): raise SystemExit, "Missing required Pygame mixer and/or font modules."
      
      self.screen = pygame.display.set_mode(resolution)
      if caption:
         pygame.display.set_caption(caption)
      if icon:
         icon = pygame.image.load(icon).set_colorkey((255, 0, 255)) # pink
         pygame.display.set_icon(icon)

      self.clock = pygame.time.Clock()
   
   def tick(self):
      """Limits framerate. Call in game loop."""
      self.clock.tick(Game.FRAMERATE)
   
   def start(self, initialScene):
      initialScene.run()

class SceneExit(Exception):
   """Raised at point of exit from a scene."""
   pass

class Scene(object):
   """Different game modes (menu, the duel, highscores) should inherit from this one."""
   
   def __init__(self, game, background = None):
      self.game = game
      self.background = pygame.Surface(self.game.screen.get_size()).convert() # Temporary
      self.background.fill((0, 0, 0)); # Temporary
   
   def end(self, retVal):
      """Call this one if you want to end a scene."""
      self.returnValue = retVal
      raise SceneExit
   
   def runScene(self, scene):
      """Run another scene and continue with current after."""
      retVal = scene.run()
      self.draw()
      return retVal
   
   def run(self):
      self.game.screen.blit(self.background, (0, 0))
      self.draw()
      pygame.display.flip()
      
      while 1:
         self.game.tick()
         for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
               raise SystemExit, 0
            try:
               self.event(event)
            except SceneExit:
               return self.returnValue
         try:
            self.loop()
         except SceneExit:
            return self.returnValue
         self.update()
         pygame.display.flip()
   
   def event(self, event):
      """Events from pygame.event.get() in the main loop."""
      pass
   
   def loop(self):
      """Called in main loop after checking for, and handling, events."""
      pass
   
   def update(self):
      """Should position game objects (and do other things?) in the scene"""
      pass
   
   def draw(self):
      """Called before the loop starts in the scene. Supposed to draw whole scene. Calls self.update() by default."""
      self.update()
