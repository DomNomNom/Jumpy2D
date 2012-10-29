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
    
    self.colour = (0.0, 1.0, int(self.shape.friction==0)/3.) # make it a slightly different colour when frictionless
    self.colour = (1,1,1)

    self.texture = game.resources.textures['platform']
    texCoords = self.size / (self.texture.width, self.texture.height)
    texCoords = Vec2d(texCoords.y, texCoords.x) # i don't even know why
    print "ratio", texCoords

    self.vertexList = game.engine.drawLayersBatch[self.drawLayer].add(
      len(self.verticies), 
      self.polyType, 
      TextureBindGroup(self.texture), # group
      ('v2f/static', tuple(chain(*self.verticies))),    # verticies
      ('t2f/static', (0,0,  texCoords.x,0,  texCoords.x,texCoords.y,  0,texCoords.y)),
      ('c3f/static', self.colour * len(self.verticies)), # colour for each vertex
    )


  def draw(self):
    pass
    '''
    s = self.size # just a shorthand
    gl.glColor3f(*self.colour)
    gl.glBegin(self.polyType)
    for vertex in self.verticies:
      gl.glVertex2f(*vertex)
    gl.glEnd()
    '''
    
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
