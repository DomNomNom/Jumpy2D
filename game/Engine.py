from pyglet.gl import *
from pyglet import clock
from pymunk import Vec2d
import time

from Camera import Camera


class Engine:

  # dictionary from group to list of Entities. they are NOT mutually exclusive
  # don't manually add to this directly! use addEntity/removeEntity.
  groups = {
    'all':      set(), # all entities should be in here
    'updating': set(), # everything that wants to be updated goes in here
    'level':    set(),
    'player':   set(),
    'physics':  set(),
    'rockets':  set(),
    'game':     set(), # will draw dependent   on camera movement
    'UI':       set(), # will draw independent of camera movement
    'UI_editor': set(), # entites that are part of the editor UI
  }

  entityAddQueue = set()
  entityDelQueue = set()

  # layers specify the order in which they are drawn. (ordered back to front)
  drawLayerNames = [
    'background',
    'game',
    'player',
    # UI ones from here on
    'UI_editor',
    'UI_pauseMenu',
    'UI_debug',
  ]

  # A dict from drawLayerNames to a list of entities. they are mutually exclusive
  drawLayers = {}
  drawLayersBatch = {} #a dict from drawLayerNames to a list of batches

  levelStartTime = time.time()
  levelTime = 0. # TODO proper pausing (maybe move to gameState or some level class)

  accumulatedFrameTime = 0.
  updateRate = 1/120. # how often our physics will kick in (in seconds)

  window = None
  windowCenter = Vec2d()
  mousePos = Vec2d()

  shapeToEntity = {} # a dict that gives the entity that contains the keyed shape


  def __init__(self):
    # init draw layers
    for name in self.drawLayerNames:
      self.drawLayers[name] = set()
      self.drawLayersBatch[name] = pyglet.graphics.Batch()

    # Window
    config = pyglet.gl.Config(
      #sample_buffers=1, samples=4   # antialiasing
    )
    self.window = pyglet.window.Window(
      config = config,
      #fullscreen = True,
      vsync = False,
      style = pyglet.window.Window.WINDOW_STYLE_BORDERLESS,
    )
    self.windowCenter = Vec2d(self.window.get_size()) / 2

    # opengl
    gl.glEnable(GL_BLEND) #enables transparency

    # camera
    self.camera = Camera()

    @self.window.event
    def on_mouse_motion(x, y, dx, dy):
      self.mousePos.x = x
      self.mousePos.y = y
    @self.window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
      self.mousePos.x = x
      self.mousePos.y = y

    self.fps_display = pyglet.clock.ClockDisplay()

    # shedule our main loop so we don't need to manually deal with time
    clock.schedule(self.run)


  # our main game loop
  def run(self, dt):
    ## UPDATE ##
    # timestep ala http://gafferongames.com/game-physics/fix-your-timestep/
    if dt > .25: # avoid spiral of death (updating taking longer than framerate)
      dt = .25
    self.accumulatedFrameTime += dt
    while self.accumulatedFrameTime >= self.updateRate:
      self.accumulatedFrameTime -= self.updateRate
      self.levelTime = time.time() - self.levelStartTime
      for entity in self.groups['updating']:
        entity.update(self.updateRate) # update all entities
      self._processRemoving()
      self._processAdding()
      for level in self.groups['level']:
        level.space.step(self.updateRate) # update physics

    ## DRAW ##
    glClearColor(0,0,0, 0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    #self.camera.gameFocus = (self.windowCenter - self.mousePos) / 2
    for name in self.drawLayerNames:
      shift = Vec2d() if name.startswith('UI') else None
      with self.camera.shiftView(shift):
        for entity in self.drawLayers[name]:  # TODO: batch drawing?
          entity.draw()
        self.drawLayersBatch[name].draw()

    self.fps_display.draw()
    #self.window.flip()



  def addEntity(self, e):
    self.entityAddQueue.add(e)

  def removeEntity(self, e):
    self.entityDelQueue.add(e)


  def _processAdding(self):
    while len(self.entityAddQueue):
      e = self.entityAddQueue.pop()
      assert 'all' in e.groups
      for group in e.groups:
        self.groups[group].add(e)
      if 'physics' in e.groups:
        e.level.space.add(e.shapes)
        for shape in e.shapes:
          self.shapeToEntity[shape] = e
        if e.body is not e.level.space.static_body:
          e.level.space.add(e.body)
      if e.drawLayer is not None:
        self.drawLayers[e.drawLayer].add(e)

  def _processRemoving(self):
    while len(self.entityDelQueue):
      e = self.entityDelQueue.pop()
      assert 'all' in e.groups
      for group in e.groups:
        if e in self.groups[group]:
          self.groups[group].remove(e)
      if 'physics' in e.groups:
        e.level.space.remove(e.shapes)
        for shape in e.shapes:
          del self.shapeToEntity[shape]
        if e.body is not e.level.space.static_body:
          e.level.space.remove(e.body)
      if e.drawLayer is not None:
        self.drawLayers[e.drawLayer].remove(e)
