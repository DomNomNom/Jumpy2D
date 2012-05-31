from pyglet.window import key

import game.globals as game
from PlayerInput import PlayerInput

class KeyboardControl(PlayerInput):

  lastDirection = 0

  def __init__(self):
    self.keys = key.KeyStateHandler()
    game.engine.window.push_handlers(self.keys)
    
  def checkInput(self):
    direction = int(self.keys[key.RIGHT]) - int(self.keys[key.LEFT])
   #direction = int(self.keys[key.D    ]) - int(self.keys[key.A   ]) # WASD control
    
    if direction != self.lastDirection:
      self.recordAction('move', direction)
      self.lastDirection = direction
