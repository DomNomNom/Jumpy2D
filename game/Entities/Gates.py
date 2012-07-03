import pyglet.gl as gl
from pymunk import Vec2d

from Entity import GameEntity

from game.Camera import shiftView

class NotGate(GameEntity):
  size = Vec2d(20, 20)
  groups = {'all', 'updating', 'game'}

  def __init__(self, level, pos, thingsToTrigger={}, startState=False):
    self.level = level
    self.pos = Vec2d(pos)
    self.thingsToTrigger = thingsToTrigger
    self.triggered(not startState)

  def draw(self, colour=(0., 0., 1.)):
    s = self.size # shorthand
    gl.glColor3f(*colour)
    with shiftView(self.pos):
      gl.glBegin(gl.GL_LINE_LOOP)
      gl.glVertex2f(-s.x, +s.y)
      gl.glVertex2f(+s.x, +s.y)
      gl.glVertex2f(+s.x, -s.y)
      gl.glVertex2f(-s.x, -s.y)
      gl.glEnd()

  def __repr__(self, className='NotGate'):
    return repr((
      className,
      tuple(self.size),
      thingsToTrigger,
    ))

  def triggered(self, state):
    state = not state
    self.state = state
    for entityID, methodName in self.thingsToTrigger.items():
      entity = self.level.ids[entityID]
      method = entity.triggerables[methodName]
      method(entity, state)

  triggerables = {'in' : triggered}

