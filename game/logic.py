#/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
gravity = 0.05
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

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

   #check for collision with the tiles
   for tile in tiles:
      #check if the player is inside the tile
      if collisionCheck(player.sprite.rect, tile.rect):  
         #set jumped and yspeed to the value they should have
         player.jumped = True
         player.yspeed = 1
         #get the smallest penetration and what direction that is
         smallestPenetrationDir, smallestPenetration = getPenetration(player.sprite.rect, tile.rect)
         #if the player is penetration from above, set yspeed to zero, and becom jumpable again
         if smallestPenetrationDir == UP:
            player.sprite.rect.top = player.sprite.rect.top - smallestPenetration
            player.yspeed = 0
            player.jumped = False
         #if the penetration is from side or below, we should move out from the tile and continue falling
         elif smallestPenetrationDir == RIGHT:
            player.sprite.rect.left = player.sprite.rect.left + smallestPenetration
         elif smallestPenetrationDir == DOWN:
            player.sprite.rect.top = player.sprite.rect.top + smallestPenetration
         elif smallestPenetrationDir == LEFT:
            player.sprite.rect.left = player.sprite.rect.left - smallestPenetration

   #set newRect to the new position of the object, then return both the new and the old positions
   newRect = player.sprite.rect
   return(oldRect, newRect)

#return true if the rects are colliding, else return false
def collisionCheck(rectOne, rectTwo):
   if rectOne.bottom < rectTwo.top: return False
   if rectOne.right < rectTwo.left: return False
   if rectOne.top > rectTwo.bottom: return False
   if rectOne.left > rectTwo.right: return False
   return True


#return the smallest direction and ammount of penetration that rectOne does in rectTwo
def getPenetration(rectOne, rectTwo):

   #get the penetrations in all directions and put them in penetrations
   top = rectOne.bottom - rectTwo.top
   right = rectTwo.right - rectOne.left
   bottom = rectTwo.bottom - rectOne.top
   left = rectOne.right - rectTwo.left
   penetrations = [top, right, bottom, left] 
   #set smallestPenetration and direction to something stupid
   smallestPenetration = 100
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




