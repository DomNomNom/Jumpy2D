import pyglet.gl as gl

from Entity import Entity
from game.Vector import Vector
import game.globals

class DebugCross(Entity):
  '''A simple Entity that just draws a cross at engine.mousePos'''

  def __init__(self):
    self.size = Vector(8, 8)
    self.groups.add('UI')
  
  def update(self, dt):
    self.pos = game.globals.engine.mousePos
  
  def draw(self):
    gl.glColor3f(1.0, 0.0, 0.0)
    gl.glBegin(gl.GL_LINES)
    gl.glVertex2f(self.pos.x            , self.pos.y+self.size.y)
    gl.glVertex2f(self.pos.x            , self.pos.y-self.size.y)
    gl.glVertex2f(self.pos.x+self.size.x, self.pos.y            )
    gl.glVertex2f(self.pos.x-self.size.x, self.pos.y            )
    gl.glEnd()
