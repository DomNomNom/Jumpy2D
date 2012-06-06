import pyglet.gl as gl

from PhysicsEntity import PhysicsEntity
from game.Vector import Vector
import game.globals

class Player(PhysicsEntity):

  size = Vector(10., 10.)
  speed = 100 # units per second

  def __init__(self, playerInput):
    super(Player, self).__init__()
    self.input = playerInput
    self.groups.add('player')
    self.drawLayer = 'player'


  def update(self, dt):
    self.input.checkInput()

    while self.input.actionQueue:
      action = self.input.actionQueue.pop(0)
      if action.type == 'move':
        self.vel.x = action.moveDir * self.speed # TODO make this safe. (check for positive/0/negative instead of taking value)

    self.move(dt)

  def draw(self):
    s = self.size # just a shorthand
    gl.glColor3f(1.0, 0.0, 0.0)

    gl.glPushMatrix()
    gl.glTranslatef(self.pos.x, self.pos.y, 0)
    gl.glBegin(gl.GL_QUADS)
    gl.glVertex2f(-s.x, +s.y)
    gl.glVertex2f(+s.x, +s.y)
    gl.glVertex2f(+s.x, -s.y)
    gl.glVertex2f(-s.x, -s.y)
    gl.glEnd()
    gl.glPopMatrix()
