#!/usr/bin/env python
# -*- coding: utf-8 -*-

from variables import *

import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):

   def __init__(self, image, keys):
      pygame.sprite.Sprite.__init__(self)      
      self.image, self.rect = image, image.get_rect()
      self.keyLeft, self.keyRight, self.keyUp = self.keys = keys
      self.xSpeed, self.ySpeed = (1, 0) # xSpeed right = positive; ySpeed up = positive
      self.jumpSpeed = 3.5
   def update(self):
      pass
      
   def move(self, keyInput, levelArray):
      #if self.keys not in keyInput: return
      #oldRect = pygame.Rect(self.rect)
      if keyInput[self.keyUp] and self.onTile(levelArray):
         self.ySpeed = self.jumpSpeed
      if keyInput[self.keyLeft]:
         self.rect.move_ip(-self.xSpeed, 0)
      if keyInput[self.keyRight]:
         self.rect.move_ip(self.xSpeed, 0)
   
   def fall(self): 
      self.ySpeed -= GRAVITY     
      self.rect.move_ip(0, -self.ySpeed) # Because of ySpeed up being positive
      
      
   def checkPosition(self, levelArray):
      """Checks if the player is at the edges of the screen or inside a tile 
      and does apropriate things"""
      self.checkOuterBounds()   
      for i in range(RES_HEIGHT/TILE_HEIGHT):
         for j in range(RES_WIDTH/TILE_WIDTH):
            if levelArray[i][j] is 1:
               tileRect = pygame.Rect(j*TILE_WIDTH, i*TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH)
               if self.rect.colliderect(tileRect):
                  self.correctPosition(tileRect)


   def checkOuterBounds(self):
      if self.rect.x < 0:
         self.rect.x = 0
      if self.rect.y < 0:
         self.rect.y = 0
         self.ySpeed = -GRAVITY
      if self.rect.right > RES_WIDTH:
         self.rect.right = RES_WIDTH
      if self.rect.top > RES_HEIGHT:
         print "you fell down, i'll help you up again"
         self.rect.top = 0
 
   def correctPosition(self, tileRect):
      
      """Correct the position of the player by moving the tile
      acording the penetration of player rect in the tileRect """
      smallestPenetrationDir, smallestPenetration = self.getPenetration(tileRect)
      if smallestPenetrationDir == UP:
         self.rect.move_ip(0, -smallestPenetration)
         self.ySpeed = 0 #so that we stop there and dont fall through the tile
      elif smallestPenetrationDir == RIGHT:
         self.rect.move_ip(smallestPenetration, 0)
         #player.ySpeed = -GRAVITY #not sure if we should have this here or not
      elif smallestPenetrationDir == DOWN:
         self.rect.move_ip(0, smallestPenetration)
         self.ySpeed = -GRAVITY #so that we "bounce" down again
      elif smallestPenetrationDir == LEFT:
         self.rect.move_ip(-smallestPenetration, 0)
         #player.ySpeed = -GRAVITY #not sure if we should have this here or not
      
   def onTile(self, levelArray):
      """Checks if the either player.centerx -5 or +5 (so that we get true when halfways outside) 
      and player.rect.y + height + 1 (so that we get true while standing on top of a tile)
      are inside of a tile, else it returns false"""
      for i in range(RES_HEIGHT/TILE_HEIGHT):
         for j in range(RES_WIDTH/TILE_WIDTH):
            if levelArray[i][j] is 1:
               tileRect = pygame.Rect(j*TILE_WIDTH, i*TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH)         
               if tileRect.collidepoint((self.rect.centerx + 5), (self.rect.y + self.rect.height + 1)) \
               or tileRect.collidepoint((self.rect.centerx - 5), (self.rect.y + self.rect.height + 1)):
                  return True
      return False

   def getPenetration(self, rectTwo):
      """This function is a bit ugly, it should be redone nicer maybe, but it works fine anyway.
      return the smallest direction and ammount of penetration that player.rect does in rectTwo"""
      #get the penetrations in all directions and put them in penetrations
      top = self.rect.bottom - rectTwo.top
      right = rectTwo.right - self.rect.left
      bottom = rectTwo.bottom - self.rect.top
      left = self.rect.right - rectTwo.left
      penetrations = [top, right, bottom, left] 
      #set smallestPenetration and direction to something stupid
      smallestPenetration = 10000
      smallestPenetrationDir = None
      
      #get ths smallest penetration in penetrations
      for penetration in penetrations:
         if penetration < smallestPenetration:
            smallestPenetration = penetration
      
      #get the direction of smallest penetration
      if smallestPenetration==top: 
         smallestPenetrationDir = UP
      elif smallestPenetration==right: 
         smallestPenetrationDir = RIGHT    
      elif smallestPenetration==bottom: 
         smallestPenetrationDir = DOWN
      elif smallestPenetration==left: 
         smallestPenetrationDir = LEFT

      #print smallestPenetrationDir, smallestPenetration
      return smallestPenetrationDir, smallestPenetration
