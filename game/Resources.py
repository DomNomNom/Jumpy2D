from pyglet import resource, image

import os # for creating files

def createFile(path, fileName):
  # path format example: 'Graphics/path/To/folder'
  # paths are relativae to game/Resources/
  
  # make a ['path', 'to', 'file.txt'] form
  fullPath = (
      [os.path.dirname(__file__), 'Resources'] # assumes this file is in jumpy/game
    + path.strip(' /').split('/')
    + [fileName]
  )
  
  fullPath = os.path.join(*fullPath) # now it's in a "./path/to/file" form
  
  dirName = os.path.dirname(fullPath)
  if not os.path.exists(dirName):
    os.makedirs(dirName)
  
  return open(fullPath, 'w')

class Resources(object):
  
  basePath = 'game/Resources/'
  
  textures = {
    'platform' : 'platform.jpg',
  }
  
  def load(self): # loads all the things. TODO: make a gameState that only loads sepcific things
    resource.path = [self.basePath]
    resource.reindex()
    texturePath = 'Graphics/Textures/'
    for key, fileName in self.textures.items():
      self.textures[key] = image.TileableTexture.create_for_image(
        resource.texture(texturePath + fileName)
      )
