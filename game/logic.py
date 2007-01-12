#/usr/bin/env python
# -*- coding: utf-8 -*-
import draw
gravity = -0.05

#this should move our Charactor and return the rectangle which needs to be update
def move(obj, key):
   oldRect = obj.sprite.rect
   #jump by setting 'yspeed' positive, and set 'jumpped' flag to true
   if key == 'JUMP':
      obj.yspeed = 3
      obj.jumped = True
   #move left or right
   if key == 'RIGHT':
      obj.sprite.rect.left = obj.sprite.rect.left + 1
   if key == 'LEFT':
      obj.sprite.rect.left = obj.sprite.rect.left - 1

   #when we have a nive ground this should change
   if (obj.sprite.rect.bottom > 300):
      obj.yspeed=0.5
      obj.jumped=False
   
   #fall!  
   obj.yspeed = obj.yspeed + gravity
   obj.sprite.rect.top = obj.sprite.rect.top - obj.yspeed
   
   newRect = obj.sprite.rect
   return(oldRect, newRect) 


