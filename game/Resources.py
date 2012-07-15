from pyglet import resource, image

class Resources(object):
  
  #basePath = 'game/Resources/'
  
  textures = {
    'platform' : 'platform.jpg',
  }
  
  def load(self):
    resource.path = ['game/Resources']
    resource.reindex()
    texturePath = 'Graphics/Textures/'
    for key, fileName in self.textures.items():
      self.textures[key] = image.TileableTexture.create_for_image(
        resource.texture(texturePath + fileName)
      )
