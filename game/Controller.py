from pyglet import app, clock
from pymunk import Vec2d
import pygame

from PlayerInput import PlayerInput


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

if __name__ == "__main__":
  c = Controller()
  c.printInfo()
  app.run()

