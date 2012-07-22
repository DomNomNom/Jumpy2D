import pyglet.gl as gl
from pymunk import Vec2d, Poly

from Entity import PhysicsEntity

from game.Camera import shiftView

import game.globals as game


class Trigger(PhysicsEntity):
  drawLayer = 'game'
  triggerables = {}

  def __init__(self, level, verticies, thingsToTrigger={}, startState=False):
    self.level = level
    self.pos = Vec2d(pos)
    self.size = Vec2d(size)

    self.thingsToTrigger = thingsToTrigger

    self.createBody(verticies)

    self.shape.sensor = True
    self.triggered(startState)


  def draw(self, colour=(0., 0., 1.)):
    s = self.size # just a shorthand
    gl.glColor3f(*colour)
    gl.glBegin(gl.GL_LINE_LOOP)
    for vertex in self.verticies:
      gl.glVertex2f(*vertex)
    gl.glEnd()

  def triggered(self, state):
    self.state = state
    for entityID, methodName in self.thingsToTrigger.items():
      entity = self.level.ids[entityID]
      method = entity.triggerables[methodName]
      method(entity, state)

  def reconstructionArgs(self):
    return [
      'Platform',
      map(tuple, self.verticies), # verticies
      thingsToTrigger
    ]



class LevelEnd(Trigger):
  def triggered(self, state):
    if state == True:
      game.gameState.popState()

  def reconstructionArgs(self):
    return [
      'LevelEnd',
      map(tuple, self.verticies), # verticies
      thingsToTrigger
    ]
