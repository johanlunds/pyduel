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
      self.state = INAIR
   
   def update(self):
      pass
      
   def move(self, keyInput):
      #if self.keys not in keyInput: return
      #oldRect = pygame.Rect(self.rect)
      if keyInput[self.keyUp] :
         self.ySpeed = 3
         self.state = INAIR
      if keyInput[self.keyLeft]:
         self.rect.move_ip(-self.xSpeed, 0)
      if keyInput[self.keyRight]:
         self.rect.move_ip(self.xSpeed, 0)
   
   def fall(self): 
      self.ySpeed -= GRAVITY     
      self.rect.move_ip(0, -self.ySpeed) # Because of ySpeed up being positive
      
   
   def stand(self, tiles):
      if (pygame.sprite.spritecollideany(self, tiles)):
         for tile in tiles:
            smallestPenetrationDir, smallestPenetration = getPenetration(self.rect, tile.rect)
            #if the player is penetration from above, set yspeed to zero, and become jumpable again

            if smallestPenetrationDir == UP:
               self.rect.move_ip(0, -smallestPenetration)
               self.ySpeed = 0
               self.state = STANDING
            #if the penetration is from side or below, we should move out from the tile and continue falling
            elif smallestPenetrationDir == RIGHT:
               self.rect.move_ip(smallestPenetration, 0)
            elif smallestPenetrationDir == DOWN:
               self.rect.move_ip(0, smallestPenetration)
            elif smallestPenetrationDir == LEFT:
               self.rect.move_ip(-smallestPenetration, 0)   
            
         
      
      # http://www.pygame.org/docs/ref/sprite.html groupcollide() etc...

#return the smallest direction and ammount of penetration that rectOne does in rectTwo
def getPenetration(rectOne, rectTwo):
   #get the penetrations in all directions and put them in penetrations
   top = rectOne.bottom - rectTwo.top
   right = rectTwo.right - rectOne.left
   bottom = rectTwo.bottom - rectOne.top
   left = rectOne.right - rectTwo.left
   penetrations = [top, right, bottom, left] 
   #set smallestPenetration and direction to something stupid
   smallestPenetration = 10000
   smallestPenetrationDir = None
   
   #get ths smallest penetration in penetrations
   for penetration in penetrations:
      if penetration < smallestPenetration:
         smallestPenetration = penetration
   
   #get the direction of smallest penetration, a bit haxy
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
