import pyglet.gl as gl
from pymunk.vec2d import Vec2d
import pymunk

from PhysicsEntity import PhysicsEntity

# things we collide with
from Rocket import Rocket
from Player import Player

import game.globals as game # engine


class Platform(PhysicsEntity):

  collisionLayer = 2**0

  def __init__(self, pos, size=Vec2d(100, 100), friction=0):
    self.drawLayer = 'game'
    self.pos = Vec2d(pos)
    self.size = Vec2d(size)

    # physics
    PhysicsEntity.__init__(self)  
    self.body = game.engine.space.static_body

    # physics shape
    s = self.size # just a shorthand
    p = self.pos
    self.shape = pymunk.Poly(self.body, (
      (p.x+s.x, p.y+s.y),
      (p.x+s.x, p.y-s.y),
      (p.x-s.x, p.y-s.y),
      (p.x-s.x, p.y+s.y),
    ))
    self.shape.friction = friction
    self.shape.layers = Player.collisionLayer + Rocket.collisionLayer
    self.shapes = [self.shape]


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



  def __repr__(self):
    return repr([
      'Platform',
      tuple(self.pos ),
      tuple(self.size),
      self.shape.friction,
    ])
