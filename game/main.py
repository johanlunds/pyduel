#!/usr/bin/env python
# -*- coding: utf-8 -*-

from variables import *

import os
import shutil

from engine import Game, Scene
from level import LevelLoader
from player import Player
from menu import Menu, Options, OptionsHandler

import pygame
from pygame.locals import *

class Duel(Scene):
   """The main game scene. Where the players fight against eachother."""
   
   def __init__(self, game):
      Scene.__init__(self, game)
      
      self.levelLoader = LevelLoader(self)
      self.loadLevel(1) # First level

      self.background = loadImgPng(os.path.join(self.level.theme, "bg.png"))
      
      self.weapons = pygame.sprite.Group()
      self.players = pygame.sprite.Group()
      for i, playerOpts in zip(range(2), (self.game.options.playerOne, self.game.options.playerTwo)):
         # Could randomize start pos with list.pop() and random.random() and len(list)
         startPos = self.level.getPixelsFromCords(self.level.startPos[i])
         keys = dict([(key, playerOpts[key]) for key in ("left", "right", "up", "down", "jump", "shoot")])
         self.players.add(Player(self, loadImgPng(playerOpts["image"]), keys, startPos))
   
   def loadLevel(self, levelNumber):
      self.levelNumber = levelNumber
      self.level = self.levelLoader.load(LevelLoader.levels[levelNumber], self.game.options.game["theme"]) # use level list from level loader's class
   
   def playerKilled(self, player):
      self.end()
   
   def event(self, event):
      if event.type == KEYDOWN and event.key == K_ESCAPE:
         self.end()

   def loop(self):
      self.level.update()
      pygame.event.pump()
      keyInput = pygame.key.get_pressed()
      self.players.update(keyInput)
   
   def update(self):
      self.level.tiles.remove(self.level.noneTiles) # why? see Level.draw()
      
      self.weapons.clear(self.game.screen, self.background)
      self.players.clear(self.game.screen, self.background)
      self.level.bullets.clear(self.game.screen, self.background)
      self.level.tiles.clear(self.game.screen, self.background)
      self.level.ladderTiles.clear(self.game.screen, self.background)
      self.level.itemTiles.clear(self.game.screen, self.background)
      
      self.level.tiles.draw(self.game.screen)
      self.level.ladderTiles.draw(self.game.screen)
      self.level.itemTiles.draw(self.game.screen)
      self.players.draw(self.game.screen)
      self.weapons.draw(self.game.screen)
      self.level.bullets.draw(self.game.screen)
      
      self.level.tiles.add(self.level.noneTiles)
        
   def draw(self):
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
         self.end()   
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
            self.end()
   
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
      self.themes = []
      self.themeIndex = 0
      tmp = True # it is buggy without this, see: http://deadbeefbabe.org/paste/4161
      for entry in os.listdir(DIR_GRAPH):
         if os.path.isdir(os.path.join(DIR_GRAPH, entry)) and entry != ".svn":
            self.themes.append(entry)
            if self.options.game["theme"] == entry: tmp = False
            if tmp: self.themeIndex += 1  

   def event(self, event):
      if event.type == KEYDOWN and event.key == K_ESCAPE:  # Escape pressed => End scene.
         self.game.optionHandler.writeXML()
         self.end()
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
         if self.menu.selection == 4: #theme
            self.changeTheme(1)
         if self.menu.selection == 5: #time
            if self.options.game["time"] < 60: self.options.game["time"] += 1
            self.menu.setLine(5, "Timelimit: %s" % self.options.game["time"])
         if self.menu.selection == 6: #lives
            if self.options.game["time"] < 50: self.options.game["lives"] += 1
            self.menu.setLine(6, "Lives: %s" % self.options.game["lives"])
 

      if event.type == KEYDOWN and event.key == K_LEFT:
         if self.menu.selection == 3: #level
            if self.options.game["level"] > 1: self.options.game["level"] += -1
            self.menu.setLine(3, "Level: %s" % self.options.game["level"])
         if self.menu.selection == 4: #theme
            self.changeTheme(-1)
         if self.menu.selection == 5: #time
            if self.options.game["time"] > 1: self.options.game["time"] += -1
            self.menu.setLine(5, "Timelimit: %s" % self.options.game["time"])
         if self.menu.selection == 6: #lives
            if self.options.game["lives"] > 1: self.options.game["lives"] += -1
            self.menu.setLine(6, "Lives: %s" % self.options.game["lives"])

      if event.type == KEYDOWN and event.key == K_RETURN:
         if self.menu.selection == 7: #player one
            self.runScene(PlayerOptionsMenu(self.game, self.options.playerOne))
         if self.menu.selection == 8: #player two
            self.runScene(PlayerOptionsMenu(self.game, self.options.playerTwo))
         if self.menu.selection == 9: #reset
            fullscreen = self.options.system["fullscreen"]
            shutil.copy("optionsDefault.xml", "options.xml")
            self.game.optionHandler = OptionsHandler("options.xml")
            if self.game.optionHandler.options.system["fullscreen"] == False and fullscreen: self.game.toggleFullscreen()
            elif fullscreen == False and self.game.optionHandler.options.system["fullscreen"]: self.game.toggleFullscreen()
            self.end()
         if self.menu.selection == 10: #back
            self.game.optionHandler.writeXML()
            self.end()

   def loop(self):
      self.menu.headerSlide()

   def update(self):
      self.menu.update(self.game.screen, self.background)

   def changeTheme(self, change):
      """take +1 or -1 and change the image in playerOptions and the line displayed"""
      self.themeIndex += change
      if self.themeIndex < 0: self.themeIndex = len(self.themes)-1
      if self.themeIndex >= len(self.themes): self.themeIndex = 0
      self.options.game["theme"] = self.themes[self.themeIndex]
      self.menu.setLine(4,"Theme: %s" % self.options.game["theme"])

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
      lines.append("Theme: %s" % self.options.game["theme"])
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
         self.end()   
      if event.type == KEYDOWN and event.key == K_DOWN: self.menu.selection += 1
      if (self.menu.selection < 0): self.menu.selection = self.menu.ammount-1
      if event.type == KEYDOWN and event.key == K_UP: self.menu.selection += -1
      if (self.menu.selection > self.menu.ammount-1): self.menu.selection = 0
      if event.type == KEYDOWN and event.key == K_RETURN: # Check for enter and do action
         if self.menu.selection == 0: # Name
            self.setName()
         if self.menu.selection == 2: # Left
            self.menu.setColor(2, (255,50,50)) 
            self.playerOptions["left"] = self.getKey(self.playerOptions["left"])
            self.menu.setLine(2,"Left: %s" % pygame.key.name(self.playerOptions["left"]))
            self.menu.setColor(2, (255,215,0)) 
         if self.menu.selection == 3: # Right 
            self.menu.setColor(3, (255,50,50)) 
            self.playerOptions["right"] = self.getKey(self.playerOptions["right"])
            self.menu.setLine(3,"Right: %s" % pygame.key.name(self.playerOptions["right"]))
            self.menu.setColor(3, (255,215,0)) 
         if self.menu.selection == 4: # Up 
            self.menu.setColor(4, (255,50,50)) 
            self.playerOptions["up"] = self.getKey(self.playerOptions["up"])
            self.menu.setLine(4,"Up: %s" % pygame.key.name(self.playerOptions["up"]))
            self.menu.setColor(4, (255,215,0)) 
         if self.menu.selection == 5: # Down 
            self.menu.setColor(5, (255,50,50)) 
            self.playerOptions["down"] = self.getKey(self.playerOptions["down"])
            self.menu.setLine(5,"Down: %s" % pygame.key.name(self.playerOptions["down"]))
            self.menu.setColor(5, (255,215,0)) 
         if self.menu.selection == 6: # Jump 
            self.menu.setColor(6, (255,50,50)) 
            self.playerOptions["jump"] = self.getKey(self.playerOptions["jump"])
            self.menu.setLine(6,"Jump: %s" % pygame.key.name(self.playerOptions["jump"]))
            self.menu.setColor(6, (255,215,0)) 
         if self.menu.selection == 7: # Shoot 
            self.menu.setColor(7, (255,50,50)) 
            self.playerOptions["shoot"] = self.getKey(self.playerOptions["shoot"])
            self.menu.setLine(7,"Shoot: %s" % pygame.key.name(self.playerOptions["shoot"]))
            self.menu.setColor(7, (255,215,0)) 
         if self.menu.selection == 8: # Back
            self.end()

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
         self.updateAndFlip()
         for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
               return oldKey
            if event.type == KEYDOWN and event.key not in(K_CAPSLOCK, K_ESCAPE):
               return event.key

   def setName(self):
      """Get a string from keyboard and change name, esc resets the old string"""
      self.menu.setColor(0, (255,50,50))
      oldString = self.playerOptions["name"]
      string = ""
      while True:
         
         self.menu.setLine(0,"Name: %s" % string)
         self.updateAndFlip()
         for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
               self.menu.setLine(0,"Name: %s" % oldString)
               self.playerOptions["name"] = oldString
               self.menu.setColor(0, (255,215,0))
               return
            if event.type == KEYDOWN and event.key == K_RETURN and string != "":
               self.playerOptions["name"] = string
               self.menu.setColor(0, (255,215,0))
               return
            elif event.type == KEYDOWN:
               if event.key == K_BACKSPACE:
                  if string != "": string = string[0:len(string)-1]
               if event.key >= K_a and event.key <= K_z or event.key >= K_0 and event.key <= K_9:
                  string += pygame.key.name(event.key)
               if event.key == K_SPACE:
                  string += " "         
   
   def updateAndFlip(self):
      self.menu.headerSlide()
      self.menu.update(self.game.screen, self.background)
      pygame.display.flip() # forgot to flip
   
def main():
   pyduel = Game(RESOLUTION, CAPTION, ICON)
   firstScene = MainMenu(pyduel, ("New Game", "Options", "Quit"))
   pyduel.start(firstScene)
   raise SystemExit, 0

if __name__ == "__main__":
   main()
