import game.globals as game

class GameState(object):
  ''' A class to manage state transitions '''
  
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
    self.stateStack.pop().end()
    self.stateStack[-1].focus()


  ## States from here on

  class BaseState(object):
    def start(self):    pass
    def focus(self):    pass
    def unfocus(self):  pass
    def end(self):      pass
