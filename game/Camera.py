import pyglet.gl as gl
from pymunk import Vec2d

from matrixMath import inverse

class Camera(object):

  def __init__(self):
    self.gameFocus = Vec2d(0,0)
    self.angle = 0 # in degrees

  def shiftView(self, pos=None):
    if pos is None:
      pos = self.gameFocus
    shift = self.ViewShift(pos)
    return shift

  # This class defines a "with" statement
  class ViewShift(object):
    def __init__(self, pos):
      self.pos = pos
    def __enter__(self):
      gl.glPushMatrix()
      gl.glTranslatef(self.pos.x, self.pos.y, 0.)
      #gl.glScalef(.5,.5,1)
      #gl.glRotatef(10, 0, 0, 1)
    def __exit__(self, type, value, traceback):
      gl.glPopMatrix()


  def toModelView(self, v):
    """ Returns a point that had the current camera translation applied to it """
    p = Vec2d(v)
    a = (gl.GLfloat * 16)() # our transformation matrix
    gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX, a)
    return Vec2d(
      # matrix multiplication with z ignored
      # see: http://stackoverflow.com/questions/9328992/opengl-transformations
      p.x*a[0] + p.y*a[4] + 0*a[8] + 1*a[12],
      p.x*a[1] + p.y*a[5] + 0*a[9] + 1*a[13],
    )

  def toScreenView(self, v):
    """ Returns a point at screenspace that would give v after camera translation """
    p = Vec2d(v)
    a = (gl.GLfloat * 16)() # our transformation matrix
    gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX, a)
    i = inverse([ # our inverse matrix
      [a[0], a[4], a[ 8], a[12]],
      [a[1], a[5], a[ 9], a[13]],
      [a[2], a[6], a[10], a[14]],
      [a[3], a[7], a[11], a[15]],
    ])
    return Vec2d(
      # matrix multiplication with z ignored
      # (note: our matrix format is a little different to toModelView())
      p.x*i[0][0] + p.y*i[0][1] + 0*i[0][2] + 1*i[0][3],
      p.x*i[1][0] + p.y*i[1][1] + 0*i[1][2] + 1*i[1][3],
    )
