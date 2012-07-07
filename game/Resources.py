from pyglet import resource
from pyglet import image

class Resources(object):
  
  textures = {
    'platform' : 'platform.jpg',
  }
  
  def load(self):
    #print 'DING'
    #resource.path = ['game']
    #print resource.path
    #resource.location('game')
    texturePath = 'game/Resources/Graphics/Textures/'
    for key, fileName in self.textures.items():
      self.textures[key] = image.TileableTexture.create_for_image(
        resource.texture(texturePath + fileName)
      )
