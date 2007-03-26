#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xml.sax.handler
import pygame
from pygame.locals import *
from level import LevelLoader
from variables import *


class Menu(object):
   """menu class, used by diffrent menus"""
   def __init__(self, lines):   
      self.ammount = len(lines)
      self.selection = 0
      
      # Load fonts
      self.fonts = {}
      self.fonts["big"] = pygame.font.Font(os.path.join(DIR_FONT, "por2.ttf"), 72)
      self.fonts["medium"] = pygame.font.Font(os.path.join(DIR_FONT, "por2.ttf"), 40)
      self.fonts["small"] = pygame.font.Font(os.path.join(DIR_FONT, "por2.ttf"), 18)
      
      self.separator = pygame.Surface((RES_WIDTH, 5)).convert()
      self.separator.fill((255,215,0))

      self.levelLoader = LevelLoader(self)
      self.loadLevel(0)
      
      # Load and position header (pyduel)
      self.header = {}
      self.header["py"] = self.text(self.fonts["big"], "Py",(255,215,0))
      self.header["duel"] = self.text(self.fonts["big"], "Duel",(255,255,255))
      self.header["py"].rect.right = 0
      self.header["duel"].rect.left = RES_WIDTH
      self.header["py"].rect.top = 10
      self.header["duel"].rect.top = 10
      
      # Add text objects into containing lists
      self.textlinesInactive = []
      self.textlinesActive = []
      for line in lines:
         self.textlinesInactive.append(self.text(self.fonts["medium"], line,(255,255,255)))
         self.textlinesActive.append(self.text(self.fonts["medium"], line,(255,215,0)))
      
      # Place the text options in the right position
      for i in range(self.ammount):
         self.textlinesInactive[i].rect.centerx = RES_WIDTH/2
         self.textlinesInactive[i].rect.y = 100 + i * 50
         self.textlinesActive[i].rect.centerx = RES_WIDTH/2
         self.textlinesActive[i].rect.y = 100 + i * 50
         
   def loadLevel(self, levelNumber):
      self.levelNumber = levelNumber
      self.level = self.levelLoader.load(self.levelLoader.__class__.levels[levelNumber]) # use level list from level loader's class

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
         widthChange = self.surface.get_rect().width - self.rect.width
         if widthChange > 0:
            self.rect.inflate_ip(widthChange, 0)

      def setColor(self, color):
         """Change the color, currently not used."""
         self.color = color
         self.surface = self.font.render(self.string , True, self.color)

   def headerSlide(self):
      """Slide in the parts of the header untill they meet."""
      if  self.header["py"].rect.right + 15 < self.header["duel"].rect.left:
         self.header["py"].rect.left += 5
         self.header["duel"].rect.left -= 7

   def update(self, screen, background):
      # Erease textlines.rect and blit active or inactive-colored text onto screen.
      for i in range(self.ammount):
         screen.blit(background, self.textlinesActive[i].rect, self.textlinesActive[i].rect)
         if i==self.selection:
            screen.blit(self.textlinesActive[i].surface,self.textlinesActive[i].rect)
         else:
            screen.blit(self.textlinesInactive[i].surface,self.textlinesInactive[i].rect)
      
      # Erease and blit header (inflate beacuse of moving), lines and level.
      for header in self.header.values():
         screen.blit(background, header.rect.inflate(15,0), header.rect.inflate(15,0))
         screen.blit(header.surface, header.rect)
         
      screen.blit(self.separator,(0,80))
      self.level.tiles.remove(self.level.noneTiles)
      self.level.tiles.clear(screen, background)
      self.level.tiles.add(self.level.noneTiles)
      self.level.draw(screen)

# Options class isn't really even started, ignore this
class Options(xml.sax.handler.ContentHandler):
   """For loading levels from XML-files. More info: http://docs.python.org/lib/module-xml.sax.handler.html"""
   def __init__(self, filename):
      """Open file and parse contents. Returns new level object."""
      self.elementTree = [] # Used to keep track of current element and it's parents  
      parser = xml.sax.make_parser()
      parser.setContentHandler(self) # Set current object to parse contents of file
      parser.parse(filename)
   
   def startElement(self, name, attributes):
      # Remember: attributes is not dict but attribute object (see xml.sax.handler.ContentHandler docs)
      # To convert we could use: attributes = dict(attributes.items()))     
      self.elementTree.append(name)
      if name == "option":
         print dict(attributes.items())



   def endElement(self, name): # called at end of element (<element /> or <element></element>)
      self.elementTree.pop() # remove last item

      
   

   
