#!/usr/bin/env python
# -*- coding: utf-8 -*-

from level import Tile
from variables import *
from animation import Animation
import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):

   JUMPSPEED = 8 # Speed at start of jump
   SPEED = 2 # Walking speed
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

   def move(self, xMove, yMove):
      """Move players rect and get corner tiles at new position."""
      self.oldRect = pygame.Rect(self.rect)
      self.rect.move_ip(xMove, -yMove) # yMove is negative because of ySpeed up = positive
      self.checkOuterBounds() # If we're outside map at new pos, move player
      self.getCornerTiles() # Get corner tiles at new pos (used later, for example in self.fixPosition())
      self.getSideTiles()
      
   def handleKeyInput(self, keyInput):
      """Handles the different keys pressed on the keyboard."""
      self.isWalking = False
      if keyInput[self.keyJump] and self.state != Player.JUMPING:
         self.state = Player.JUMPING
         self.ySpeed = Player.JUMPSPEED
      if keyInput[self.keyLeft]:
         self.move(-self.xSpeed, 0)
         if self.facing == RIGHT: self.changeDirection()
         self.isWalking = True
         self.fixPosition(LEFT)
      if keyInput[self.keyRight]:
         self.move(self.xSpeed, 0)
         if self.facing == LEFT: self.changeDirection()
         self.isWalking = True
         self.fixPosition(RIGHT)

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

   def getCornerTiles(self, rect=None):
      """Calculate players corner tiles.
      
      An optional rect argument can be passed which gets used instead of players.
      """
      if not rect: rect = self.rect
      self.tileTopLeft = self.scene.level.get((rect.left, rect.top))
      self.tileTopRight = self.scene.level.get((rect.right, rect.top))
      self.tileBottomLeft = self.scene.level.get((rect.left, rect.bottom))
      self.tileBottomRight = self.scene.level.get((rect.right, rect.bottom))
   
   def getSideTiles(self, rect=None):
      """Calculate players tiles on his four sides.
      
      An optional rect argument can be passed which gets used instead of players.
      """
      if not rect: rect = self.rect
      self.tileLeft = self.scene.level.get((rect.left, rect.centery))
      self.tileRight = self.scene.level.get((rect.right, rect.centery))
      self.tileTop = self.scene.level.get((rect.centerx, rect.top))
      self.tileBottom = self.scene.level.get((rect.centerx, rect.bottom))     
         
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
   
   def jump(self):
      if self.state != Player.JUMPING: return
      # Player is in the air.
      self.ySpeed -= GRAVITY
      # If speed is too high we might miss tiles (and begin moving through walls)
      if self.ySpeed > Tile.HEIGHT: self.ySpeed = Tile.HEIGHT # speed is bigger than tile's height
      
      self.move(0, self.ySpeed)
      if self.ySpeed > 0: # we're going up
         fixedPos = self.fixPosition(UP)
         if fixedPos: self.ySpeed = 0 # we've hit a tile above us. Fall down again.
      elif self.ySpeed < 0: # we're going down
         fixedPos = self.fixPosition(DOWN)
         if fixedPos: self.state = Player.STANDING # We've fallen down to solid ground
   
   def fall(self):
      """Check if we have stepped out into air."""
      if self.state == Player.JUMPING: return # Only if we're not already in the air
      self.getCornerTiles(self.rect.inflate(0, 2)) # We have to expand the rect we're passing as argument
      if not self.hasHitGround() and not self.isOnCloud(): # Check expanded rect's position
         # We're in the air
         self.ySpeed = 0 # Start falling
         self.state = Player.JUMPING # Force state to be JUMPING
   
   def fixPosition(self, dir):
      """Check position of player at chosen direction and fix if we've hit something.
      
      Returns true if position is changed ("fixed").
      """
      # Works like this: If directions corners contains tiles who aren't walkable
      # we move player as far as we can (to the tile's side).
      if dir == UP:
         if self.hasHitCeiling():
            self.rect = self.oldRect
            self.rect.top = self.scene.level.get((self.rect.centerx, self.rect.top)).rect.top         
            return True
      elif dir == DOWN:
         if self.hasHitGround() or self.isOnCloud():
            self.rect = self.oldRect
            self.rect.bottom = self.scene.level.get((self.rect.centerx, self.rect.bottom)).rect.bottom-1 # Minus one (important!), because of how rects works
            return True
      elif dir == LEFT:
         if self.hasHitWall(dir):
            self.rect = self.oldRect
            self.rect.left = self.scene.level.get((self.rect.left, self.rect.centery)).rect.left
            return True
      elif dir == RIGHT:
         if self.hasHitWall(dir):
            self.rect = self.oldRect
            self.rect.right = self.scene.level.get((self.rect.right, self.rect.centery)).rect.right-1 # Minus one (important!), because of how rects works
            return True
            
      return False # We haven't changed the position of player

   def isOnCloud(self):
      """If player is on cloud return true, else return false."""
      if self.tileBottomLeft.isCloud or self.tileBottomRight.isCloud:
         if self.state != Player.JUMPING:
            return True
         
         # If we've come down here, player is in a jump, he's falling down
         # and he's in a cloud. Check if he just entered the cloud from above
         newTile = self.scene.level.get((self.rect.centerx, self.rect.bottom))
         oldTile = self.scene.level.get((self.oldRect.centerx, self.oldRect.bottom))

         if newTile.row > oldTile.row:
            return True
      return False

   def hasHitCeiling(self):
      return (not self.tileTopLeft.isWalkable or not self.tileTopRight.isWalkable)
      
   def hasHitWall(self, dir):
      if dir == LEFT: return (not self.tileTopLeft.isWalkable or not self.tileBottomLeft.isWalkable or not self.tileLeft.isWalkable)
      if dir == RIGHT: return (not self.tileTopRight.isWalkable or not self.tileBottomRight.isWalkable or not self.tileRight.isWalkable)
   
   def hasHitGround(self):
      return (not self.tileBottomLeft.isWalkable or not self.tileBottomRight.isWalkable)
