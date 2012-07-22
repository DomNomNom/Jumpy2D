import pyglet.gl as gl
from pyglet.sprite import Sprite
from pymunk import Vec2d
from pymunk.util import is_clockwise

from Entity import PhysicsEntity

from game.Camera import shiftView
import game.globals as game # engine, resources


class Platform(PhysicsEntity):

  drawLayer = 'game'

  

  def __init__(self, level, verticies, friction=0):

    self.level = level
    self.body = level.space.static_body

    self.createShape(verticies)
    self.shape.friction = friction


  def draw(self):
    s = self.size # just a shorthand
    gl.glColor3f(0.0, 1.0, int(self.shape.friction==0)/3.) # make it a slightly different colour when frictionless

    # TODO: batch
    gl.glBegin(self.polyType)
    for vertex in self.verticies:
      gl.glVertex2f(*vertex)
    gl.glEnd()

    # TODO: textures
    '''
    with shiftView(self.pos - self.size):
      tex = game.resources.textures['platform']
      Sprite(tex)
      tex.blit_tiled(0,0, 0, *(self.size*2))
    '''

  def reconstructionArgs(self):
    return [
      'Platform',
      map(tuple, self.verticies), # verticies
      self.shape.friction,        # friction
    ]
