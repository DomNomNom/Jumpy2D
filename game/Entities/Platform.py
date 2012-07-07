import pyglet.gl as gl
from pymunk import Vec2d, Poly
from pymunk.util import is_clockwise

from Entity import PhysicsEntity

from game.Camera import shiftView
import game.globals as game # engine, resources


class Platform(PhysicsEntity):

  def __init__(self, level, pos, size, friction=0):
    self.drawLayer = 'game'
    self.pos = Vec2d(pos)
    self.size = Vec2d(size)

    # physics from here on
    self.level = level
    self.body = level.space.static_body

    s = self.size # just a shorthand
    p = self.pos
    self.shape = Poly(self.body, (
      (p.x+s.x, p.y+s.y),
      (p.x+s.x, p.y-s.y),
      (p.x-s.x, p.y-s.y),
      (p.x-s.x, p.y+s.y),
    ))
    self.shape.friction = friction

    # note: collisionLayers and collisionType get created by physics.py
    self.shape.layers = self.collisionLayers
    self.shape.collision_type = self.collisionType
    self.shapes = [self.shape]


  def draw(self):
    s = self.size # just a shorthand
    gl.glColor3f(0.0, 1.0, int(self.shape.friction==0)/3.) # make it a slightly different colour when frictionless

    '''
    gl.glPushMatrix()
    gl.glTranslatef(self.pos.x, self.pos.y, 0)
    gl.glBegin(gl.GL_QUADS)
    gl.glVertex2f(-s.x, +s.y)
    gl.glVertex2f(+s.x, +s.y)
    gl.glVertex2f(+s.x, -s.y)
    gl.glVertex2f(-s.x, -s.y)
    gl.glEnd()
    gl.glPopMatrix()
    '''

    with shiftView(self.pos - self.size):
      tex = game.resources.textures['platform']
      tex.blit_tiled(0,0, 0, *(self.size*2))



  def __repr__(self):
    return repr((
      'Platform',
      tuple(self.pos ),
      tuple(self.size),
      self.shape.friction,
    ))






class TrianglePlatform(Platform):
  def __init__(self, level, a,b,c, friction=0): # a,b,c are our corners
    a,b,c = map(Vec2d, (a,b,c)) # convert a,b,c to vectors
    self.a = a
    self.b = b
    self.c = c
    self.level = level
    self.body = level.space.static_body
    self.shape = Poly(self.body, (a, b, c))
    self.shape.friction = friction
    self.shape.layers = self.collisionLayers
    self.shape.collision_type = self.collisionType
    self.shapes = [self.shape]

  def __repr__(self):
    return repr((
      'TrianglePlatform',
      tuple(self.a),
      tuple(self.b),
      tuple(self.c),
      self.shape.friction,
    ))

  def draw(self):
    gl.glColor3f(0.0, 1.0, int(self.shape.friction==0)/3.)
    gl.glPushMatrix()
    gl.glTranslatef(self.pos.x, self.pos.y, 0)
    gl.glBegin(gl.GL_TRIANGLES)
    gl.glVertex2f(*self.a)
    gl.glVertex2f(*self.b)
    gl.glVertex2f(*self.c)
    gl.glEnd()
    gl.glPopMatrix()
