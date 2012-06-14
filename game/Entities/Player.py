import pyglet.gl as gl
import pymunk
from pymunk import Vec2d
from math import degrees

from PhysicsEntity import PhysicsEntity
import game.globals as game

class Player(PhysicsEntity):

  size = Vec2d(10., 10.)
  speed = 100. # units per second
  jump_impulse = 3000.

  def __init__(self, playerInput, pos):
    super(Player, self).__init__()
    self.input = playerInput
    self.groups = self.groups | {'player'}
    self.drawLayer = 'player'
    self.body = pymunk.Body(self.mass, float('inf'))
    self.body.position = Vec2d(pos)
    self.pos = self.body.position
    self.vel = self.body.velocity

    # init shape
    self.collisionSquare = pymunk.Poly.create_box(self.body, 2*self.size)

    '''
    verticies = [
      (+s.x, +s.y),
      (+s.x, -s.y),
      (-s.x, -s.y),
      (-s.x, +s.y),
    ]
    '''

    # legs are the bottom of our shape
    s = self.size # just a shorthand
    v = 1.1 # a small vertical offset
    h = 3  # making the triangle thinner
    verticies = [
      (   0, 0),
      (+s.x - h, -s.y - v),
      (-s.x + h, -s.y - v),
    ]
    self.legs = pymunk.Poly(self.body, verticies)
    self.legs.friction = 1
    self.shapes = [self.collisionSquare, self.legs]


  def update(self, dt):
    self.input.checkInput()

    while self.input.actionQueue:
      action = self.input.actionQueue.pop(0)
      if action.type == 'move':
        # TODO make this safe. (check for positive/0/negative instead of taking value)
        self.legs.surface_velocity = Vec2d(action.moveDir * self.speed, 0)
      elif action.type == 'jump':
        self.vel.y = 0
        self.body.apply_impulse((0, self.jump_impulse))
      elif action.type == 'shoot':
        print "pew pew:", action.aim

  def draw(self):
    s = self.size # just a shorthand

    #this block does nothing, it's a template for when images come in
    gl.glPushMatrix()
    gl.glTranslatef(self.pos.x, self.pos.y, 0)
    gl.glRotatef(degrees(self.body.angle), 0, 0, 1)
    # blip image
    gl.glPopMatrix()

    # main collision square
    gl.glColor3f(1.0, 0.0, 0.0)
    gl.glBegin(gl.GL_POLYGON)
    for p in self.collisionSquare.get_points():
      gl.glVertex2f(p.x, p.y)
    gl.glEnd()

    # "feet" triangle
    gl.glColor3f(1.0, 0.0, 1.0)
    gl.glBegin(gl.GL_POLYGON)
    for p in self.legs.get_points():
      gl.glVertex2f(p.x, p.y)
    gl.glEnd()
