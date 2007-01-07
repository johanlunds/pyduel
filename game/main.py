#/usr/bin/env python
# -*- coding: utf-8 -*-

#import python and pyduel modules
import os, sys
import pygame
from pygame.locals import *

#import project modules which should:
import io      #handle input (and output)
import logic   #handle moving, collision detecting etc.   
import draw    #handle drawing
import obj     #contain the objects

#The main class
class Game:
   def __init__(self):
      #initialize screen
      self.screen = pygame.display.set_mode((640, 480))
      pygame.display.set_caption('PyDuel')
      
      #create objects
      self.charOne = obj.Charactor("man.bmp") 

   #the main loop, where the game runs until it ends ;o
   def mainLoop(self):
      while(1):
         #1 check for input
         key = io.getKbdInput()
         #2 do the logic
         updateRect = logic.move(self.charOne, key)
         #3 draw
         draw.draw(self.charOne.sprite,self.screen,updateRect)

if __name__ == "__main__":
   # Change working directory so that the paths work correctly
   os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
   
   #make an object of the Game class, the main class, and start its main loop.
   pyduel = Game()
   pyduel.mainLoop()
   

