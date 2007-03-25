#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tile import Tile
from variables import *
from animation import Animation
import pygame
from pygame.locals import *

class SurroundingTiles(object):
   """Help class for Player-class. Holds variables for player's surrounding (and center) tiles."""
   
   def __init__(self, rect, scene):
      self.forRect = rect
      self.getFunc = scene.level.get # Function used to fetch tiles
      self.setCenter()
      self.setSides()
      self.setCorners()
      
   def setCenter(self):
      rect = self.forRect
      self.center = self.getFunc((rect.centerx, rect.centery))
      
   def setSides(self):
      rect = self.forRect
      self.left = self.getFunc((rect.left, rect.centery))
      self.right = self.getFunc((rect.right, rect.centery))
      self.top = self.getFunc((rect.centerx, rect.top))
      self.bottom = self.getFunc((rect.centerx, rect.bottom))
      
   def getSides(self):
      return (self.top, self.right, self.bottom, self.left) # Return in clockwise order
   
   def setCorners(self):
      rect = self.forRect
      self.topLeft = self.getFunc((rect.left, rect.top))
      self.topRight = self.getFunc((rect.right, rect.top))
      self.bottomLeft = self.getFunc((rect.left, rect.bottom))
      self.bottomRight = self.getFunc((rect.right, rect.bottom))
   
   def getCorners(self):
      # Return in clockwise order, starting with topleft (maybe should be topright)
      return (self.topLeft, self.topRight, self.bottomRight, self.bottomLeft)
   
