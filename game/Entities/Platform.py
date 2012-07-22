import pyglet.gl as gl
from pyglet.sprite import Sprite
from pymunk import Vec2d, Poly
from pymunk.util import is_clockwise

from Entity import PhysicsEntity

from game.Camera import shiftView
import game.globals as game # engine, resources


class Platform(PhysicsEntity):

  drawLayer = 'game'

  specialPolyTypes = {
    2 : gl.GL_LINES,
    3 : gl.GL_TRIANGLES,
    4 : gl.GL_QUADS,
  }

  def __init__(self, level, verticies, friction=0):

    self.level = level
    self.body = level.space.static_body

    assert len(verticies) >= 2
    verticies = self.verticies = map(Vec2d, verticies)
    if len(verticies) in self.specialPolyTypes:
      self.polyType = self.specialPolyTypes[len(verticies)]
    else:
      self.polyType = pg.GL_POLYGON
    #self.pos = sum(verticies) / len(verticies) # Average of verticies

    self.shape = Poly(self.body, verticies)
    self.shape.friction = friction

    # note: collisionLayers and collisionType get created by physics.py
    self.shape.layers = self.collisionLayers
    self.shape.collision_type = self.collisionType
    self.shapes = [self.shape]


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


  def __repr__(self):
    return ', '.join(map(repr, [
      'Platform',
      map(tuple, self.verticies),
      self.shape.friction,
    ]))
