import pyglet.gl as gl
from pymunk import Vec2d

from Entity import GameEntity

import game.globals as game

class Explosion(GameEntity):

  radius = 20
  size = Vec2d(radius, 0) # size.x is our radius
  explosionImpact = 3000

  lifeSpan = 0.2 # in seconds

  def __init__(self, pos, player):
    self.pos = Vec2d(pos)
    self.player = player
    self.startTime = game.engine.levelTime
    self.hasCollided = False

  def update(self, dt):
    lifeRatio = (game.engine.levelTime - self.startTime) / self.lifeSpan
    self.size = lifeRatio * Explosion.size
    if lifeRatio > 1:
      game.engine.removeEntity(self)  # Suicide D:

    # do the collision with player
    if self.hasCollided: return
    toPlayer = self.player.body.position - self.pos # the vector from our center to the player
    if toPlayer.length < self.radius:
      self.hasCollided = True
      if toPlayer == Vec2d(0,0): # when in doubt, go upwards
        toPlayer = Vec2d(0,1)
      impulse = toPlayer.normalized() * self.explosionImpact # TODO: falloff curve
      self.player.body.apply_impulse(impulse)

  def draw(self):
    r = self.size.x
    gl.glColor3f(1.0, .7, 0.0)
    with game.engine.camera.shiftView(self.pos):
      gl.glBegin(gl.GL_LINE_LOOP)
      for angle in xrange(0, 360, 360/12):
        gl.glVertex2f(*self.size.rotated_degrees(angle))
      gl.glEnd()
