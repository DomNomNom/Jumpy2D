# Things for PlayCurrentLevel
from game.Entities.Player import Player
from game.Entities.Editor import Editor

from Entities.Level import Level

import game.globals as game

class GameState(object):
  '''
  A class to manage state transitions.

  it involves a lot of "glue" that just ties the game together
  '''

  def __init__(self):
    # our states are in a stack,
    # eg. we know that we are in the pauseMenu, while playing, while editing
    self.stateStack = [GameState.BaseState()] # always have one base state.

  def pushState(self, state):
    self.stateStack[-1].unfocus()
    state.start()
    state.focus()
    self.stateStack.append(state)

  def popState(self):
    toEnd = self.stateStack.pop()
    toEnd.unfocus()
    toEnd.end()
    self.stateStack[-1].focus()


  ## States from here on

  class BaseState(object):
    def start(self):    pass # does things like creating entities
    def focus(self):    pass # does things like setting up mouse listeners
    def unfocus(self):  pass # undoes focus()
    def end(self):      pass # undoes start()

  class Play(BaseState):
    def __init__(self, playerInputs, levelName):
      assert playerInputs
      self.levels = [Level(playerInput, levelName) for playerInput in playerInputs]
      self.primaryLevel = self.levels[0]
    def start(self):
      for level in self.levels:
        game.engine.addEntity(level)
    def focus(self):   
      for level in self.levels: level.setPaused(False)
      game.engine.camera.trackingFunction = lambda: game.engine.windowCenter-self.primaryLevel.player.pos
    def unfocus(self): 
      for level in self.levels: level.setPaused(True )
      game.engine.camera.resetTracking()
    def end(self):
      for level in self.levels: 
        level.player.input.saveReplay()
        game.engine.removeEntity(level.player)
      for entity in game.engine.groups['game']: # note: this seems a bit wrong :/
        game.engine.removeEntity(entity)

  class editLevel(BaseState):
    def __init__(self):
      self.editor = Editor()
    def start(self):
      game.engine.addEntity(self.editor)
    def focus(self):
      self.editor.focus = True
    def unfocus(self):
      self.editor.focus = False
    def end(self):
      self.editor.level.save()
      game.engine.removeEntity(self.editor)
