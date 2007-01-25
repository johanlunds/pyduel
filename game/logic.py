#/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
gravity = 0.05

#this should move our Charactor and return the rectangle which needs to be update
def move(player, key, tiles):

   #copy so that we can alter player.sprite.rect without altering oldRect
   oldRect = copy.copy(player.sprite.rect)

   #jump by setting 'yspeed' negative (upwards), and set 'jumpped' flag to true
   if key == 'JUMP':
      player.yspeed = -3
      player.jumped = True
   #move left or right
   if key == 'RIGHT':
      player.sprite.rect.left = player.sprite.rect.left + player.xspeed
   if key == 'LEFT':
      player.sprite.rect.left = player.sprite.rect.left - player.xspeed
   
   #fall!  
   player.yspeed = player.yspeed + gravity
   player.sprite.rect.top = player.sprite.rect.top + player.yspeed

   
   #print player.yspeed
   for tile in tiles:
      #if we are inside a tile and going down
      if collisionCheck(player.sprite.rect, tile.rect): 
         if player.sprite.rect.top < tile.rect.top: 
            penetration = player.sprite.rect.bottom - tile.rect.top 
            player.sprite.rect.top = player.sprite.rect.top - penetration
            player.yspeed = 0
            player.jumped=False
            #print "stay!"
         else: 
            #player.sprite.rect.top = tile.rect.bottom
            player.yspeed = 1
            

      """if we are inside a tile and going upwards
      if collisionCheck(player.sprite.rect,tile.rect) and player.yspeed < 0:
         player.yspeed=0.5
         player.jumped=True
         print "fall!"""
         

   
   #set newRect to the new position of the object, then return both the new and the old positions
   newRect = player.sprite.rect
   return(oldRect, newRect)

def collisionCheck(rectOne, rectTwo):
   if rectOne.bottom < rectTwo.top: return False
   if rectOne.right < rectTwo.left: return False
   if rectOne.top > rectTwo.bottom: return False
   if rectOne.left > rectTwo.right: return False
   #if rectOne.bottom > rectTwo.bottom: return False
   return True



