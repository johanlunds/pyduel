#!/usr/bin/env python
# -*- coding: utf-8 -*-

from variables import *
from animation import Animation
from math import ceil

import pygame
from pygame.locals import *

class HUD(object):
   """This is HUD class"""
   def __init__(self, playerOneName, playerTwoName, maxAmmo):     
      self.background = pygame.Surface((RES_WIDTH,20)).convert()
      self.background.fill((0, 0, 0))
      self.background.set_alpha(180)
      self.rect = pygame.Rect(0,0,RES_WIDTH,20)
      
      self.playerOneHUD = PlayerHUD(playerOneName, 0, maxAmmo)
      self.playerTwoHUD = PlayerHUD(playerTwoName, RES_WIDTH/2, maxAmmo)
      
   def update(self, status):
      """Update status images and blit everython on background"""
      for playerHUD, i in zip((self.playerOneHUD, self.playerTwoHUD ), range(2)):
         health, ammo = status[i]
         playerHUD.health.changeFrame(health)
         playerHUD.ammo.changeFrame(ammo)
         self.background.blit(playerHUD.textName.surface, playerHUD.textName.rect)
         self.background.blit(playerHUD.textHealth.surface, playerHUD.textHealth.rect)
         self.background.blit(playerHUD.health.image, playerHUD.health.rect)
         self.background.blit(playerHUD.textAmmo.surface, playerHUD.textAmmo.rect)
         self.background.blit(playerHUD.ammo.image, playerHUD.ammo.rect)
   
   def clear(self, screen, background):
      """blit level.background and refill background to remove previous blits"""
      screen.blit(background, self.rect, self.rect)
      self.background.fill((0, 0, 0)) # Fill to erease from previous blits

   def draw(self, screen):
      """blit background (with everything on) onto screen)"""
      screen.blit(self.background, self.rect, self.rect)
      
   
class PlayerHUD(object):
   """Holds the elements of the hud of one player"""
   def __init__(self, name, xpos, maxAmmo):
      self.textName = Text(name.title(), (xpos + 10,3))
      self.textHealth = Text("Health:", (self.textName.rect.right + 10 ,3), (255,50,50))
      self.health = Status(100, (self.textHealth.rect.right + 10,6))
      self.textAmmo = Text("Ammo: ", (self.health.rect.right + 10,3), (50,50,255))
      self.ammo = Status(30, (self.textAmmo.rect.right + 10,6))
      
class Text(object):
   """Text class used for writing"""
   pygame.font.init()
   font = pygame.font.Font(os.path.join(DIR_FONT, "vera.ttf"), 12)
   
   def __init__(self, text, pos, color=(255, 255, 255)):
         self.string = text
         self.color = color
         self.surface = Text.font.render(self.string , True, self.color)
         self.rect = self.surface.get_rect()
         self.rect.move_ip(pos)
         
   
class Status(object):
   """Status class is used for displaying health and ammo status with various frames"""
   A_FRAMES = 10
   def __init__(self, max, pos):
      self.max = float(max)
      self.image = loadImgPng("hud-status.png")
      self.animation = Animation(self)
      self.image, self.rect = self.animation.loadFrames(self.image, Status.A_FRAMES)
      self.rect.move_ip(pos)
      normal = zip(range(Status.A_FRAMES), Status.A_FRAMES * (5, ))
      self.animation.addSequence("normal", normal) # 5 = dummy speed, not used
      self.image = self.animation.getFrame(0)
      self.animation.stop()
      
   def changeFrame(self, status):
      frame = 10 - int(ceil(status / self.max * 10))
      if frame > Status.A_FRAMES - 1: frame = Status.A_FRAMES - 1 # Don't go higher than max index
      if frame < 0: frame = 0 # Don't go lower than 0
      self.image = self.animation.getFrame(frame)
