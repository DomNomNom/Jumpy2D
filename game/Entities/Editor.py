from Entity import Entity
from game.Vector import Vector
import game.globals

class Editor(Entity):

  #Constructor
  def __init__(self):
    self.leftMouseDown = False #reflects the left mouse button's state
    self.rightMouseDown = False #reflects the right mouse button's state
    self.mousePos = game.globals.engine.mousePos

  #Functions    
  #Updates the editor
  def update(self, dt):
    #poll the input here
    #process the input here
    print("I am updating")

  #Draw the editor
  def draw(self):
    pass #do nothing

  def leftMouseDown(self):
    leftMouseDown = True

  def leftMouseUp(self):
    leftMouseDown = False

  def rightMouseDown(self):
    rightMouseDown = True

  def rightMouseUp(self):
    rightMouseDown = False
