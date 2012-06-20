import pyglet.gl as gl
import pymunk
from pymunk import Vec2d

from PhysicsEntity import PhysicsEntity
import game.globals as game


class Rocket(PhysicsEntity):

  collisionLayer = 2**2
  collisionType = 3

  size = Vec2d(10, 4)
  speed = 300. # units per second

  def __init__(self, pos, angle):
    self.groups = self.groups | {'rockets'}
    PhysicsEntity.__init__(self)
    self.body = pymunk.Body(self.mass, self.moment)
    self.body.position = Vec2d(pos)
    self.body.angle = angle
    self.body.velocity = Vec2d(self.speed, 0).rotated(angle)
    self.body.apply_force(-self.mass*game.engine.space.gravity) # make it not be affected by gravity
    
    self.shape = pymunk.Poly.create_box(self.body, 2*self.size)
    self.shape.layers = self.collisionLayer
    self.shape.collision_type = self.collisionType
    self.shapes = [self.shape]
    #self.shape.sensor = True #TODO: sensing

  def draw(self):
    # main collision square
    gl.glColor3f(1.0, 1.0, 0.0)
    gl.glBegin(gl.GL_QUADS)
    for point in self.shape.get_points():
      gl.glVertex2f(*point)
    gl.glEnd()
