from pyglet.gl import *
from pyglet import clock
import time

from Controller import Controller
from Vector import Vector
from Entities.Editor import Editor


class Engine:

  gameController = None

  # dictionary from group to list of Entities. they are NOT mutually exclusive
  # don't manually add to this directly! use addEntity/removeEntity.
  groups = {
    'all':      set(), # all entities should be in here
    'updating': set(), # everything that wants to be updated goes in here
    'game':     set(), # will draw dependent   on camera movement
    'UI':       set(), # will draw independent of camera movement
    'player':   set(),
    'UI_editor': set(), # entites that are part of the editor UI
  }


  # layers specify the order in which they are drawn. (ordered back to front)
  drawLayerNames = [
    'background',
    'game',
    'player',
    # UI ones from here on
    'UI_editor',
    'UI_pauseMenu',
    'UI_debug'
  ]

  # A dict from drawLayerNames to a list of entities. they are mutually exclusive
  # TODO: would it make sense to have a batch draw for each of these?
  drawLayers = {}


  levelStartTime = time.time()

  window = None
  windowCenter = Vector()
  mousePos = Vector()

  """
  @window.event
  def on_draw():
    pass # draw loop in here maybe?
  """


  def __init__(self):
    # init draw layers
    for name in self.drawLayerNames:
      self.drawLayers[name] = []

    # Window
    self.window = pyglet.window.Window()
    self.windowCenter = Vector(fromTuple=self.window.get_size()) / 2

    # update our mousePos on every move event
    @self.window.event
    def on_mouse_motion(x, y, dx, dy):
      self.mousePos = Vector(x, y)
    @self.window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
      self.mousePos = Vector(x, y)

    try:
      gameController = Controller()
    except: pass

    # shedule our main loop so we don't need to manually deal with time
    clock.schedule(self.run)


  # note this has been moved to a entity
  def drawCross(self, v):
    '''draw a cross at the position of a vector'''
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
    for entity in self.groups['updating']:
      entity.update(dt)

    # DRAW
    # TODO: camera
    for name in self.drawLayerNames:
      for entity in self.drawLayers[name]:  # TODO: batch drawing?
        entity.draw()

    if self.gameController: # if we have a controller
      glColor3f(0.0, 1.0, 0.0)
      self.drawCross(self.windowCenter + 100 * c.stick_l_raw)
      glColor3f(1.0, 1.0, 0.0)
      self.drawCross(self.windowCenter + 100 * c.stick_r_raw)

    glColor3f(1.0, 1.0, 1.0)
    self.drawCross(self.windowCenter)


  def addEntity(self, e):
    for group in e.groups:
      self.groups[group].add(e)
    if e.drawLayer is not None:
      self.drawLayers[e.drawLayer].append(e)

  def removeEntity(self, e):
    for group in e.groups:
      self.groups[group].remove(e)
    if e.drawLayer is not None:
      self.drawLayers[e.drawLayer].remove(e)
