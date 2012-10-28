from pyglet.sprite import Sprite as pygletSprite
from Entity import GameEntity
from pymunk import Vec2d
from game.Camera import shiftView

import game.globals as game

class Sprite(GameEntity):
  
  def __init__(self, level, pos, textureName):
    self.level = level
    self.textureName = textureName
    self.tex = game.resources.textures[textureName]
    self.pos = Vec2d(pos)
    self.size = Vec2d(self.tex.width, self.tex.height)
    # TODO test me
    self.pySprite = pygletSprite(self.tex, *(self.pos - self.size))
  
  def draw(self):
    
    with shiftView(self.pos - self.size):
      tex = game.resources.textures['platform']
      #tex.blit(0,0, 0, *(self.size*2))
    self.pySprite.draw()
    
  
  def reconstructionArgs(self):
    return [
      'Sprite',
      tuple(self.pos),
      self.textureName
    ]
