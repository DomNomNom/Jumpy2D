# Things for PlayCurrentLevel
from game.KeyboardControl import KeyboardControl
from game.Controller import Controller
from game.Entities.Player import Player

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

  class PlayCurrentLevel(BaseState):
    def start(self):
      playerInput = KeyboardControl()
      try: playerInput = Controller() # use game pad input if we have one
      except: pass
      self.player = Player(playerInput, pos=(320, 240))
      game.engine.addEntity(self.player)
    def focus(self):   self.player.input.currentlyRecording = True
    def unfocus(self): self.player.input.currentlyRecording = False
    def end(self):
      self.player
      #for entity in game.engine.groups['game']:
      #  game.engine.removeEntity(entity)
