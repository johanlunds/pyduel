#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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
     
      playerOne = Player(self, "player-red.png", (K_a, K_d, K_w, K_s, K_SPACE))
      playerTwo = Player(self, "player-blue.png", (K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RETURN))
      
      self.players = pygame.sprite.Group(playerTwo, playerOne)
      self.levelLoader = LevelLoader(self)
      self.loadLevel(0) # First level
   
   def loadLevel(self, levelNumber):
      self.levelNumber = levelNumber
      self.level = self.levelLoader.load(self.levelLoader.__class__.levels[levelNumber]) # use level list from level loader's class
   
   def event(self, event):
      pass

   def loop(self):
      pygame.event.pump()
      keyInput = pygame.key.get_pressed()
      self.players.update(keyInput, self.level)
   
   def update(self):
      self.players.clear(self.game.screen, self.background)
      self.level.backgroundTiles.clear(self.game.screen, self.background)
      self.level.cloudTiles.clear(self.game.screen, self.background)
      self.level.cloudTiles.draw(self.game.screen)
      self.level.backgroundTiles.draw(self.game.screen)
      self.players.draw(self.game.screen)
        
   def draw(self):
      self.level.draw(self.game.screen)
      self.players.draw(self.game.screen)

def main():
   pyduel = Game(RESOLUTION, CAPTION, ICON)
   firstScene = Duel(pyduel)
   pyduel.start(firstScene) # Start the game with a new Duel scene
   raise SystemExit, 0

if __name__ == "__main__":
   main()
