#!/usr/bin/env python
# -*- coding: utf-8 -*-

from variables import *

import os
import xml.sax.handler

from level import LevelLoader

import pygame
from pygame.locals import *

class Menu(object):
   """menu class, used by diffrent menus"""
   def __init__(self, header, lines, useSmallFont = False):   
      self.ammount = len(lines)
      self.selection = 0
      # Load fonts
      self.theme = "jungle" # hardcoded menu level theme
      self.fonts = {}
      self.fonts["big"] = pygame.font.Font(os.path.join(DIR_FONT, "por2.ttf"), 72)
      self.fonts["medium"] = pygame.font.Font(os.path.join(DIR_FONT, "por2.ttf"), 40)
      self.fonts["small"] = pygame.font.Font(os.path.join(DIR_FONT, "por2.ttf"), 26)
      
      self.separator = pygame.Surface((RES_WIDTH, 5)).convert()
      self.separator.fill((255,215,0))

      self.levelLoader = LevelLoader(self)
      self.loadLevel(0)
      
      # Load and position header (pyduel)
      self.header = {}
      headerPartOne, headerPartTwo = header
      self.header[1] = self.text(self.fonts["big"], headerPartOne,(255,215,0))
      self.header[2] = self.text(self.fonts["big"], headerPartTwo,(255,255,255))
      self.header[1].rect.right = 0
      self.header[2].rect.left = RES_WIDTH
      self.header[1].rect.top = 10
      self.header[2].rect.top = 10
      
      # Add text objects into containing lists
      self.textlinesInactive = []
      self.textlinesActive = []
      if useSmallFont:
         for line in lines:
            self.textlinesInactive.append(self.text(self.fonts["small"], line,(255,255,255)))
            self.textlinesActive.append(self.text(self.fonts["small"], line,(255,215,0)))
      else:
         for line in lines:
            self.textlinesInactive.append(self.text(self.fonts["medium"], line,(255,255,255)))
            self.textlinesActive.append(self.text(self.fonts["medium"], line,(255,215,0)))
         
      # Place the text options in the right position
      for i in range(self.ammount):
         for textline in self.textlinesInactive[i], self.textlinesActive[i]:
            textline.rect.centerx = RES_WIDTH/2
            if useSmallFont: textline.rect.y = 100 + i * 30
            else: textline.rect.y = 100 + i * 50
         
   def loadLevel(self, levelNumber):
      self.levelNumber = levelNumber
      self.level = self.levelLoader.load(LevelLoader.levels[levelNumber], self.theme) # use level list from level loader's class
   
   def setLine(self, linenumber, string):
      self.textlinesActive[linenumber].setString(string)
      self.textlinesInactive[linenumber].setString(string)
      
   def setColor(self, linenumber, color):
      self.textlinesActive[linenumber].setColor(color)

   class text (object):
      """used to get text objects"""
      def __init__(self, font, text, color):
         self.font = font
         self.string = text
         self.color = color
         self.surface = self.font.render(self.string , True, self.color)
         self.rect = self.surface.get_rect()

      def setString(self, string):
         """Get a surface for a new string, inflate the rect if its bigger"""
         self.string = string
         self.surface = self.font.render(self.string , True, self.color)
         self.rect.width = self.surface.get_rect().width
         self.rect.centerx = RES_WIDTH / 2


      def setColor(self, color):
         """Change the color, currently not used."""
         self.color = color
         self.surface = self.font.render(self.string , True, self.color)

   def headerSlide(self):
      """Slide in the parts of the header untill they meet."""
      distanceFromCenter = (self.header[1].rect.width + self.header[2].rect.width) / 2
      if self.header[1].rect.left + distanceFromCenter + 7 < (RES_WIDTH / 2): self.header[1].rect.left += 7
      if self.header[2].rect.right - distanceFromCenter - 7 > (RES_WIDTH / 2): self.header[2].rect.left += -7

   def update(self, screen, background):
      # Erease textlines.rect and blit active or inactive-colored text onto screen.
      screen.blit(background, (0,0))
      for i in range(self.ammount):
         if i==self.selection:
            screen.blit(self.textlinesActive[i].surface,self.textlinesActive[i].rect)
         else:
            screen.blit(self.textlinesInactive[i].surface,self.textlinesInactive[i].rect)
      
      # Erease and blit header (inflate beacuse of moving), lines and level.
      for header in self.header.values():
         screen.blit(header.surface, header.rect)
         
      screen.blit(self.separator,(0,80))
      self.level.draw(screen)

class Options(object):
   """Holds the option dictionaries"""
   def __init__(self):
      self.system = {}
      self.game = {}
      self.playerOne = {}
      self.playerTwo = {}

