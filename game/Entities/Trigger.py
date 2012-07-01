import pyglet.gl as gl
from pymunk import Vec2d, Poly

from Entity import PhysicsEntity

from game.Camera import shiftView

class Trigger(PhysicsEntity):
  drawLayer = 'game'

  def __init__(self, level, pos, size): # TODO: triggerable thing
    self.pos = Vec2d(pos)
    self.size = Vec2d(size)

    # physics from here on
    self.level = level
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

  def draw(self):
    s = self.size # just a shorthand
    gl.glColor3f(0.0, 0.0, 1.0)

    with shiftView(self.pos):
      gl.glBegin(gl.GL_LINE_LOOP)
      gl.glVertex2f(-s.x, +s.y)
      gl.glVertex2f(+s.x, +s.y)
      gl.glVertex2f(+s.x, -s.y)
      gl.glVertex2f(-s.x, -s.y)
      gl.glEnd()

  def __repr__(self):
    return repr((
      'Trigger',
      tuple(self.pos ),
      tuple(self.size),
      # TODO: triggerable thing
    ))
