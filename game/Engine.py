from pyglet.gl import *

from game.Controller import Controller
from game.Vector import Vector

class Engine:

  window = None
  windowCenter = Vector()

  gameController = None

  groups = {} # TODO map from group to list of Entities

  time = 0
  prevTime = 0


  def __init__(self, window):
    self.window = window
    self.windowCenter = Vector(fromTuple=window.get_size()) / 2

    try:
      gameController = Controller()
    except: pass

  # DEBUG: draw a cross at the position of a vector
  def drawCross(self, v):
    r = 8
    glBegin(GL_LINES)
    glVertex2f(v.x  , v.y+r)
    glVertex2f(v.x  , v.y-r)
    glVertex2f(v.x+r, v.y  )
    glVertex2f(v.x-r, v.y  )
    glEnd()


  def run(self):
    glClearColor(0,0,0, 0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glColor3f(1.0, 0.0, 0.0)
    #self.drawCross(Vector(posX, posY)) # FIXME: mouse input

    if self.gameController: # if we have a controller
      glColor3f(0.0, 1.0, 0.0)
      self.drawCross(self.windowCenter + 100 * c.stick_l_raw)
      glColor3f(1.0, 1.0, 0.0)
      self.drawCross(self.windowCenter + 100 * c.stick_r_raw)

    glColor3f(1.0, 1.0, 1.0)
    self.drawCross(self.windowCenter)
