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
      self.level.draw(self.game.screen)
      self.players.draw(self.game.screen)

class Menu(Scene):
   """menu class, atm just for the main menu. I'll add options menu later"""   
   def __init__(self, game, lines):
      Scene.__init__(self, game)
      self.ammount = len(lines)
      self.selection = 0
      
      self.fonts = {}
      self.fonts["big"] = pygame.font.Font(os.path.join(DIR_FONT, "por2.ttf"), 72)
      self.fonts["medium"] = pygame.font.Font(os.path.join(DIR_FONT, "por2.ttf"), 40)
      self.fonts["small"] = pygame.font.Font(os.path.join(DIR_FONT, "por2.ttf"), 18)
      
      self.separator = pygame.Surface((RES_WIDTH, 5)).convert()
      self.separator.fill((255,215,0))

      self.levelLoader = LevelLoader(self)
      self.loadLevel(0)
      
      self.header = {}
      self.header["py"] = self.text(self.fonts["big"], "Py",(255,215,0))
      self.header["duel"] = self.text(self.fonts["big"], "Duel",(255,255,255))
      self.header["py"].rect.right = 0
      self.header["duel"].rect.left = RES_WIDTH
      self.header["py"].rect.top = 10
      self.header["duel"].rect.top = 10
      
      #add text objects into containing lists
      self.textlinesInactive = []
      self.textlinesActive = []
      for line in lines:
         self.textlinesInactive.append(self.text(self.fonts["medium"], line,(255,255,255)))
         self.textlinesActive.append(self.text(self.fonts["medium"], line,(255,215,0)))
      
      #place the text options in the right position
      for i in range(self.ammount):
         self.textlinesInactive[i].rect.centerx = RES_WIDTH/2
         self.textlinesInactive[i].rect.y = 100 + i * 50
         self.textlinesActive[i].rect.centerx = RES_WIDTH/2
         self.textlinesActive[i].rect.y = 100 + i * 50
         
   def loadLevel(self, levelNumber):
      self.levelNumber = levelNumber
      self.level = self.levelLoader.load(self.levelLoader.__class__.levels[levelNumber]) # use level list from level loader's class

   class text (object):
      """used to get text objects with a surface and a rect"""
      def __init__(self, font, text, color):
         self.surface = font.render(text, True, color)
         self.rect = self.surface.get_rect()
     
   def loop(self):
      #put moves here, used for the headers slide-in now.
      if  self.header["py"].rect.right + 15 < self.header["duel"].rect.left:
         self.header["py"].rect.left += 5
         self.header["duel"].rect.left -= 7
      
   def event(self, event):
      #Check for keyp up/down and set new selection
      if event.type == KEYDOWN and event.key == K_DOWN:
         if (self.selection < self.ammount-1):
            self.selection += 1
      if event.type == KEYDOWN and event.key == K_UP:
         if (self.selection > 0):
            self.selection += -1
      #check for enter and do action (currently only for main-menu)
      if event.type == KEYDOWN and event.key == K_RETURN:
         if self.selection == 0:
            self.runScene(Duel(self.game))
         if self.selection == 1:
            pass
         if self.selection == 2:
            self.end(0)
   
   def update(self):
      #Erease textlines.rect and blit active or inactive-colored text onto screen.
      for i in range(self.ammount):
         self.game.screen.blit(self.background, self.textlinesActive[i].rect, self.textlinesActive[i].rect)
         if i==self.selection:
            self.game.screen.blit(self.textlinesActive[i].surface,self.textlinesActive[i].rect)
         else:
            self.game.screen.blit(self.textlinesInactive[i].surface,self.textlinesInactive[i].rect)
      
      #erease and blit header (inflate beacuse of moving), lines and level.
      for header in self.header.values():
         self.game.screen.blit(self.background, header.rect.inflate(15,0), header.rect.inflate(15,0))
         self.game.screen.blit(header.surface, header.rect)
         
      self.game.screen.blit(self.separator,(0,80))
      self.level.tiles.remove(self.level.noneTiles)
      self.level.tiles.clear(self.game.screen, self.background)
      self.level.tiles.add(self.level.noneTiles)
      self.level.draw(self.game.screen) 

def main():
   pyduel = Game(RESOLUTION, CAPTION, ICON)
   firstScene = Menu(pyduel,("New Game","Options","Quit"))
   pyduel.start(firstScene)
   raise SystemExit, 0

if __name__ == "__main__":
   main()
