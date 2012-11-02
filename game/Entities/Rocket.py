import pyglet.gl as gl
import pymunk
from pymunk import Vec2d

from Entity import PhysicsEntity
from Explosion import Explosion, ExplosionDerbis
import game.globals as game


class Rocket(PhysicsEntity):

  size = Vec2d(9, 4)
  speed = 500. # units per second

  def __init__(self, level, pos, angle, player):
    self.level = level
    self.groups = self.groups | {'rockets'}
    self.body = pymunk.Body(self.mass, self.moment)
    self.body.position = Vec2d(pos)
    self.body.angle = angle
    self.body.velocity = Vec2d(self.speed, 0).rotated(angle)
    self.body.apply_force(-self.mass*self.level.space.gravity) # make it not be affected by gravity

    self.shape = pymunk.Segment(
      self.body,
      Vec2d(-self.size.x, 0),
      Vec2d( self.size.x, 0),
      0 # the collision model is acutally 0-thin
    )
    # note: collisionLayers and collisionType get created by physics.py
    self.shape.layers = self.collisionLayers
    self.shape.collision_type = self.collisionType
    self.shapes = [self.shape]
    self.shape.sensor = True

    self.player = player

  def draw(self):
    gl.glColor3f(1.0, 1.0, 0.0)
    gl.glBegin(gl.GL_LINES)
    gl.glVertex2f(*self.body.local_to_world(self.shape.a))
    gl.glVertex2f(*self.body.local_to_world(self.shape.b))
    gl.glEnd()

  def explode(self):
    game.engine.addEntity(Explosion(self.level, self.body.position, self.player))
    for i in xrange(10):
      game.engine.addEntity(
        ExplosionDerbis(self.level, self.body.position, self.player)
      )
