from pyglet.gl import *

from Entity import Entity
from game.Vector import Vector
import game.globals

"""
simple Entity that just draws a cross at the mousePos
"""
class DebugCross(Entity):
  def __init__(self):
    #self.super()
    self.size = Vector(8, 8)
    self.groups.add('game')
  
  def update(self, dt):
    self.pos = game.globals.engine.mousePos
  
  def draw(self):
    glBegin(GL_LINES)
    glVertex2f(self.pos.x            , self.pos.y+self.size.y)
    glVertex2f(self.pos.x            , self.pos.y-self.size.y)
    glVertex2f(self.pos.x+self.size.x, self.pos.y            )
    glVertex2f(self.pos.x-self.size.x, self.pos.y            )
    glEnd()
