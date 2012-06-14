import pyglet.gl as gl
from pymunk.vec2d import Vec2d
import pymunk

from PhysicsEntity import PhysicsEntity
import game.globals as game

class Platform(PhysicsEntity):

  def __init__(self, pos, size=Vec2d(100, 100)):
    self.drawLayer = 'game'
    self.pos = Vec2d(pos)
    self.size = Vec2d(size)

    # physics
    super(Platform, self).__init__()
    self.body = game.engine.space.static_body
    s = self.size # just a shorthand
    p = self.pos
    verticies = [
      (p.x+s.x, p.y+s.y),
      (p.x+s.x, p.y-s.y),
      (p.x-s.x, p.y-s.y),
      (p.x-s.x, p.y+s.y),
    ]
    self.shapes = [pymunk.Poly(self.body, verticies)]
    self.shapes[0].friction = 1

  def __repr__(self):
    # return comma separated
    return repr([
      'Platform',
      tuple(self.pos ),
      tuple(self.size),
    ])

  def draw(self):
    s = self.size # just a shorthand
    gl.glColor3f(0.0, 1.0, 0.0)

    gl.glPushMatrix()
    gl.glTranslatef(self.pos.x, self.pos.y, 0)
    gl.glBegin(gl.GL_QUADS)
    gl.glVertex2f(-s.x, +s.y)
    gl.glVertex2f(+s.x, +s.y)
    gl.glVertex2f(+s.x, -s.y)
    gl.glVertex2f(-s.x, -s.y)
    gl.glEnd()
    gl.glPopMatrix()
