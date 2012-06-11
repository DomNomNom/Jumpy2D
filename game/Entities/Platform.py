import pyglet.gl as gl
from pymunk.vec2d import Vec2d
import pymunk

from PhysicsEntity import PhysicsEntity
import game.globals as game

class Platform(PhysicsEntity):

  size = Vec2d(100., 100.)
  speed = 100 # units per second

  def __init__(self):
    self.drawLayer = 'game'
    self.pos = Vec2d(game.engine.windowCenter.tuple())
    self.pos.y -= 150

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
    self.shape = pymunk.Poly(pymunk.Body(), verticies)
    self.shape.friction = 0.5


  def update(self, dt):
    pass #self.vel.y = 0

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
