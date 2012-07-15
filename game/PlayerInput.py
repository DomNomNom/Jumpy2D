import time
import globals as game

import pygame # for controller

from pyglet.window import key # for keyboard
from pyglet.resource import file as resourceOpen

from game.Resources import createFile # for saving replays

from pymunk import Vec2d

class PlayerInput:

  actionQueue = []  # queue of PlayerAction. This is for the Player to process
  actionLog = []    # list  of PlayerAction. This is for the Replay to process

  currentAim = 0.0  # should only be used for cosmetics (not for rocket firing direction)

  currentlyRecording = False
  
  level = None # For recording levelTime and level. This gets initialized be Level

  def recordAction(self, actionType, moveDir=None):
    if not self.currentlyRecording: return
    action = self.PlayerAction(self.level, actionType, self.currentAim, moveDir)
    self.actionQueue.append(action)
    self.actionLog.append(repr(action))
    #print "Action:", action

  def checkInput(self, dt):
    # do recordAction when you have corresponding input
    pass

  def saveReplay(self):
    replayName = str(int(time.time()*10000)) + '.replay'
    with createFile('Replays/'+self.level.levelName, replayName) as f:
      for action in self.actionLog:
        f.write(action + '\n')


  class PlayerAction:
    ''' A small class to hold information about a action '''
    actionTypes = ['move', 'jump', 'shoot', 'shoot2']

    def __init__(self, level, actionType, aim, moveDir=None):
      assert actionType in self.actionTypes, str(actionType) + ' is not a actionType'
      self.type = actionType
      self.aim = aim
      self.time = level.levelTime
      self.moveDir = moveDir
      if moveDir != None:
        self.moveDir = max(min(moveDir, 1), -1) # constraint:  -1 <= moveDir <= 1

    def __repr__(self):
      return repr((
        self.type,
        self.aim,
        self.time,
        self.moveDir,
      ))


class Controller(PlayerInput):

  prevDirection = 0

  j = None # our pygame.joystick

  joyID = 0 # note: is used as a static counter

  # these come straight from the input
  stick_l = Vec2d(0.0, 0.0)
  stick_r = Vec2d(0.0, 0.0)

  # button bindings
  bindings = {
    4 : 'jump',
    6 : 'shoot',
    7 : 'shoot2',
  }


  def __init__(self):
    # init pygame
    pygame.init()

    if self.joyID >= pygame.joystick.get_count(): # check we have a joystick
      raise Exception("OMG I CAN'T FIND ANY (more) JOYSTICKS!")

    # Setup and init joystick
    self.j = pygame.joystick.Joystick(self.joyID)
    self.j.init()
    Controller.joyID += 1 # the next joystick created will use the next ID

    # Check init status
    if self.j.get_init() != 1:
      self.printInfo()
      raise Exception("OMG, something is wrong with this joystick")

    # TODO: move this to a config file
    if "PLAYSTATION(R)3" in self.j.get_name():
      self.bindings = {
        10 : 'jump',
        11 : 'shoot',
        9  : 'shoot2',
      }

    #self.printInfo()
    #print "Joystick initialized"

  def checkInput(self):
    for e in pygame.event.get():
      #print '%s: %s' % (pygame.event.event_name(e.type), e.dict)
      if e.type == pygame.JOYAXISMOTION:
        axis = e.dict['axis']
        val = e.dict['value']
        if   axis == 0: self.stick_l.x = val
        elif axis == 1: self.stick_l.y = val
        elif axis == 2: self.stick_r.x = val
        elif axis == 3: self.stick_r.y = val

        if self.stick_r == Vec2d(0,0):
          self.currentAim = Vec2d(0,-1).angle
        else:
          self.currentAim = -self.stick_r.angle

        direction = round(self.stick_l.x)
        if direction != self.prevDirection:
          self.recordAction('move', direction)
          self.prevDirection = direction
        #print self.stick_l
        #print self.currentAim

      elif e.type == pygame.JOYHATMOTION: #TODO
        print "d pad", e.dict
      elif e.type == pygame.JOYBUTTONDOWN:
        #print "buttonDOWN:", e.dict
        button = e.dict['button']
        if button in self.bindings:
          self.recordAction(self.bindings[button])
      elif e.type == pygame.JOYBUTTONUP:
        pass #print "buttonUP  :", e.dict


  def printInfo(self):
    print "Joystick ID: ", self.j.get_id()
    print "Joystick Name: ", self.j.get_name()
    print "No. of axes: ", self.j.get_numaxes()
    print "No. of trackballs: ", self.j.get_numballs()
    print "No. of buttons: ", self.j.get_numbuttons()
    #print "No. of hat controls: ", self.j.get_numhats()




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

    # jump
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
        gameMousePos = game.engine.camera.toModelSpace(game.engine.mousePos)
      self.currentAim = (gameMousePos - controlledPlayer.pos).angle
