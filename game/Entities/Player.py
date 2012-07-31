import pyglet.gl as gl
import pymunk
from pymunk import Vec2d
from math import degrees

from Entity import PhysicsEntity
from Rocket import Rocket
from game.Camera import shiftView
import game.globals as game

class Player(PhysicsEntity):

  size = Vec2d(10, 0)
  drawLayer = 'player'
  speed = 200. # units per second
  jump_impulse = 2500.

  slopeRanges = {
    # ground range (0 <= )
    'wall' : 45 +1,
    # wall range
    'ceiling'  :  45*3 +1,
    # ceiling range (<= 180)
  }

  def __init__(self, level, playerInput, pos):
    PhysicsEntity.__init__(self)
    self.input = playerInput
    self.groups = self.groups | {'player'}
    self.targetVel = Vec2d(0, 0) # target velocity
    self.body = pymunk.Body(self.mass, float('inf'))
    self.body.position = Vec2d(pos)
    self.level = level
    self.isTouchingGround = False
    self.isTouchingWall = False
    self.isTouchingCeiling = False

    # init shape
    self.collisionSquare = pymunk.Circle(self.body, self.size.x)
    # note: collisionLayers and collisionType get created by physics.py
    self.collisionSquare.friction = 1
    self.collisionSquare.layers = self.collisionLayers
    self.collisionSquare.collision_type = self.collisionType
    self.shapes = [self.collisionSquare]

  # pos/vel now return the our physics-bodys properties
  @property
  def pos(self): return self.body.position
  @property
  def vel(self): return self.body.velocity


  # this shoulbe be called by physics.py when a player-platform collision has taken place
  # this method decides whether the player is allowed to jump (which is only when standing on a platform)
  def platformCollision(self, arbiter):
    # steepness is a angle between 0-180 degrees saying with what we collided
    # note: 0 == ground < slope < wall < ceiling == 180
    steepness = abs(arbiter.total_impulse.rotated_degrees(-90).angle_degrees)
    #print steepness
    if steepness < self.slopeRanges['wall']:
      self.isTouchingGround = True
    elif steepness < self.slopeRanges['ceiling']:
      self.isTouchingWall = True
    else:
      self.isTouchingCeiling = True

  # kills the player; respawning him at the closest checkpoint
  def die(self, state):
    if state:
      self.respawn()
  triggerables = dict(PhysicsEntity.triggerables) # copy and extend
  triggerables['die'] = die  # the above method is triggerable

  def respawn(self):
    self.body.position = self.level.currentSpawn.pos
    self.body.velocity =  Vec2d(0, 0)

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
        if self.isTouchingGround:
          self.vel.y = 0
          self.body.apply_impulse((0, self.jump_impulse))
      elif action.type == 'shoot':
        game.engine.addEntity(Rocket(self.level, self.pos, action.aim, self))


    # movement Control
    # increase our velocity if our target velocity is 'faster'
    # (faster is in quotes as going the opposite direction means 'faster')
    # a target velocity of 0 will not change the velocity.
    vel = self.targetVel.x # shorthand
    if (
      (vel < 0 and vel < self.body.velocity.x) or
      (vel > 0 and vel > self.body.velocity.x)
    ): # and here's a happy face to make up for it:  :)
      self.body.apply_impulse((self.targetVel.x - self.body.velocity.x, 0))

    self.isTouchingGround = False
    self.isTouchingWall = False
    self.isTouchingCeiling = False

  def draw(self):
    with shiftView(self.pos):
      gl.glColor3f(1.0, 0.0, 0.0)
      gl.glBegin(gl.GL_TRIANGLE_FAN)
      gl.glVertex2f(0, 0)
      for i in xrange(0, 365, 5):
        gl.glVertex2f(*self.size.rotated_degrees(i))
      gl.glEnd()

      gl.glRotatef(degrees(self.body.angle), 0, 0, 1)
      gl.glColor3f(1.0, 0.0, 1.0)
      gl.glBegin(gl.GL_LINES)
      gl.glVertex2f(0,0)
      gl.glVertex2f(*Vec2d(30, 0).rotated(self.input.currentAim))
      gl.glEnd()
