#!/usr/bin/env python
# -*- coding: utf-8 -*-

from variables import *

import pygame
from pygame.locals import *
      
class Music(object):
   def __init__(self):
      self.isPaused = False
      self.files = []
      for entry in os.listdir(DIR_MUSIC):
         if os.path.isfile(os.path.join(DIR_MUSIC, entry)) and entry.find(".ogg") != -1:
            self.files.append(os.path.join(DIR_MUSIC, entry))
      self.files.sort()
      pygame.mixer.music.load(self.files[0])
      pygame.mixer.music.play()
      for i in range(1,len(self.files)):
         pygame.mixer.music.queue(self.files[i])

   def pause(self):
      if self.isPaused:
         pygame.mixer.music.unpause()
         self.isPaused = False
      else:
         pygame.mixer.music.pause()
         self.isPaused = True
         
class Sound(object):

   def __init__(self):
      self.files = {
      "jump": os.path.join(DIR_SOUND, "jump.wav"),
      "shoot": os.path.join(DIR_SOUND, "shot.wav"),
      "powerup": os.path.join(DIR_SOUND, "powerup.wav"),
      "die": os.path.join(DIR_SOUND, "death.wav")
      }
      
      self.sounds = {}
      for name, file in zip(self.files.keys(), self.files.values()):
         self.sounds[name] = pygame.mixer.Sound(file)
         
   def play(self, name):
      self.sounds[name].play()
