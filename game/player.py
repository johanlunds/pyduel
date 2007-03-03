#!/usr/bin/env python
# -*- coding: utf-8 -*-

from variables import *

import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):

   JUMPSPEED = 3.5

   def __init__(self, image, keys):
      pygame.sprite.Sprite.__init__(self)
      
      self.image, self.rect = image, image.get_rect()
      self.keyLeft, self.keyRight, self.keyUp = self.keys = keys
      self.xSpeed, self.ySpeed = (1, 0) # xSpeed right = positive; ySpeed up = positive
      
   def update(self):
      pass
      
   def move(self, keyInput, level):
      if keyInput[self.keyUp] and self.onTile(level):
         self.ySpeed = Player.JUMPSPEED
      if keyInput[self.keyLeft]:
         self.rect.move_ip(-self.xSpeed, 0)
      if keyInput[self.keyRight]:
         self.rect.move_ip(self.xSpeed, 0)
   
   def fall(self): 
      self.ySpeed -= GRAVITY     
      self.rect.move_ip(0, -self.ySpeed) # Because of ySpeed up being positive
      
   def checkPosition(self, level):
      """Checks if the player is at the edges of the screen or inside a tile and does apropriate things."""
      self.checkOuterBounds()   
      for tile in level.tiles:
         if not tile.isWalkable and self.rect.colliderect(tile.rect):
            self.correctPosition(tile)

   def checkOuterBounds(self):
      if self.rect.left < 0:
         self.rect.left = 0
      if self.rect.top < 0:
         self.rect.top = 0
         self.ySpeed = 0
      if self.rect.right > RES_WIDTH:
         self.rect.right = RES_WIDTH
      if self.rect.top > RES_HEIGHT:
         self.rect.top = 0 # Move to top of screen if falled all the way down
 
   def correctPosition(self, tile):
      """Correct the position of the player by moving the tile
      acording the penetration of player rect in the tileRect """
      smallestPenetrationDir, smallestPenetration = self.getPenetration(tile.rect)
      if smallestPenetrationDir == UP:
         self.rect.move_ip(0, -smallestPenetration)
         self.ySpeed = 0 # so that we stop there and dont fall through the tile
      elif smallestPenetrationDir == RIGHT:
         self.rect.move_ip(smallestPenetration, 0)
      elif smallestPenetrationDir == DOWN:
         self.rect.move_ip(0, smallestPenetration)
         self.ySpeed = 0 # so that we "bounce" down again
      elif smallestPenetrationDir == LEFT:
         self.rect.move_ip(-smallestPenetration, 0)

   def onTile(self, level):
      """Checks if player is standing on a tile."""
      for tile in level.tiles:
         if not tile.isWalkable:
            # Return true when +/- 5 px from centerx (halfways outside)
            if tile.rect.collidepoint(self.rect.centerx+5, self.rect.bottom+1) \
            or tile.rect.collidepoint(self.rect.centerx-5, self.rect.bottom+1):
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
