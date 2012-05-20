from pyglet import app, clock
from Vector import Vector
import pygame

# init pygame
pygame.init()

class Controller:

  j = None # our pygame.joystick

  joyID = 0 # note: is used as a static counter

  # these are filtered to be at a maximum length of 1
  stick_l = Vector(0.0, 0.0)
  stick_r = Vector(0.0, 0.0)
  # these come straight from the input
  stick_l_raw = Vector(0.0, 0.0)
  stick_r_raw = Vector(0.0, 0.0)
  
  def __init__(self):
    if self.joyID >= pygame.joystick.get_count(): # check we have a joystick
      raise Exception("OMG I CAN'T FIND ANY (more) JOYSTICKS!") # FIXME this needs to be a exception

    # Setup and init joystick
    self.j = pygame.joystick.Joystick(self.joyID)
    self.j.init()
    Controller.joyID += 1 # the next joystick created will use the next ID

    # Check init status
    if self.j.get_init() != 1: 
      self.printInfo()
      raise "OMG, something is wrong with this joystick"

    clock.schedule(self.checkInput) # maybe this wants to be elsewhere?
    #print "Joystick initialized"


  def checkInput(self, dt):
    for e in pygame.event.get():
      #print '%s: %s' % (pygame.event.event_name(e.type), e.dict)
      if e.type == pygame.JOYAXISMOTION:
        axis = e.dict['axis']
        val = e.dict['value']
        if   axis == 0: self.stick_l_raw.x = val
        elif axis == 1: self.stick_l_raw.y = val
        elif axis == 2: self.stick_r_raw.x = val
        elif axis == 3: self.stick_r_raw.y = val
        self.stick_r.copyFrom(self.stick_r_raw).constrainLength(1.0)
        self.stick_l.copyFrom(self.stick_l_raw).constrainLength(1.0)
       # print self.stick_l
        
      elif e.type == pygame.JOYHATMOTION: #TODO: this stuff
        print "d pad"
      elif e.type == pygame.JOYBUTTONUP:
        print "buttonUP"
      elif e.type == pygame.JOYBUTTONDOWN:
        print "buttonDOWN"
  

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