class OptionsHandler(xml.sax.handler.ContentHandler):
   """For loading levels from XML-files. More info: http://docs.python.org/lib/module-xml.sax.handler.html"""
   def __init__(self, filename):
      self.options = Options()
      self.propertyName = ""
      self.propertyType = ""

      self.elementTree = [] # Used to keep track of current element and it's parents  
      parser = xml.sax.make_parser()
      parser.setContentHandler(self) # Set current object to parse contents of file
      parser.parse(filename)
      

   def startElement(self, name, attributes):
      # Remember: attributes is not dict but attribute object (see xml.sax.handler.ContentHandler docs)
      # To convert we could use: attributes = dict(attributes.items()))     
      self.elementTree.append(name)
      if name == "option":
         self.propertyName = attributes["name"]
         self.propertyType = attributes.get("type", "str") # defaults to int (change to str?)
         if self.propertyType not in ("int", "float", "long", "str", "unicode", "eval"): # allowed types
            # we haven't got valid value, raise exception with msg and exit
            raise StandardError, 'Element "property" has attribute "type" with invalid value.'
         
   def characters(self, content):
      if self.elementTree[-1] == "option":
         key = str(self.propertyName)
         value = eval(self.propertyType)(content)
         if self.elementTree[-2]  == "system":
            self.options.system[key] = value
         if self.elementTree[-2]  == "game":
            self.options.game[key] = value
         if self.elementTree[-2]  == "playerOne":
               self.options.playerOne[key] = value
         if self.elementTree[-2]  == "playerTwo":
               self.options.playerTwo[key] = value         

   def endElement(self, name): # called at end of element (<element /> or <element></element>)
      #if self.elementTree[-1] == "options":
      #   for player in self.options.playerOne, self.options.playerTwo:
      #      player["keys"] = (player["left"], player["right"], player["up"], player["down"], player["jump"])
      self.elementTree.pop() # remove last item

   def writeXML(self):
      """Writes the options to options.xml, it breaks if a key isn't found."""
      file = open("options.xml", "w")
      file.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
      file.write('\n')
      file.write('<options>\n')
      file.write('   <system>\n')
      file.write('      <option name="fullscreen" type="eval">%s</option>\n' % self.options.system["fullscreen"])
      file.write('      <option name="sound" type="eval">%s</option>\n' % self.options.system["sound"])
      file.write('      <option name="music" type="eval">%s</option>\n' % self.options.system["music"])
      file.write('   </system>\n')
      file.write('   <game>\n')
      file.write('      <option name="level" type="int">%d</option>\n' % self.options.game["level"])
      file.write('      <option name="theme">%s</option>\n' % self.options.game["theme"])
      file.write('      <option name="lives" type="int">%d</option>\n' % self.options.game["lives"])
      file.write('      <option name="time" type="int">%d</option>\n' % self.options.game["time"])
      file.write('   </game>\n')
      file.write('   <playerOne>\n')
      file.write('      <option name="name">%s</option>\n' % self.options.playerOne["name"])
      file.write('      <option name="image">%s</option>\n' % self.options.playerOne["image"])
      file.write('      <option name="left" type="int">%s</option>\n' % self.options.playerOne["left"])
      file.write('      <option name="right" type="int">%s</option>\n' % self.options.playerOne["right"])
      file.write('      <option name="up" type="int">%s</option>\n' % self.options.playerOne["up"])
      file.write('      <option name="down" type="int">%s</option>\n' % self.options.playerOne["down"])
      file.write('      <option name="jump" type="int">%s</option>\n' % self.options.playerOne["jump"])
      file.write('      <option name="shoot" type="int">%s</option>\n' % self.options.playerOne["shoot"])
      file.write('   </playerOne>\n')
      file.write('   <playerTwo>\n')
      file.write('      <option name="name">%s</option>\n' % self.options.playerTwo["name"])
      file.write('      <option name="image">%s</option>\n' % self.options.playerTwo["image"])
      file.write('      <option name="left" type="int">%s</option>\n' % self.options.playerTwo["left"])
      file.write('      <option name="right" type="int">%s</option>\n' % self.options.playerTwo["right"])
      file.write('      <option name="up" type="int">%s</option>\n' % self.options.playerTwo["up"])
      file.write('      <option name="down" type="int">%s</option>\n' % self.options.playerTwo["down"])
      file.write('      <option name="jump" type="int">%s</option>\n' % self.options.playerTwo["jump"])
      file.write('      <option name="shoot" type="int">%s</option>\n' % self.options.playerTwo["shoot"])
      file.write('   </playerTwo>\n')
      file.write('</options>\n')
      file.write('\n')
      file.close()

