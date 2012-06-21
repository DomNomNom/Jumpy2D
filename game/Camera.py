import pyglet.gl as gl
from pymunk import Vec2d

from random import randint

class Camera(object):

  def __init__(self):
    self.pos = Vec2d(0,0)
    self.angle = 0 # in degrees

  def shiftView(self, pos=None):
    if pos is None:
      pos = self.pos
    pos = Vec2d(randint(-5,5), randint(-2,2))
    shift = self.ViewShift(pos)
    return shift

  # This class defines a "with" statement
  class ViewShift(object):
    def __init__(self, pos):
      self.pos = pos
    def __enter__(self):
      gl.glPushMatrix()
      gl.glTranslatef(self.pos.x, self.pos.y, 0)
      #gl.glRotatef(self.angle, 0, 0, 1)
    def __exit__(self, type, value, traceback):
      gl.glPopMatrix()
