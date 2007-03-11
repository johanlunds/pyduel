#!/usr/bin/env python
# -*- coding: utf-8 -*-

from level import Tile
from variables import *

import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):

   JUMPSPEED = 8 # Speed at start of jump
   SPEED = 2 # Walking speed
   STANDING, JUMPING, CLIMBING = range(3) # States of player
   ANIMATIONSPEED = 15
   FRAMES = 4
   WIDTH=18
   HEIGHT=36 

   def __init__(self, image, keys):
      pygame.sprite.Sprite.__init__(self)
      self.frames = loadImageFrames(image, Player.WIDTH, Player.HEIGHT, Player.FRAMES, True)
      self.currentFrame = 0
      self.image, self.rect = self.frames[self.currentFrame], self.frames[self.currentFrame].get_rect()
      self.keyLeft, self.keyRight, self.keyUp, self.keyDown = self.keys = keys
      self.xSpeed, self.ySpeed = (Player.SPEED, Player.SPEED) # xSpeed right = positive; ySpeed up = positive
      self.state = Player.JUMPING # Maybe change to STANDING later, but player begins in air right now
      self.isWalking = False
      self.facing = RIGHT
      self.frameCounter = 0
      
   def update(self, keyInput, level):
      self.frameCounter += 1
      if self.frameCounter % Player.ANIMATIONSPEED == 0: self.changeFrame()
      self.handleKeyInput(keyInput, level)
      if self.state == Player.JUMPING:
         self.jump(level)

   def move(self, xMove, yMove, level):
      """Move players rect and get corner tiles at new position."""
      self.oldRect = pygame.Rect(self.rect)
      self.rect.move_ip(xMove, -yMove) # yMove is negative because of ySpeed up = positive
      self.checkOuterBounds() # If we're outside map at new pos, move player
      self.getCornerTiles(level) # Get corner tiles at new pos (used later, for example in self.fixPosition())
      
   def handleKeyInput(self, keyInput, level):
      """Handles the different keys pressed on the keyboard."""
      self.isWalking = False
      if keyInput[self.keyUp] and self.state != Player.JUMPING:
         self.state = Player.JUMPING
         self.ySpeed = Player.JUMPSPEED
      if keyInput[self.keyLeft]:
         self.move(-self.xSpeed, 0, level)
         if self.facing == RIGHT: self.changeDirection()
         self.isWalking = True
         fixedPos = self.fixPosition(LEFT, level)
         if not fixedPos: self.fall(level) # We can only fall if we move left/right, and haven't got tiles at our left/right 
      if keyInput[self.keyRight]:
         self.move(self.xSpeed, 0, level)
         if self.facing == LEFT: self.changeDirection()
         self.isWalking = True
         fixedPos = self.fixPosition(RIGHT, level)
         if not fixedPos: self.fall(level) # See above. 
         

   def changeDirection(self):
      """Change which way the player is facing, adjust self.facing and currentFrame acordingly"""
      if self.facing is LEFT:
         self.currentFrame = 0
         self.facing = RIGHT
      elif self.facing is RIGHT:
         self.currentFrame = Player.FRAMES*2 - 1
         self.facing = LEFT
      self.changeFrame()
            

   def changeFrame(self):
      """Go to the next frame if we are walking, go to first if we passed the last or if we aren't walking. note that the frames facing left are mirrored, therefor we do -1 instead of +1"""  
      if self.facing is RIGHT:
         if self.isWalking is True: self.currentFrame += 1
         if self.currentFrame is Player.FRAMES or self.isWalking is False: self.currentFrame = 0
      elif self.facing is LEFT:
         if self.isWalking is True: self.currentFrame += -1
         if self.currentFrame is Player.FRAMES - 1 or self.isWalking is False: self.currentFrame = Player.FRAMES*2 - 1
      self.image = self.frames[self.currentFrame] 

   def getCornerTiles(self, level, rect=None):
      """Calculate players corner tiles. An optional rect argument can be passed which gets used instead of players."""
      if not rect: rect = self.rect
      self.tileTopLeft = level.get((rect.left, rect.top), True)
      self.tileTopRight = level.get((rect.right, rect.top), True)
      self.tileMiddleLeft = level.get((rect.left, rect.centery), True)
      self.tileMiddleRight = level.get((rect.right, rect.centery), True)
      self.tileBottomLeft = level.get((rect.left, rect.bottom), True)
      self.tileBottomRight = level.get((rect.right, rect.bottom), True)
      self.tileMiddleLeft = level.get((rect.left, rect.centery), True)
      self.tileMiddleRight = level.get((rect.right, rect.centery), True)
         
   def checkOuterBounds(self):
      # Player cant go outside the screens sides, but can jump over top
      if self.rect.right < 0:
         self.rect.right = RES_WIDTH 
      if self.rect.right > RES_WIDTH:
         self.rect.left = 0
      if self.rect.top > RES_HEIGHT:
         self.rect.top = 0 # Falled through screen so move to top of screen
      if self.rect.bottom < 0:
         self.rect.top = RES_HEIGHT
   
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
      if self.state != Player.JUMPING: # Only if we're not already in the air
         self.getCornerTiles(level, self.rect.inflate(0, 2)) # We have to expand the rect we're passing as argument
         if not self.hasHitGround() and not self.isOnCloud(level): # Check expanded rect's position
            # We're in the air
            self.ySpeed = 0 # Start falling
            self.state = Player.JUMPING # Force state to be JUMPING
   
   def fixPosition(self, dir, level):
      """Check position of player at chosen direction and fix if we've hit something.
      
      Returns true if position is changed ("fixed").
      """
      # Works like this: If directions corners contains tiles who aren't walkable
      # we move player as far as we can (to the tile's side).
      if dir == UP:
         if self.hasHitCeiling():
            self.rect = self.oldRect
            self.rect.top = level.get((self.rect.centerx, self.rect.top), True).rect.top         
            return True
      elif dir == DOWN:
         if self.hasHitGround() or self.isOnCloud(level):
            self.rect = self.oldRect
            self.rect.bottom = level.get((self.rect.centerx, self.rect.bottom), True).rect.bottom-1 # Minus one (important!), because of how rects works
            return True
      elif dir == LEFT:
         if self.hasHitWall(dir):
            self.rect = self.oldRect
            self.rect.left = level.get((self.rect.left, self.rect.centery), True).rect.left
            return True
      elif dir == RIGHT:
         if self.hasHitWall(dir):
            self.rect = self.oldRect
            self.rect.right = level.get((self.rect.right, self.rect.centery), True).rect.right-1 # Minus one (important!), because of how rects works
            return True
            
      return False # We haven't changed the position of player

   def isOnCloud(self, level):
      """If player is on cloud return true, else return false."""
      if self.tileBottomLeft.isCloud or self.tileBottomRight.isCloud:
         if self.state != Player.JUMPING:
            return True
         
         # If we've come down here, player is in a jump, he's falling down
         # and he's in a cloud. Check if he just entered the cloud from above
         newTile = level.get((self.rect.centerx, self.rect.bottom), True)
         oldTile = level.get((self.oldRect.centerx, self.oldRect.bottom), True)

         if newTile.row > oldTile.row:
            return True
      return False

   def hasHitCeiling(self):
      return (not self.tileTopLeft.walkable or not self.tileTopRight.walkable)
      
   def hasHitWall(self, dir):
      if dir == LEFT: return (not self.tileTopLeft.walkable or not self.tileBottomLeft.walkable or not self.tileMiddleLeft.walkable)
      if dir == RIGHT: return (not self.tileTopRight.walkable or not self.tileBottomRight.walkable or not self.tileMiddleRight.walkable)

   
   def hasHitGround(self):
      return (not self.tileBottomLeft.walkable or not self.tileBottomRight.walkable)
