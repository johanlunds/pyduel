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

class Player:
   def __init__(self, image, keys):
      self.sprite = obj.Sprite(image)
      self.inp = io.Input(keys)
      self.moveDir = None
      self.yspeed = 0
      self.jumped = True

#The main class
class Game:
   def __init__(self):
      #initialize screen
      self.screen = pygame.display.set_mode((640, 480))
      pygame.display.set_caption('PyDuel')
      
      #create objects
      self.playerOne = Player("red.bmp", [K_a,K_d,K_w])
      self.playerTwo = Player("blue.bmp", [K_LEFT,K_RIGHT,K_UP])
      self.background = obj.Background()
      
      self.objects = [self.playerOne.sprite, self.playerTwo.sprite]
      #draw initial objects and background
      draw.draw(self.objects,self.background.sprite, self.screen,(0,0,640,480))

   #the main loop, where the game runs until it ends ;o
   def mainLoop(self):
      while(1):
         #1 check for input
         self.playerTwo.moveDir = self.playerTwo.inp.getKbdInput(self.playerTwo.jumped)
         self.playerOne.moveDir = self.playerOne.inp.getKbdInput(self.playerOne.jumped)
         #2 do the logic
         rect1 = logic.move(self.playerOne, self.playerOne.moveDir)
         rect2 = logic.move(self.playerTwo, self.playerTwo.moveDir)
                  
         #updateRect = rect1.union(rect2)
         updateRect = 0,0,640,480
         #3 draw
         draw.draw(self.objects,self.background.sprite, self.screen,updateRect)
   
if __name__ == "__main__":
   # Change working directory so that the paths work correctly
   os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
   
   #make an object of the Game class, the main class, and start its main loop.
   pyduel = Game()
   pyduel.mainLoop()
   

