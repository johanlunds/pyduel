#/usr/bin/env python
# -*- coding: utf-8 -*-

#this should move our Charactor and return the rectangle which needs to be updated
def move(obj, key):
   if key == 'RIGHT':
      print("Right key pressed")
      obj.rect.left = obj.rect.left + 1
      
   if key == 'LEFT':
      print("Left key pressed")
      obj.rect.left = obj.rect.left - 1

   movedRect = 0,0,640,480   
   return(movedRect) 
