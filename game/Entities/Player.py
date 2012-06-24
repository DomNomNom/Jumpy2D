import pyglet.gl as gl
import pymunk
from pymunk import Vec2d
from math import degrees

from Entity import PhysicsEntity
from Rocket import Rocket
import game.globals as game

class Player(PhysicsEntity):

  size = Vec2d(10, 10)
  speed = 200. # units per second
  jump_impulse = 3000.

  def __init__(self, playerInput, pos):
    PhysicsEntity.__init__(self)
    self.input = playerInput
    self.groups = self.groups | {'player'}
    self.drawLayer = 'player'
    self.body = pymunk.Body(self.mass, float('inf'))
    self.body.position = Vec2d(pos)
    self.targetVel = Vec2d(0, 0) # target velocity
    self.pos = self.body.position
    self.vel = self.body.velocity

    # init shape
    self.collisionSquare = pymunk.Poly.create_box(self.body, 2*self.size)
    # note: collisionLayers and collisionType get created by physics.py
    self.collisionSquare.friction = 1
    self.collisionSquare.layers = self.collisionLayers
    self.collisionSquare.collision_type = self.collisionType
    self.shapes = [self.collisionSquare]


  def update(self, dt):
    self.input.checkInput()

    while self.input.actionQueue:
      action = self.input.actionQueue.pop(0)
      if action.type == 'move':
        if action.moveDir == 0:
          self.targetVel.x = 0
        else:
          self.targetVel.x = self.speed * (action.moveDir/abs(action.moveDir))
        self.collisionSquare.surface_velocity = Vec2d(self.targetVel.x, 0)
      elif action.type == 'jump':
        self.vel.y = 0
        self.body.apply_impulse((0, self.jump_impulse))
      elif action.type == 'shoot':
        game.engine.addEntity(Rocket(self.pos, action.aim, self))

    # movement Control
    # increase our velocity iff our target velocity is 'faster'
    # (faster is in quotes as going the opposite direction means 'faster')
    # a target velocity of 0 will not change the velocity.
    vel = self.targetVel.x # shorhand
    if (
      (vel < 0 and vel < self.body.velocity.x) or
      (vel > 0 and vel > self.body.velocity.x)
    ): # and here's a happy face to make up for it:  :)
      self.body.apply_impulse((self.targetVel.x - self.body.velocity.x, 0))


  def draw(self):

    # main collision square
    gl.glColor3f(1.0, 0.0, 0.0)
    gl.glBegin(gl.GL_QUADS)
    for point in self.collisionSquare.get_points():
      gl.glVertex2f(*point)
    gl.glEnd()


    #this push/pop block is for player-relative coordinates
    gl.glPushMatrix()
    gl.glTranslatef(self.pos.x, self.pos.y, 0)
    gl.glRotatef(degrees(self.body.angle), 0, 0, 1)
    gl.glColor3f(1.0, 0.0, 1.0)
    gl.glBegin(gl.GL_LINES)
    gl.glVertex2f(0,0)
    gl.glVertex2f(*Vec2d(30, 0).rotated(self.input.currentAim))
    gl.glEnd()
    gl.glPopMatrix()
