#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from engine import Game, Scene
from level import LevelLoader
from player import Player
from variables import *

import pygame
from pygame.locals import *

class Duel(Scene):
   """The main game scene. Where the players fight against eachother."""
   
   def __init__(self, game):
      Scene.__init__(self, game)
      
      playerOne = Player(loadImgPng("red.png"), (K_a, K_d, K_w))
      playerTwo = Player(loadImgPng("blue.png"), (K_LEFT, K_RIGHT, K_UP))
      
      self.players = pygame.sprite.Group(playerTwo, playerOne)
      self.currentLevel = LevelLoader().load(os.path.join(DIR_LEVELS, "1.xml"))
      
   def event(self, event):
      pass

   def loop(self):
      pygame.event.pump()
      keyInput = pygame.key.get_pressed()
      for player in self.players:
         player.move(keyInput, self.currentLevel)
         player.fall()
         player.checkPosition(self.currentLevel)
      self.players.update()
   
   def update(self):
      self.players.clear(self.game.screen, self.background)
      self.players.draw(self.game.screen)
        
   def draw(self):
      self.currentLevel.draw(self.game.screen)
      self.players.draw(self.game.screen)

def main():
   # Change working directory so that the paths work correctly
   os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
   
   pyduel = Game(RESOLUTION, CAPTION, ICON)
   firstScene = Duel(pyduel)
   pyduel.start(firstScene) # Start the game with a new Duel scene
   raise SystemExit, 0

if __name__ == "__main__":
   main()
