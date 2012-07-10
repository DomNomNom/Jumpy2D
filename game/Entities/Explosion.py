import pyglet.gl as gl
from pymunk import Vec2d, Circle, Body

from Entity import PhysicsEntity

import game.globals as game
from game.Camera import shiftView

class Explosion(PhysicsEntity):

  radius = 20
  size = Vec2d(radius, 0) # size.x is our radius
  explosionImpact = 3000

  lifeSpan = 0.2 # in seconds

  def __init__(self, level, pos, player):
    self.level = level
    self.pos = Vec2d(pos)
    self.player = player
    self.startTime = game.engine.levelTime
    self.hasCollided = False


    self.body = Body(self.mass, self.moment)
    self.body.position = Vec2d(pos)
    self.body.apply_force(-self.mass*self.level.space.gravity) # make it not be affected by gravity
    self.shape = Circle(self.body, self.radius)
    self.shape.layers = self.collisionLayers
    self.shape.collision_type = self.collisionType
    self.shape.sensor = True
    self.shapes = [self.shape]

  def update(self, dt):
    lifeRatio = (game.engine.levelTime - self.startTime) / self.lifeSpan
    self.size = lifeRatio * Explosion.size
    if lifeRatio > 1:
      game.engine.removeEntity(self)  # Suicide D:


  def onPlayerCollide(self, player):
    if self.hasCollided: return
    self.hasCollided = True
    toPlayer = self.player.body.position - self.pos # the vector from our center to the player
    if toPlayer == Vec2d(0,0): # when in doubt, go upwards
      toPlayer = Vec2d(0,1)
    impulse = toPlayer.normalized() * self.explosionImpact # TODO: falloff curve
    self.player.body.apply_impulse(impulse)

  def draw(self):
    r = self.size.x
    gl.glColor3f(1.0, .7, 0.0)
    with shiftView(self.pos):
      gl.glBegin(gl.GL_LINE_LOOP)
      for angle in xrange(0, 360, 360/12):
        gl.glVertex2f(*self.size.rotated_degrees(angle))
      gl.glEnd()
