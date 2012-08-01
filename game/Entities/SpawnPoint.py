import pyglet.gl as gl
from pymunk import Vec2d

from game.Camera import shiftView
from Entity import GameEntity


class SpawnPoint(GameEntity):
  ''' A small class that only holds a spawn position for the player '''

  size = Vec2d(5, 5)

  def __init__(self, level, pos):
    self.level = level
    self.pos = Vec2d(pos)
    self.groups = {'game', 'all'}
    self.drawLayer = 'game'

  def reconstructionArgs(self):
    return [
      'SpawnPoint',
      tuple(self.pos),
    ]

  def draw(self):
    s = self.size # shorthand
    gl.glColor3f(0.7, 0.0, 0.0)
    with shiftView(self.pos):
      gl.glBegin(gl.GL_LINES)
      gl.glVertex2f(+s.x, +s.y)
      gl.glVertex2f(-s.x, -s.y)
      gl.glVertex2f(-s.x, +s.y)
      gl.glVertex2f(+s.x, -s.y)
      gl.glEnd()

  def changeSpawnLocation(self, state):
    if state:
      self.level.currentSpawn = self

  triggerables = dict(GameEntity.triggerables) # copy and extend
  triggerables['checkpoint'] = changeSpawnLocation  # the above method is triggerable
