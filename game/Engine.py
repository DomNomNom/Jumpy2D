from pyglet.gl import *
from pyglet import clock

from game.Controller import Controller
from game.Vector import Vector

class Engine:

  gameController = None

  groups = {} # TODO map from group to list of Entities

  time = 0

  window = pyglet.window.Window()
  windowCenter = Vector()
  mousePos = Vector()

  """
  @window.event
  def on_draw():
    pass # draw loop in here maybe?
  """


  def __init__(self):
    # Window events
    @self.window.event
    def on_mouse_motion(x, y, dx, dy):
      self.mousePos = Vector(x, y)

    self.windowCenter = Vector(fromTuple=self.window.get_size()) / 2

    clock.schedule(self.run)

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


  def run(self, dt):
    glClearColor(0,0,0, 0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glColor3f(1.0, 0.0, 0.0)
    self.drawCross(self.mousePos)

    if self.gameController: # if we have a controller
      glColor3f(0.0, 1.0, 0.0)
      self.drawCross(self.windowCenter + 100 * c.stick_l_raw)
      glColor3f(1.0, 1.0, 0.0)
      self.drawCross(self.windowCenter + 100 * c.stick_r_raw)

    glColor3f(1.0, 1.0, 1.0)
    self.drawCross(self.windowCenter)


  def addEntity(e):
    pass #TODO

  def removeEntity(e):
    pass # TODO
