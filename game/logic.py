#/usr/bin/env python
# -*- coding: utf-8 -*-

gravity = -0.05

#this should move our Charactor and return the rectangle which needs to be update
def move(obj, key):
   movedRect = obj.sprite.rect
   if key == 'JUMP':
      if obj.jumped == False:
         obj.yspeed = 3
         obj.jumped = True
   if key == 'RIGHT':
      obj.sprite.rect.left = obj.sprite.rect.left + 1
   if key == 'LEFT':
      obj.sprite.rect.left = obj.sprite.rect.left - 1

   if (obj.sprite.rect.bottom > 300):
      obj.yspeed=0.5
      obj.jumped=False  
   obj.yspeed = obj.yspeed + gravity
   obj.sprite.rect.top = obj.sprite.rect.top - obj.yspeed
   movedRect = movedRect.union(obj.sprite.rect)
   return(movedRect) 


