from Entity import Entity
import game.globals

class EditorIcon(Entity):
  
  #CONSTRUCTOR
  def __init__(self, pos, img, scale, func):
    self.pos = pos
    self.sprite = img
    self.scale = scale
    self.action = func
    self.display = True #is true when the icon should be displayed
    
    self.groups = self.groups | {'UI_editor'}
    self.drawLayer = 'UI_editor'
    self.batch = game.globals.engine.drawLayersBatch[self.drawLayer]
    
    self.sprite.position = (pos.x*self.scale, pos.y*self.scale)
    self.sprite.scale = self.scale
    
  #FUNCTIONS
  #returns true if the given mouse position is on the icon
  def mouseOn(self, mousePos):
    if mousePos.x < pos.x or mousePos.x > pos.x+16: return False
    if mousePos.y < pos.y or mousePos.y > pos.y+16: return False
    return True
    
  #Draws the icon
  def draw(self):
    pass
