from pyglet.gl import *
from pyglet import clock

from Controller import Controller
from Vector import Vector

from Entities.DebugCross import DebugCross


class Engine:

  gameController = None

  # dictionary from group to list of Entities
  # don't modify this directly! use addEntity/removeEntity.
  groups = {
    'game':   [], # will draw dependent   on camera movement
    'UI':     [], # will draw independent of camera movement
    'player': [],
  }

  time = 0

  window = None
  windowCenter = Vector()
  mousePos = Vector()

  """
  @window.event
  def on_draw():
    pass # draw loop in here maybe?
  """


  def __init__(self):
    # Window
    self.window = pyglet.window.Window()
    @self.window.event
    def on_mouse_motion(x, y, dx, dy):
      self.mousePos = Vector(x, y)
    self.windowCenter = Vector(fromTuple=self.window.get_size()) / 2

    try:
      gameController = Controller()
    except: pass

    self.addEntity(DebugCross())

    clock.schedule(self.run)


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

    # UPDATE
    for entity in self.groups['game']:
      entity.update(dt)

    # DRAW
    # TODO: sort entities
    for entity in self.groups['game']:
      entity.draw()
#    glColor3f(1.0, 0.0, 0.0)

    if self.gameController: # if we have a controller
      glColor3f(0.0, 1.0, 0.0)
      self.drawCross(self.windowCenter + 100 * c.stick_l_raw)
      glColor3f(1.0, 1.0, 0.0)
      self.drawCross(self.windowCenter + 100 * c.stick_r_raw)

    glColor3f(1.0, 1.0, 1.0)
    self.drawCross(self.windowCenter)


  def addEntity(self, e):
    for group in e.groups:
      self.groups[group].append(e)

  def removeEntity(self, e):
    for group in e.groups:
      self.groups[group].remove(e)
