#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from shutil import copy 
from engine import Game, Scene
from level import LevelLoader
from player import Player
from variables import *
from menu import *

import pygame
from pygame.locals import *

class Duel(Scene):
   """The main game scene. Where the players fight against eachother."""
   
   def __init__(self, game):
      Scene.__init__(self, game)
      playerOneOptions = game.options.playerOne  
      playerTwoOptions = game.options.playerTwo
      playerOne = Player(self, playerOneOptions, (0,0))
      playerTwo = Player(self, playerTwoOptions, (RES_WIDTH-40,0))
      
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
      self.menu = Menu(("  Py","Duel"),lines)

   def loop(self):
      self.menu.headerSlide()
      
   def event(self, event):      
      if event.type == KEYDOWN and event.key == K_ESCAPE: # Escape pressed => Exit.
         self.end(0)   
      if event.type == KEYDOWN and event.key == K_DOWN: self.menu.selection += 1
      if (self.menu.selection < 0): self.menu.selection = self.menu.ammount-1
      if event.type == KEYDOWN and event.key == K_UP: self.menu.selection += -1
      if (self.menu.selection > self.menu.ammount-1): self.menu.selection = 0
      if event.type == KEYDOWN and event.key == K_RETURN: # Check for enter and do action
         if self.menu.selection == 0:
            self.runScene(Duel(self.game))
         if self.menu.selection == 1:
            self.runScene(OptionsMenu(self.game))
         if self.menu.selection == 2:
            self.end(0)
   
   def update(self):
      self.menu.update(self.game.screen, self.background)

class OptionsMenu(Scene):
   """Options menu, everything but players is working. code is huge and ugly though. ;o"""
   def __init__(self, game):
      Scene.__init__(self, game)
      self.game = game
      self.options = self.game.optionHandler.options  
      lines = self.loadLines()
      self.menu = Menu((" Opt","ions"), lines, True)
   
   def event(self, event):
      if event.type == KEYDOWN and event.key == K_ESCAPE:  # Escape pressed => End scene.
         self.game.optionHandler.writeXML()
         self.end(0)
      # Check for keyp up/down and set new selection    
      if event.type == KEYDOWN and event.key == K_DOWN: self.menu.selection += 1
      if (self.menu.selection < 0): self.menu.selection = self.menu.ammount-1
      if event.type == KEYDOWN and event.key == K_UP: self.menu.selection += -1
      if (self.menu.selection > self.menu.ammount-1): self.menu.selection = 0
      
      if event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_LEFT or event.key == K_RETURN):
         if self.menu.selection == 0: #fullscreen
            if self.options.system["fullscreen"]:
               self.options.system["fullscreen"] = False
               self.menu.setLine(0, "Fullscreen: %s" % "No")
               self.game.toggleFullscreen()
            else: 
               self.options.system["fullscreen"] = True
               self.menu.setLine(0, "Fullscreen: %s" % "Yes")
               self.game.toggleFullscreen()
         if self.menu.selection == 1: #sound
            if self.options.system["sound"]:
               self.options.system["sound"] = False
               self.menu.setLine(1, "Sound: %s" % "No")
            else: 
               self.options.system["sound"] = True
               self.menu.setLine(1, "Sound: %s" % "Yes")
         if self.menu.selection == 2: #music
            if self.options.system["music"]: 
               self.options.system["music"] = False
               self.menu.setLine(2, "Music: %s" % "No")
            else:
               self.options.system["music"] = True
               self.menu.setLine(2, "Music: %s" % "Yes")
      
      if event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_RETURN):
         if self.menu.selection == 3: #level
            if self.options.game["level"] < len(LevelLoader.levels)-1: self.options.game["level"] += 1
            self.menu.setLine(3, "Level: %s" % self.options.game["level"])
         if self.menu.selection == 4: #time
            if self.options.game["time"] < 60: self.options.game["time"] += 1
            self.menu.setLine(4, "Timelimit: %s" % self.options.game["time"])
         if self.menu.selection == 5: #lives
            if self.options.game["time"] < 50: self.options.game["lives"] += 1
            self.menu.setLine(5, "Lives: %s" % self.options.game["lives"])
 

      if event.type == KEYDOWN and event.key == K_LEFT:
         if self.menu.selection == 3: #level
            if self.options.game["level"] > 1: self.options.game["level"] += -1
            self.menu.setLine(3, "Level: %s" % self.options.game["level"])
         if self.menu.selection == 4: #time
            if self.options.game["time"] > 1: self.options.game["time"] += -1
            self.menu.setLine(4, "Timelimit: %s" % self.options.game["time"])
         if self.menu.selection == 5: #lives
            if self.options.game["lives"] > 1: self.options.game["lives"] += -1
            self.menu.setLine(5, "Lives: %s" % self.options.game["lives"])

      if event.type == KEYDOWN and event.key == K_RETURN:
         if self.menu.selection == 6: #player one
            self.runScene(PlayerOptionsMenu(self.game, self.options.playerOne))
         if self.menu.selection == 7: #player two
            self.runScene(PlayerOptionsMenu(self.game, self.options.playerTwo))
         if self.menu.selection == 8: #reset
            fullscreen = self.options.system["fullscreen"]
            copy("options-default.xml", "options.xml")
            self.game.optionHandler = OptionsHandler("options.xml")
            if self.game.optionHandler.options.system["fullscreen"] == False and fullscreen: self.game.toggleFullscreen()
            elif fullscreen == False and self.game.optionHandler.options.system["fullscreen"]: self.game.toggleFullscreen()
            self.end(0)
         if self.menu.selection == 9: #back
            self.game.optionHandler.writeXML()
            self.end(0)

   def loop(self):
      self.menu.headerSlide()

   def update(self):
      self.menu.update(self.game.screen, self.background)

   def loadLines(self):
      """Return the lines used when loading the menu"""
      lines = []
      if self.options.system["fullscreen"]: lines.append("Fullscreen: %s" % "Yes") 
      else: lines.append("Fullscreen: %s" % "No") 
      if self.options.system["sound"]: lines.append("Sound: %s" % "Yes" )
      else: lines.append("Sound: %s" % "No" )
      if self.options.system["music"]: lines.append("Music: %s" % "Yes")
      else: lines.append("Music: %s" % "No")
      lines.append("Level: %s" % self.options.game["level"])
      lines.append("Timelimit: %s" % self.options.game["time"])
      lines.append("Lives: %s" % self.options.game["lives"])     
      lines.append("Player 1")
      lines.append("Player 2")
      lines.append("Reset All")
      lines.append("Back")
      return lines