class Player(pygame.sprite.Sprite):

   JUMPSPEED = 14 # Speed at start of jump
   SPEED = 4 # Walking speed
   STANDING, JUMPING, CLIMBING = range(3) # States of player
   ANIMATIONSPEED = 15
   FRAMES = 4
   SIZE = (18,36) 

   def __init__(self, scene, image, keys):
      pygame.sprite.Sprite.__init__(self)
      
      self.scene = scene
      self.animation = Animation(image, Player.SIZE, Player.FRAMES)
      self.image = self.animation.getCurrentFrame()
      self.rect = self.image.get_rect()
      self.keyLeft, self.keyRight, self.keyUp, self.keyDown, self.keyJump = self.keys = keys
      self.xSpeed, self.ySpeed = (Player.SPEED, Player.SPEED) # xSpeed right = positive; ySpeed up = positive
      self.state = Player.JUMPING # Maybe change to STANDING later, but player begins in air right now
      self.isWalking = False
      self.facing = RIGHT
      self.frameCounter = 0
      
   def update(self, keyInput):
      self.frameCounter += 1
      if self.frameCounter % Player.ANIMATIONSPEED == 0: self.changeFrame()
      self.handleKeyInput(keyInput)
      self.fall()
      self.jump()
      self.checkForItems()

   def move(self, xMove, yMove):
      """Move players rect and get corner tiles at new position."""
      self.oldRect = pygame.Rect(self.rect)
      self.rect.move_ip(xMove, -yMove) # yMove is negative because of ySpeed up = positive
      self.checkOuterBounds() # If we're outside map at new pos, move player
      self.setTiles() # get surrounding tiles of player
   
   def setTiles(self, rect=None):
      """Sets player's present and previous surrounding tiles.
      
      An optional rect argument can be passed, wich gets used instead.
      """
      if rect:
         self.tiles = SurroundingTiles(rect, self.scene)
      else:
         self.oldTiles = SurroundingTiles(self.oldRect, self.scene)
         self.tiles = SurroundingTiles(self.rect, self.scene)
      
   def handleKeyInput(self, keyInput):
      """Handles the different keys pressed on the keyboard."""
      self.isWalking = False
      
      if keyInput[self.keyJump] and self.state not in (Player.JUMPING, Player.CLIMBING):
         self.state = Player.JUMPING
         self.ySpeed = Player.JUMPSPEED
      
      if keyInput[self.keyLeft]:
         self.move(-self.xSpeed, 0)
         if self.facing == RIGHT: self.changeDirection()
         self.isWalking = True
         if self.state == Player.CLIMBING:
            if self.hasHitWall(LEFT): self.rect = self.oldRect
            else: self.state = Player.JUMPING # we moved into air or onto ground
         else: # move as usual
            self.fixPosition(LEFT)
      elif keyInput[self.keyRight]:
         self.move(self.xSpeed, 0)
         if self.facing == LEFT: self.changeDirection()
         self.isWalking = True
         if self.state == Player.CLIMBING:
            if self.hasHitWall(RIGHT): self.rect = self.oldRect
            else: self.state = Player.JUMPING # we moved into air or onto ground
         else: # move as usual
            self.fixPosition(RIGHT)
            
      if keyInput[self.keyUp] and self.state != Player.JUMPING:
         self.move(0, Player.SPEED)
         if self.canClimb(UP): # also fixes pos if we hit ceiling and is on ladder
            self.climb()
         else:
            self.rect = self.oldRect
      elif keyInput[self.keyDown] and self.state != Player.JUMPING:
         self.move(0, -Player.SPEED)
         if self.canClimb(DOWN):
            self.climb()
         elif not self.fixPosition(DOWN): # Check if we've hit ground, and fix position in that case
            self.state = Player.JUMPING # Else we're in the air

   def changeDirection(self):
      """Change which way the player is facing, adjust self.facing and currentFrame acordingly"""
      if self.facing == LEFT:
         self.animation.currentFrame = 0
         self.facing = RIGHT
      elif self.facing == RIGHT:
         self.animation.currentFrame = Player.FRAMES*2 - 1
         self.facing = LEFT
      self.changeFrame()

   def changeFrame(self):
      """Go to the next frame if we are walking, go to first if we passed the last or if we aren't walking. note that the frames facing left are mirrored, therefor we do -1 instead of +1"""  
      if self.facing  == RIGHT:
         if self.isWalking is True: self.animation.currentFrame += 1
         if self.animation.currentFrame == Player.FRAMES or self.isWalking == False: self.animation.currentFrame = 0
      elif self.facing == LEFT:
         if self.isWalking is True: self.animation.currentFrame += -1
         if self.animation.currentFrame == Player.FRAMES - 1 or self.isWalking == False: self.animation.currentFrame = Player.FRAMES*2 - 1
      self.image = self.animation.getCurrentFrame()   
         
   def checkOuterBounds(self):
      # Player cant go outside the screens sides, but can jump over top
      if self.rect.right < 0:
         self.rect.left = RES_WIDTH-1 
      if self.rect.left > RES_WIDTH:
         self.rect.right = 1
      if self.rect.top > RES_HEIGHT:
         self.rect.bottom = 0 # Falled through screen so move to top of screen
   
   def checkForItems(self):
      """Check if player's walked on level items and run their walked on method."""
      # could also use pygame.sprite.spritecollide(self, self.scene.level.itemTiles)
      self.setTiles(self.rect) # Ensure surrounding tiles are up to date (but don't set self.oldTiles)
      items = [tile.item for tile in self.tiles.getCorners() if tile.item]
      for item in items:
         item.walkedOn(self)
   
   def jump(self):
      if self.state != Player.JUMPING: return
      # Player is in the air.
      self.ySpeed -= GRAVITY
      # If speed is too high we might miss tiles (and begin moving through walls)
      if self.ySpeed < -Tile.HEIGHT: self.ySpeed = -Tile.HEIGHT # speed is bigger than tile's height
      elif self.ySpeed > Tile.HEIGHT: self.ySpeed = Tile.HEIGHT
      
      self.move(0, self.ySpeed)
      if self.ySpeed > 0: # we're going up
         fixedPos = self.fixPosition(UP)
         if fixedPos:
            self.ySpeed = 0 # we've hit a tile above us. Fall down again.
      elif self.ySpeed < 0: # we're going down
         fixedPos = self.fixPosition(DOWN)
         if fixedPos:
            self.ySpeed = 0
            self.state = Player.STANDING # We've fallen down to solid ground
   
   def fall(self):
      """Check if we have stepped out into air."""
      if self.state in (Player.JUMPING, Player.CLIMBING): return # Only if we're not already in the air or climbing
      
      # We have to check if there's air underneath us.
      # Use setTiles with an expanded rect to accomplish this,
      # but save the real tiles first. We'll set them back later, to avoid strange bugs
      temp = self.tiles
      self.setTiles(self.rect.inflate(0, 2))
      if not self.hasHitGround() and not self.isOnCloud():
         self.state = Player.JUMPING # Force state to be JUMPING
      self.tiles = temp # Set the real tiles again
   
   def climb(self):
      self.state = Player.CLIMBING
      self.rect.centerx = self.tiles.center.rect.centerx # center player on X-axis in tile
   
   def fixPosition(self, dir):
      """Check position of player at chosen direction and fix if we've hit something.
      
      Returns true if position is changed ("fixed").
      """
      # Works like this: If directions corners contains tiles who aren't walkable
      # we move player as far as we can (to the tile's side).
      if dir == UP:
         if self.hasHitCeiling():
            self.rect = self.oldRect
            self.rect.top = self.oldTiles.top.rect.top         
            return True
      elif dir == DOWN:
         if self.hasHitGround() or self.isOnCloud():
            self.rect = self.oldRect
            self.rect.bottom = self.oldTiles.bottom.rect.bottom-1 # Minus one (important!), because of how rects works
            return True
      elif dir == LEFT:
         if self.hasHitWall(dir):
            self.rect = self.oldRect
            self.rect.left = self.oldTiles.left.rect.left
            return True
      elif dir == RIGHT:
         if self.hasHitWall(dir):
            self.rect = self.oldRect
            self.rect.right = self.oldTiles.right.rect.right-1 # Minus one (important!), because of how rects works
            return True
            
      return False # We haven't changed the position of player
   
   def canClimb(self, dir):
      if dir == DOWN:
         # Check if there's ladder at bottom
         if self.tiles.bottom.ladder: return True
      elif dir == UP:
         # If we we're on ladder (player top or bottom)
         if self.oldTiles.bottom.ladder or self.oldTiles.top.ladder:
            # and climbed onto ladder or into air
            if self.tiles.top.ladder or not self.hasHitCeiling():
               return True
            elif self.hasHitCeiling():
               # If we hit ceiling, move player as far as we can (tile's top side)
               self.rect = self.oldRect
               self.rect.top = self.oldTiles.top.rect.top
               return True
      return False

   def isOnCloud(self):
      """If player is on cloud return true, else return false."""
      if self.tiles.bottomLeft.isCloud or self.tiles.bottomRight.isCloud:
         if self.state != Player.JUMPING:
            return True
         # If we've come down here, player is in a jump, he's falling down
         # and he's in a cloud. Check if he just entered the cloud from above
         if self.tiles.bottom.row > self.oldTiles.bottom.row:
            return True
      return False
   
   def hasHitCeiling(self):
      return (not self.tiles.topLeft.isWalkable or not self.tiles.topRight.isWalkable)
      
   def hasHitWall(self, dir):
      if dir == LEFT: return (not self.tiles.topLeft.isWalkable or not self.tiles.bottomLeft.isWalkable or not self.tiles.left.isWalkable)
      if dir == RIGHT: return (not self.tiles.topRight.isWalkable or not self.tiles.bottomRight.isWalkable or not self.tiles.right.isWalkable)
   
   def hasHitGround(self):
      return (not self.tiles.bottomLeft.isWalkable or not self.tiles.bottomRight.isWalkable)
