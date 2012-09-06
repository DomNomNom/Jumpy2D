from pyglet.sprite import Sprite as pygletSprite
from Entity import GameEntity

class Sprite(GameEntity):
  
  def __init__(self, pos, textureName):
    self.tex = game.resources.textures[textureName]
    self.pos = Vec2D(pos)
    self.size = Vec2D(self.tex.width, self.tex.height)
    # TODO test me
    Sprite(tex)
  
  def draw(self):
    with shiftView(self.pos - self.size):
      tex = game.resources.textures['platform']
      tex.blit_tiled(0,0, 0, *(self.size*2))
