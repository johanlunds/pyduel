#!/usr/bin/env python
# -*- coding: utf-8 -*-

from level import Tile
from variables import *

import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):

   JUMPSPEED = 8 # Speed at start of jump
   SPEED = 2 # Walking speed
   JUMPED, STANDING = range(2) # States of player

   def __init__(self, image, keys):
      pygame.sprite.Sprite.__init__(self)
      
      self.image, self.rect = image, image.get_rect()
      self.keyLeft, self.keyRight, self.keyUp, self.keyDown = self.keys = keys
      self.xSpeed, self.ySpeed = (Player.SPEED, Player.SPEED) # xSpeed right = positive; ySpeed up = positive
      self.state = Player.JUMPED # Maybe change to STANDING later, but player begins in air right now
      
   def update(self, keyInput, level):
      self.handleKeyInput(keyInput, level)
      if self.state == Player.JUMPED:
         self.jump(level)

   def move(self, xMove, yMove, level):
      """Move players rect and get corner tiles at new position."""
      self.oldRect = pygame.Rect(self.rect)
      self.rect.move_ip(xMove, -yMove) # yMove is negative because of ySpeed up = positive
      self.checkOuterBounds() # If we're outside map at new pos, move player
      self.getCornerTiles(level) # Get corner tiles at new pos (used later, for example in self.fixPosition())
      
   def handleKeyInput(self, keyInput, level):
      """Handles the different keys pressed on the keyboard."""
      if keyInput[self.keyUp] and self.state != Player.JUMPED:
         self.state = Player.JUMPED
         self.ySpeed = Player.JUMPSPEED
      if keyInput[self.keyLeft]:
         self.move(-self.xSpeed, 0, level)
         fixedPos = self.fixPosition(LEFT, level)
         if not fixedPos: self.fall(level) # We can only fall if we move left/right, and haven't got tiles at our left/right
      if keyInput[self.keyRight]:
         self.move(self.xSpeed, 0, level)
         fixedPos = self.fixPosition(RIGHT, level)
         if not fixedPos: self.fall(level) # See above.
      
   def getCornerTiles(self, level, rect=None):
      """Calculate players corner tiles. An optional rect argument can be passed which gets used instead of players."""
      if not rect: rect = self.rect
      self.tileTopLeft = level.get((rect.left, rect.top), True)
      self.tileTopRight = level.get((rect.right, rect.top), True)
      self.tileBottomLeft = level.get((rect.left, rect.bottom), True)
      self.tileBottomRight = level.get((rect.right, rect.bottom), True)
         
   def checkOuterBounds(self):
      # Player cant go outside the screens sides, but can jump over top
      if self.rect.left < 0:
         self.rect.left = 0
      if self.rect.right > RES_WIDTH:
         self.rect.right = RES_WIDTH
      if self.rect.top > RES_HEIGHT:
         self.rect.top = 0 # Falled through screen so move to top of screen
   
   def jump(self, level):
      # Player is in the air.
      self.ySpeed -= GRAVITY
      # If speed is too high we might miss tiles (and begin moving through walls)
      if self.ySpeed > Tile.HEIGHT: self.ySpeed = Tile.HEIGHT # speed is bigger than tile's height
      
      self.move(0, self.ySpeed, level)
      if self.ySpeed > 0: # we're going up
         fixedPos = self.fixPosition(UP, level)
         if fixedPos: self.ySpeed = 0 # we've hit a tile above us. Fall down again.
      elif self.ySpeed < 0: # we're going down
         fixedPos = self.fixPosition(DOWN, level)
         if fixedPos: self.state = Player.STANDING # We've fallen down to solid ground
   
   def fall(self, level):
      """Check if we have stepped out into air."""
      if self.state != Player.JUMPED: # Only if we're not already in the air
         self.getCornerTiles(level, self.rect.inflate(0, 2)) # We have to expand the rect we're passing as argument
         if not self.tileBottomLeft.walkable or not self.tileBottomRight.walkable:
            # We're in the air
            self.ySpeed = 0 # Start falling
            self.state = Player.JUMPED # Force state to be jumped
         
   def fixPosition(self, dir, level):
      """Check position of player at chosen direction and fix if we've hit something.
      
      Returns true if position is changed ("fixed").
      """
      # Works like this: If directions corners contains tiles who aren't walkable
      # we move player as far as we can (to the tile's side).
      if dir == UP:
         if not self.tileTopLeft.walkable or not self.tileTopRight.walkable:
            self.rect = self.oldRect
            self.rect.top = level.get((self.rect.centerx, self.rect.top), True).rect.top         
            return True
      elif dir == DOWN:
         if not self.tileBottomLeft.walkable or not self.tileBottomRight.walkable:
            self.rect = self.oldRect
            self.rect.bottom = level.get((self.rect.centerx, self.rect.bottom), True).rect.bottom-1 # Minus one (important!), because of how rects works
            return True
      elif dir == LEFT:
         if not self.tileTopLeft.walkable or not self.tileBottomLeft.walkable:
            self.rect = self.oldRect
            self.rect.left = level.get((self.rect.left, self.rect.centery), True).rect.left
            return True
      elif dir == RIGHT:
         if not self.tileTopRight.walkable or not self.tileBottomRight.walkable:
            self.rect = self.oldRect
            self.rect.right = level.get((self.rect.right, self.rect.centery), True).rect.right-1 # Minus one (important!), because of how rects works
            return True
            
      return False # We haven't changed the position of player
