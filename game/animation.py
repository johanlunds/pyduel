#!/usr/bin/env python
# -*- coding: utf-8 -*-

from variables import *

import pygame
from pygame.locals import *

# TODO: new property "previous"?

class Animation(object):
   """Used to get the ability to animate sprites.
   
   Should be property of the animated sprite, and call update() method every game loop."""
   
   def __init__(self, obj):
      self.obj = obj # The animation owner. Must have image property
      # self.sequences format: {name: (((frameNumber, duration), [...]), repeat), [...]}
      self.sequences = {}
      
      # Difference between stopped and paused:
      # When paused you can continue were you were.
      # When stopped you have to start new sequence
      self.isStopped, self.isPaused = (True, True)
      
      self.current, self.next = (None, None) # Current and next sequence
      self.seqFrame = 0 # The sequences frame (not an self.frames index)
      self.counter = 0 # Frame counter, incremented in self.update()

   def loadFrames(self, image, numFrames, defaultFrame=0, flipX=False, flipY=False, flipXAndY=False):
      """Loads the frames used in the animation sequences. Must be called after initiation of object."""
      self.image = image
      self.defaultFrame = defaultFrame # an index in self.frames
      self.frames = [] # Holds images
      
      imageRect = image.get_rect()
      # Make rect for one frame
      frameRect = pygame.rect.Rect(0, 0, imageRect.width/numFrames, imageRect.height) # x, y, w, h
      
      images = [] # (image, reverse)
      images.append((image, False))
      if flipX: images.append((pygame.transform.flip(image, True, False), True))
      if flipY: images.append((pygame.transform.flip(image, False, True), False))
      if flipXAndY: images.append((pygame.transform.flip(image, True, True), True))
      
      for image, reverse in images:
         frames = []
         for i in range(numFrames):
            frames.append(image.subsurface(frameRect.move(i*frameRect.width, 0)))
         if reverse: frames.reverse()
         self.frames.extend(frames)
      
      return (self.frames[self.defaultFrame], frameRect) # (image, rect)

   def addSequence(self, name, frames, repeat=True):
      # frames = ((frameNumber, duration), [...])
      self.sequences[name] = (frames, repeat)
   
   def getCurrent(self):
      """Return current sequence as (name, sequence). Returns (None, None) if no current."""
      if self.current is None: return (None, None)
      return (self.current, self.sequences[self.current]) # return name and sequence in tuple
   
   def getDefaultImage(self):
      """Returns image surface."""
      return self.frames[self.defaultFrame] # return image
   
   def getFrame(self, frame):
      """Returns image surface."""
      return self.frames[frame]
   
   def start(self, name):
      if name is None: raise StandardError, "Invalid name of sequence (name is None)."
      self.isStopped, self.isPaused = (False, False)
      self.current, self.next = (name, None)
      self.seqFrame = 0
      self.counter = 0
   
   def stop(self):
      """When stop() is called, you have to call start() method with new sequence to begin again."""
      self.isStopped = True
      self.current, self.next = (None, None)
   
   def pause(self):
      """If you only pause, you can continue current sequence."""
      self.isPaused = True
   
   def unpause(self):
      """Continue current animation sequence."""
      self.isPaused = False
   
   def setNext(self, name):
      if self.isStopped: # If we're not running one right now, start next
         self.start(name)
      else:
         self.next = name

   def next(self):
      """Run next sequence."""
      if self.next is None:
         self.pause() # Pause at what is probably the last frame in current sequence
      else:
         self.start(self.next)
   
   def update(self):
      if self.isStopped or self.isPaused: return
      elif self.current is None: return
      elif self.image is None: raise StandardError, "Update method can't run without loaded frames."
      
      frames, repeat = self.sequences[self.current]
      # self.seqFrame = the current sequence's frame number (not a self.frames index)
      frameNum, duration = frames[self.seqFrame] # frameNum = an index in self.frames
      self.obj.image = self.frames[frameNum] # The real magic: change animation owners image
      
      self.counter += 1 # Increase frame counter
      if self.counter >= duration: # change to next frame
         self.seqFrame += 1
         if self.seqFrame < len(frames): # not end of sequence
            self.counter = 0
         else: # start new sequence
            if repeat: self.start(self.current) # repeat current sequence
            else: self.next()
      
