import pyglet.gl as gl
from pymunk import Vec2d

from Entity import Entity
import game.globals

class DebugCross(Entity):
  '''A simple Entity that just draws a cross at engine.mousePos'''

  def __init__(self):
    self.size = Vec2d(8, 8)
    self.groups = self.groups | {'UI'}
    self.drawLayer = 'UI_debug'

  def update(self, dt):
    self.pos = game.globals.engine.mousePos

  def draw(self):
    s = self.size # just a shorthand
    gl.glColor3f(1.0, 0.0, 0.0)

    gl.glPushMatrix()
    gl.glTranslatef(self.pos.x, self.pos.y, 0)
    gl.glBegin(gl.GL_LINES)
    gl.glVertex2f(+s.x,    0)
    gl.glVertex2f(-s.x,    0)
    gl.glVertex2f(   0, +s.y)
    gl.glVertex2f(   0, -s.y)
    gl.glEnd()
    gl.glPopMatrix()
