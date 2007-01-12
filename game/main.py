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

#the player class, duh
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
      self.clock = pygame.time.Clock()
      
      #create objects
      self.playerOne = Player("red.bmp", [K_a,K_d,K_w])
      self.playerTwo = Player("blue.bmp", [K_LEFT,K_RIGHT,K_UP])
      self.background = obj.Background()
      
      self.objects = [self.playerOne.sprite, self.playerTwo.sprite]
      self.players = [self.playerOne, self.playerTwo]
      
      self.tiles = []
      for i in range(240):
            self.tiles.append(obj.Sprite("tile.bmp"))   
            self.tiles[i].rect.top=300
            self.tiles[i].rect.left=(i*20)
            self.objects.append(self.tiles[i])
      #draw initial objects and background
      draw.erease(self.background.sprite, self.screen,[(0,0,640,480)])
      draw.draw(self.objects,self.background.sprite, self.screen, [(0,0,640,480)])

   #the main loop, where the game runs until it ends ;o
   def mainLoop(self):

      while(1):
         #0 cap the fps
         self.clock.tick(100)
         #1 check for input
         self.playerTwo.moveDir = self.playerTwo.inp.getKbdInput(self.playerTwo.jumped)
         self.playerOne.moveDir = self.playerOne.inp.getKbdInput(self.playerOne.jumped)
         #2 do the logic
         updateRects = []
         ereaseRects = []
         for p in self.players:
            oldRect, newRect = logic.move(p, p.moveDir)
            ereaseRects.append(oldRect)
            updateRects.append(oldRect)
            updateRects.append(newRect)       
         #3 draw
         draw.erease(self.background.sprite, self.screen, ereaseRects)
         draw.draw(self.objects, self.background.sprite, self.screen, updateRects)
   
if __name__ == "__main__":
   # Change working directory so that the paths work correctly
   os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
   
   #make an object of the Game class, the main class, and start its main loop.
   pyduel = Game()
   pyduel.mainLoop()
   

