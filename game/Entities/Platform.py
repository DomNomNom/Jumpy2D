import pyglet.gl as gl
from pymunk import Vec2d
from itertools import chain

from Entity import PhysicsEntity

from game.Camera import shiftView
import game.globals as game # engine, resources
from game.DrawingGroups import TextureBindGroup


class Platform(PhysicsEntity):

  drawLayer = 'game'


  def __init__(self, level, verticies, friction=0):
    self.level = level
    self.body = level.space.static_body
    self.createShape(verticies)
    self.shape.friction = friction
    
    #self.colour = (0.0, 1.0, int(self.shape.friction==0)/3.) # make it a slightly different colour when frictionless
    self.colour = (1,1,1)

    self.texture = game.resources.textures['platform']
    texScale = 1/Vec2d(self.texture.width, self.texture.height)
    texCoords = [xy*texScale for xy in self.verticies]

    self.vertexList = game.engine.drawLayersBatch[self.drawLayer].add(
      len(self.verticies),
      self.polyType,
      TextureBindGroup(self.texture), # group
      ('v2f/static', list(chain(*self.verticies))),      # verticies
      ('t2f/static', list(chain(*texCoords     ))),      # texture coordinates
      ('c3f/static', self.colour * len(self.verticies)), # colour for each vertex (all the same)
    )


  def draw(self):
    pass # we are using a vertex list

  def reconstructionArgs(self):
    return [
      'Platform',
      map(tuple, self.verticies), # verticies
      self.shape.friction,        # friction
    ]
