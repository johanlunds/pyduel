#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from engine import Game, Scene
from level import LevelLoader
from player import Player
from variables import *
from menu import Menu

import pygame
from pygame.locals import *

class Duel(Scene):
   """The main game scene. Where the players fight against eachother."""
   
   def __init__(self, game):
      Scene.__init__(self, game)
     
      playerOne = Player(self, loadImgPng("player-red.png"), (K_a, K_d, K_w, K_s, K_SPACE))
      playerTwo = Player(self, loadImgPng("player-blue.png"), (K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RETURN))
      
      self.players = pygame.sprite.Group(playerTwo, playerOne)
      self.levelLoader = LevelLoader(self)
      self.loadLevel(1) # First level
   
   def loadLevel(self, levelNumber):
      self.levelNumber = levelNumber
      self.level = self.levelLoader.load(self.levelLoader.__class__.levels[levelNumber]) # use level list from level loader's class
   
   def event(self, event):
      if event.type == KEYDOWN and event.key == K_ESCAPE:
         self.end(0)


   def loop(self):
      pygame.event.pump()
      keyInput = pygame.key.get_pressed()
      self.players.update(keyInput)
   
   def update(self):
      self.level.tiles.remove(self.level.noneTiles) # why? see Level.draw()
      
      self.players.clear(self.game.screen, self.background)
      self.level.tiles.clear(self.game.screen, self.background)
      self.level.ladderTiles.clear(self.game.screen, self.background)
      self.level.itemTiles.clear(self.game.screen, self.background)
      
      self.level.tiles.draw(self.game.screen)
      self.level.ladderTiles.draw(self.game.screen)
      self.level.itemTiles.draw(self.game.screen)
      self.players.draw(self.game.screen)
      
      self.level.tiles.add(self.level.noneTiles)
        
   def draw(self):
      self.game.screen.blit(self.background, (0, 0))
      self.level.draw(self.game.screen)
      self.players.draw(self.game.screen)


class MainMenu(Scene):
   def __init__(self, game,lines):
      Scene.__init__(self, game)
      self.menu = Menu(lines)

   def loop(self):
      self.menu.headerSlide()
      
   def event(self, event):      
      if event.type == KEYDOWN and event.key == K_ESCAPE: # Escape pressed => Exit.
         self.end(0)   
      if event.type == KEYDOWN and event.key == K_DOWN:  # Check for keyp up/down and set new selection
         if (self.menu.selection < self.menu.ammount-1):
            self.menu.selection += 1
      if event.type == KEYDOWN and event.key == K_UP:
         if (self.menu.selection > 0):
            self.menu.selection += -1 
      if event.type == KEYDOWN and event.key == K_RETURN: # Check for enter and do action
         if self.menu.selection == 0:
            self.runScene(Duel(self.game))
         if self.menu.selection == 1:
            self.runScene(OptionsMenu(self.game, ("Timelimit: ", "Option 2", "Back")))
         if self.menu.selection == 2:
            self.end(0)
   
   def update(self):
      self.menu.update(self.game.screen, self.background)

class OptionsMenu(Scene):
   def __init__(self, game, lines):
      Scene.__init__(self, game)
      self.timelimit = 0
      self.menu = Menu(lines)
   
   def event(self, event):
      if event.type == KEYDOWN and event.key == K_ESCAPE:  # Escape pressed => End scene.
         self.end(0)    
      if event.type == KEYDOWN and event.key == K_DOWN: # Check for keyp up/down and set new selection
         if (self.menu.selection < self.menu.ammount-1):
            self.menu.selection += 1
      if event.type == KEYDOWN and event.key == K_UP:
         if (self.menu.selection > 0):
            self.menu.selection += -1
      if event.type == KEYDOWN and event.key == K_RETURN:  # Check for enter and do action
         if self.menu.selection == 0:
            self.timelimit += 1
            self.menu.textlinesInactive[0].setString("Timelimit: %d" % self.timelimit) 
            self.menu.textlinesActive[0].setString("Timelimit: %d" % self.timelimit) 
         if self.menu.selection == 1:
            pass
         if self.menu.selection == 2:
            self.end(0)
   
   def loop(self):
      self.menu.headerSlide()

   def update(self):
      self.menu.update(self.game.screen, self.background)

   def saveOptions(self):
      pass

def main():
   pyduel = Game(RESOLUTION, CAPTION, ICON)
   firstScene = MainMenu(pyduel,("New Game","Options","Quit"))
   pyduel.start(firstScene)
   raise SystemExit, 0

if __name__ == "__main__":
   main()
