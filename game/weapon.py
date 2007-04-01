#!/usr/bin/env python
# -*- coding: utf-8 -*-

from variables import *

import pygame
from pygame.locals import *
      
class Weapon(object):

   SHOOTSPEED = 40 # higher value = longer pauses between shooting
   
   def __init__(self, scene, obj):
      self.scene = scene
      self.obj = obj
      self.bullets = pygame.sprite.Group()
      self.lastShot = pygame.time.get_ticks()
      self.bulletClass = Bullet # Class to use for bullets
      
   def canShoot(self):
      """You can shoot if long enough time has gone."""
      return (pygame.time.get_ticks() > Weapon.SHOOTSPEED+self.lastShot)
   
   def shoot(self, dir):
      self.lastShot = pygame.time.get_ticks()
      if dir == LEFT: x = self.obj.rect.left
      elif dir == RIGHT: x = self.obj.rect.right
      pos = (x, self.obj.rect.centery) # todo: maybe change start pos depending on weapon's pos
      bullet = self.bulletClass(self.scene, pos, dir)
      self.bullets.add(bullet) # keep track of this weapon's fired bullets
      
class Bullet(pygame.sprite.Sprite):
   
   DAMAGE = 5
   SPEED = 8 # must be over player's max speed
   
   def __init__(self, scene, pos, dir):
      pygame.sprite.Sprite.__init__(self)
      
      self.scene = scene
      self.scene.level.bullets.add(self) # add to level's bullet group
      self.dir = dir
      
      image = pygame.Surface((2, 1))
      image.fill((255, 0, 0)) # red
      self.image, self.rect = image, image.get_rect()
      x, y = pos
      if dir == LEFT: x -= self.rect.width # add width to x pos if we're moving left
      self.rect.x, self.rect.centery = (x, y)
   
   def update(self):
      """Move and check if bullet has hit any players."""
      # move left or right
      if self.dir == LEFT: self.move(-Bullet.SPEED, 0)
      elif self.dir == RIGHT: self.move(Bullet.SPEED, 0)
      
      # check if we hit something not walkable
      if self.hasHitCeiling() or self.hasHitGround() or self.hasHitWall(LEFT) or self.hasHitWall(RIGHT):
         self.kill()
      
      # check if we hit players
      hitPlayers = pygame.sprite.spritecollide(self, self.scene.players, False)
      if len(hitPlayers) > 0:
         for player in hitPlayers:
            self.playerHit(player)
         self.kill()
   
   def playerHit(self, player):
      """A player has been hit."""
      player.health -= Bullet.DAMAGE
      if player.health <= 0: self.scene.playerKilled(player) # tell scene object that a player has been killed
   
   def move(self, xMove, yMove):
      self.rect.move_ip(xMove, -yMove)
      self.checkOuterBounds()
      self.tiles = SurroundingTiles(self.rect, self.scene) # to check if we've hit something
      
   def checkOuterBounds(self):
      # if we're outside level, we remove bullet
      if not self.rect.colliderect(self.scene.game.screen.get_rect()):
         # bullet and screen don't overlap
         self.kill()
   
   # These methods are copied from player.py's Player
   
   def hasHitCeiling(self):
      return (not self.tiles.topLeft.isWalkable or not self.tiles.topRight.isWalkable)
      
   def hasHitWall(self, dir):
      if dir == LEFT: return (not self.tiles.topLeft.isWalkable or not self.tiles.bottomLeft.isWalkable or not self.tiles.left.isWalkable)
      if dir == RIGHT: return (not self.tiles.topRight.isWalkable or not self.tiles.bottomRight.isWalkable or not self.tiles.right.isWalkable)
   
   def hasHitGround(self):
      return (not self.tiles.bottomLeft.isWalkable or not self.tiles.bottomRight.isWalkable)
