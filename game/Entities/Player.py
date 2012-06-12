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

  def __init__(self, playerInput):
    super(Player, self).__init__()
    self.input = playerInput
    self.groups = self.groups | {'player'}
    self.drawLayer = 'player'
    self.body = pymunk.Body(self.mass, float('inf'))
    self.body.position = Vec2d(game.engine.windowCenter)
    self.pos = self.body.position
    self.vel = self.body.velocity
#    self.shape = pymunk.Poly.create_box(self.body)

    s = self.size # just a shorthand
    verticies = [
      (+s.x, +s.y),
      (+s.x, -s.y),
      (-s.x, -s.y),
      (-s.x, +s.y),
    ]
    self.shape = pymunk.Poly(self.body, verticies)
    self.shape.friction = 1


  def update(self, dt):
    self.input.checkInput()

    while self.input.actionQueue:
      action = self.input.actionQueue.pop(0)
      if action.type == 'move':
        # TODO make this safe. (check for positive/0/negative instead of taking value)
        self.shape.surface_velocity = Vec2d(action.moveDir * self.speed, 0)
      elif action.type == 'jump':
        self.vel.y = 0
        self.body.apply_impulse((0, self.jump_impulse))
      elif action.type == 'shoot':
        print "pew pew!", "trajectory:", action.aim

  def draw(self):
    s = self.size # just a shorthand
    gl.glColor3f(1.0, 0.0, 0.0)

    gl.glPushMatrix()
    gl.glTranslatef(self.pos.x, self.pos.y, 0)
    gl.glRotatef(degrees(self.body.angle), 0, 0, 1)
    gl.glBegin(gl.GL_QUADS)
    gl.glVertex2f(-s.x, +s.y)
    gl.glVertex2f(+s.x, +s.y)
    gl.glVertex2f(+s.x, -s.y)
    gl.glVertex2f(-s.x, -s.y)
    gl.glEnd()
    gl.glPopMatrix()