class PlayerOptionsMenu(Scene):
   def __init__(self, game, playerOptions):
      Scene.__init__(self, game)
      self.imageIndex = 0
      self.images = []
      self.playerOptions = playerOptions
      tmp = True # it is buggy without this, see: http://deadbeefbabe.org/paste/4161
      for entry in os.listdir(DIR_GRAPH):
         if os.path.isfile(os.path.join(DIR_GRAPH, entry)) and entry.find("player-") != -1 and entry.find(".png") != -1:
            self.images.append(entry)
            if self.playerOptions["image"] == entry: tmp = False
            if tmp: self.imageIndex += 1  
      self.lines = self.loadLines()
      self.menu = Menu(("Pla","yer"), self.lines, True)

   def loop(self):
      self.menu.headerSlide()
      
   def event(self, event):      
      if event.type == KEYDOWN and event.key == K_ESCAPE: # Escape pressed => Exit.
         self.end(0)   
      if event.type == KEYDOWN and event.key == K_DOWN: self.menu.selection += 1
      if (self.menu.selection < 0): self.menu.selection = self.menu.ammount-1
      if event.type == KEYDOWN and event.key == K_UP: self.menu.selection += -1
      if (self.menu.selection > self.menu.ammount-1): self.menu.selection = 0
      if event.type == KEYDOWN and event.key == K_RETURN: # Check for enter and do action
         if self.menu.selection == 0: # Name
            self.setName()
         if self.menu.selection == 2: # Left 
            self.playerOptions["left"] = self.getKey(self.playerOptions["left"])
            self.menu.setLine(2,"Left: %s" % pygame.key.name(self.playerOptions["left"]))
         if self.menu.selection == 3: # Right 
            self.playerOptions["right"] = self.getKey(self.playerOptions["right"])
            self.menu.setLine(3,"Right: %s" % pygame.key.name(self.playerOptions["right"]))
         if self.menu.selection == 4: # Up 
            self.playerOptions["up"] = self.getKey(self.playerOptions["up"])
            self.menu.setLine(4,"Up: %s" % pygame.key.name(self.playerOptions["up"]))
         if self.menu.selection == 5: # Down 
            self.playerOptions["down"] = self.getKey(self.playerOptions["down"])
            self.menu.setLine(5,"Down: %s" % pygame.key.name(self.playerOptions["down"]))
         if self.menu.selection == 6: # Jump 
            self.playerOptions["jump"] = self.getKey(self.playerOptions["jump"])
            self.menu.setLine(6,"Jump: %s" % pygame.key.name(self.playerOptions["jump"]))
         if self.menu.selection == 7: # Shoot 
            self.playerOptions["shoot"] = self.getKey(self.playerOptions["shoot"])
            self.menu.setLine(7,"Shoot: %s" % pygame.key.name(self.playerOptions["shoot"]))
         if self.menu.selection == 8: # Back
            self.end(0)

      if self.menu.selection == 1 and event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_RIGHT):    
         self.changeImage(1)
      if self.menu.selection == 1 and event.type == KEYDOWN and event.key == K_LEFT:
         self.changeImage(-1)

   def update(self):
      self.menu.update(self.game.screen, self.background)
   
   def loadLines(self):
      """Return the lines used when loading the menu"""
      lines = []
      lines.append("Name: %s" % self.playerOptions["name"])
      lines.append("Image: %s" % self.playerOptions["image"].replace("player-","").replace(".png", ""))
      lines.append("Left: %s" % pygame.key.name(self.playerOptions["left"]))
      lines.append("Right: %s" % pygame.key.name(self.playerOptions["right"]))
      lines.append("Up: %s" % pygame.key.name(self.playerOptions["up"]))
      lines.append("Down: %s" % pygame.key.name(self.playerOptions["down"]))
      lines.append("Jump: %s" % pygame.key.name(self.playerOptions["jump"]))
      lines.append("Shoot: %s" % pygame.key.name(self.playerOptions["shoot"]))
      lines.append("Back")
      return lines

   def changeImage(self, change):
      """take +1 or -1 and change the image in playerOptions and the line displayed"""
      self.imageIndex += change
      if self.imageIndex < 0: self.imageIndex = len(self.images)-1
      if self.imageIndex >= len(self.images): self.imageIndex = 0
      self.playerOptions["image"] = self.images[self.imageIndex]
      self.menu.setLine(1,"Image: %s" % self.playerOptions["image"].replace("player-","").replace(".png", ""))

   def getKey(self, oldKey):
      """check for a key and return the keycode, escape returns oldKey parameter"""
      while 1:
         self.update()
         for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
               return oldKey
            if event.type == KEYDOWN:
               return event.key

   def setName(self):
      """Get a string from keyboard and change name, esc resets the old string"""
      oldString = self.playerOptions["name"]
      string = ""
      while True:
         self.menu.setLine(0,"Name: %s" % string)
         self.update()
         for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
               self.menu.setLine(0,"Name: %s" % oldString)
               self.playerOptions["name"] = oldString
               return
            if event.type == KEYDOWN and event.key == K_RETURN and string != "":
               self.playerOptions["name"] = string
               return
            elif event.type == KEYDOWN:
               if event.key == K_BACKSPACE:
                  if string != "": string = string[0:len(string)-1]
               if event.key >= K_a and event.key <= K_z or event.key >= K_0 and event.key <= K_9:
                  string += pygame.key.name(event.key)
               if event.key == K_SPACE:
                  string += " "         
               

def main():
   pyduel = Game(RESOLUTION, CAPTION, ICON)
   firstScene = MainMenu(pyduel,("New Game","Options","Quit"))
   pyduel.start(firstScene)
   raise SystemExit, 0

if __name__ == "__main__":
   main()
