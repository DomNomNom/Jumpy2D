from pyglet import image, sprite

from Entity import Entity
import game.globals

class Editor(Entity):

  #Constructor
  def __init__(self):
  
    self.groups = self.groups | {'UI_editor'}
    self.drawLayer = 'UI_editor'
    
    #create variable
    self.numTabs = 8 #the number of tabs the editor has
    self.leftMouseDown = False #reflects the left mouse button's state
    self.rightMouseDown = False #reflects the right mouse button's state
    self.mousePos = game.globals.engine.mousePos
    
    #until resources is implement the editor currently loads its own images
    self.sideBarImage  = image.load("game/Resources/Graphics/EditorUI/editorUI.png")
    self.tab0Image     = image.load("game/Resources/Graphics/EditorUI/editorTab0.png") #deslected tab
    self.tab1Image     = image.load("game/Resources/Graphics/EditorUI/editorTab1.png") #selected tab
    
    
    #set sprites
    self.sideBarSprite = sprite.Sprite(self.sideBarImage)
    #tab0 = image.load(sideBarImage)
    self.tabList = [] #list that contains all the sprites of the tabs
    i = 0
    while i < self.numTabs:
      self.tabList.append(sprite.Sprite(self.tab0Image)) #default load all the tabs to unselected
      i += 1
    
    #scaling
    scale = float(game.globals.engine.window.height)/1080.0 #find the scale
    self.sideBarSprite.scale  = scale
    i = 0
    while i < self.numTabs:
      self.tabList[i].scale = scale
      i += 1
    
    #set positions
    i = 0
    while i < self.numTabs:
      self.tabList[i].position = ((38.0*scale)+(self.tabList[i].width*i), 1004.0*scale)
      i += 1
    
    self.selectTab(0)  

  #Functions    
  #Updates the editor
  def update(self, dt):
    #poll the input here
    #process the input here
    pass

  #Draw the editor
  def draw(self):
    self.sideBarSprite.draw()
    i = 0
    while i < self.numTabs:
      self.tabList[i].draw()
      i += 1

  def leftMouseDown(self):
    leftMouseDown = True

  def leftMouseUp(self):
    leftMouseDown = False

  def rightMouseDown(self):
    rightMouseDown = True

  def rightMouseUp(self):
    rightMouseDown = False
  
  #set the given tab as the selected tab  
  def selectTab(self, tabNo):
    i = 0
    while i < self.numTabs:
      if i == tabNo: self.tabList[i].image = self.tab1Image
      else: self.tabList[i].image = self.tab0Image
      i += 1
