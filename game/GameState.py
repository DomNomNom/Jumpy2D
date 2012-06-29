# Things for PlayCurrentLevel
from game.Entities.Player import Player

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
    # TODO: do stuff

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
      self.levels = []
      for playerInput in playerInputs:
        self.levels.append(Level(playerInput, levelName))
    def start(self):
      for level in self.levels:
        game.engine.addEntity(level)
    def focus(self):   self.setRecording(True )
    def unfocus(self): self.setRecording(False)
    def end(self):
      for level in self.levels: game.engine.removeEntity(level.player)
      #for entity in game.engine.groups['game']:
      #  game.engine.removeEntity(entity)
    def setRecording(self, recording):
      for level in self.levels: level.player.input.currentlyRecording = recording
