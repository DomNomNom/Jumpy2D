from pyglet.window import key

import game.globals as game
from PlayerInput import PlayerInput

class KeyboardControl(PlayerInput):

  prevDirection = 0
  prevJump = False

  def __init__(self):
    self.keys = key.KeyStateHandler()
    game.engine.window.push_handlers(self.keys)

  def checkInput(self):
    # walking
    direction = int(self.keys[key.RIGHT]) - int(self.keys[key.LEFT])
   #direction = int(self.keys[key.D    ]) - int(self.keys[key.A   ]) # WASD control.  TODO: rebindable keys?
    if direction != self.prevDirection:
      self.recordAction('move', direction)
      self.prevDirection = direction

    #jump
    jump = self.keys[key.UP]
    if jump and not self.prevJump:
      self.recordAction('jump')
    self.prevJump = jump
