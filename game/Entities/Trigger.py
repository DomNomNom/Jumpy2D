import pyglet.gl as gl
from pymunk import Vec2d, Poly

from Entity import PhysicsEntity

from game.Camera import shiftView

import game.globals as game


class Trigger(PhysicsEntity):
  drawLayer = 'game'

  def __init__(self, level, pos, size, thingsToTrigger={}, startState=False):
    self.level = level
    self.pos = Vec2d(pos)
    self.size = Vec2d(size)

    self.thingsToTrigger=thingsToTrigger # TODO

    # physics from here on
    self.body = level.space.static_body

    s = self.size # just a shorthand
    p = self.pos
    self.shape = Poly(self.body, (
      (p.x+s.x, p.y+s.y),
      (p.x+s.x, p.y-s.y),
      (p.x-s.x, p.y-s.y),
      (p.x-s.x, p.y+s.y),
    ))

    # note: collisionLayers and collisionType get created by physics.py
    self.shape.layers = self.collisionLayers
    self.shape.collision_type = self.collisionType
    self.shape.sensor = True
    self.shapes = [self.shape]

    self.triggered(startState)


  def draw(self, colour=(0., 0., 1.)):
    s = self.size # just a shorthand
    gl.glColor3f(*colour)

    with shiftView(self.pos):
      gl.glBegin(gl.GL_LINE_LOOP)
      gl.glVertex2f(-s.x, +s.y)
      gl.glVertex2f(+s.x, +s.y)
      gl.glVertex2f(+s.x, -s.y)
      gl.glVertex2f(-s.x, -s.y)
      gl.glEnd()

  def triggered(self, state):
    self.state = state
    for entityID, methodName in self.thingsToTrigger.items():
      entity = self.level.ids[entityID]
      method = entity.triggerables[methodName]
      method(entity, state)
    if state == True:
      print 'state ON'
    else:
      print 'state OFF'

  def __repr__(self, className='Trigger'):
    return repr((
      className,
      tuple(self.pos ),
      tuple(self.size),
    ))



class LevelEnd(Trigger):
  def triggered(self, state):
    if state == True:
      game.gameState.popState()

  def __repr__(self):
    return Trigger.__repr__(self, 'LevelEnd')
