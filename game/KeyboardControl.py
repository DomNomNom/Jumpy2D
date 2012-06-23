from pyglet.window import key

import game.globals as game
from PlayerInput import PlayerInput

class KeyboardControl(PlayerInput):

  prevDirection = 0
  prevJump = False


  def __init__(self):
    self.keys = key.KeyStateHandler()
    game.engine.window.push_handlers(self.keys)
    self.keyBindings = { # note: this will be re-bound below
      'left'  : key.LEFT,
      'right' : key.RIGHT,
      'jump'  : key.UP,
    }
    self.keyBindings = { # re-bind with WASD control
      'left'  : key.A,
      'right' : key.D,
      'jump'  : key.W,
    }

    @game.engine.window.event
    def on_mouse_press(x, y, button, modifiers):
      self.recordAction('shoot')


  def checkInput(self):
    kb = self.keyBindings # shorthand

    # walk
    direction = int(self.keys[kb['right']]) - int(self.keys[kb['left']])
    if direction != self.prevDirection:
      self.recordAction('move', direction)
      self.prevDirection = direction

    #jump
    jump = self.keys[kb['jump']]
    if jump and not self.prevJump:
      self.recordAction('jump')
    self.prevJump = jump

    # aim: point towards the mouse
    # note: this is an ugly hack as it is getting the player it controls
    controlledPlayer = None
    for p in game.engine.groups['player']:
      if p.input is self:
        controlledPlayer = p
    if controlledPlayer:
      with game.engine.camera.shiftView():
        gameMousePos = game.engine.camera.toScreenView(game.engine.mousePos)
      self.currentAim = (gameMousePos - controlledPlayer.pos).angle
