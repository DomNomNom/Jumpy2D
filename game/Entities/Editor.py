from pyglet import image, sprite, graphics, gl
from pymunk import Vec2d

from Entity import Entity
import game.globals

class Editor(Entity):

  #CONSTRUCTOR
  def __init__(self):

    #set groups
    self.groups = self.groups | {'UI_editor'}
    self.drawLayer = 'UI_editor'

    #create variables
    self.numTabs = 8 #the number of tabs the editor has
    self.leftMouseDown = False #reflects the left mouse button's state
    self.rightMouseDown = False #reflects the right mouse button's state
    self.mousePos = game.globals.engine.mousePos
    self.gridOn = True #is the grid on
    self.snapToGridOn = True #is snap to grid on?
    self.gridSize = 32 #the size of a grid unit
    self.gridOffset = Vec2d(0, 0) # the x and y offsets of the grid

    #until resources is implement the editor currently loads its own images
    self.sideBarImage  = image.load("game/Resources/Graphics/EditorUI/editorUI.png")
    self.tab0Image     = image.load("game/Resources/Graphics/EditorUI/editorTab0.png") #deslected tab
    self.tab1Image     = image.load("game/Resources/Graphics/EditorUI/editorTab1.png") #selected tab

    #set sprites
    self.sideBarSprite = sprite.Sprite(self.sideBarImage)
    self.tabList = [] #list that contains all the sprites of the tabs
    for i in xrange(self.numTabs):
      self.tabList.append(sprite.Sprite(self.tab0Image)) #default load all the tabs to unselected

    #scaling
    self.scale = float(game.globals.engine.window.height)/1080.0 #find the scale
    self.sideBarSprite.scale  = self.scale
    for i in self.tabList:
      i.scale = self.scale

    #set positions
    self.sideBarSprite.position = (0, 0);
    j = 0
    for i in self.tabList:
      i.position = ((38.0*self.scale)+(i.width*j), 1004.0*self.scale)
      j += 1

    self.selectTab(0) #select the first tab

  #FUNCTIONS
  #Updates the editor
  def update(self, dt):
    #poll the input here
    #process the input here
    pass


  #Draw the editor
  def draw(self):
    if self.gridOn: #draw the grid if it is on
      gl.glColor3f(0.5, 0.5, 0.5)
      winWidth = game.globals.engine.window.width
      winHeight = game.globals.engine.window.height
      gl.glBegin(gl.GL_LINES)
      for i in xrange(int(self.gridOffset.x), winWidth, self.gridSize): #draw the vertical lines
        gl.glVertex2f(i, 0)
        gl.glVertex2f(i, winHeight)
      for i in xrange(int(self.gridOffset.y), winHeight, self.gridSize):
        gl.glVertex2f(0, i)
        gl.glVertex2f(winWidth, i)
      gl.glEnd()

    self.sideBarSprite.draw() #draw the side bar

    for i in xrange(self.numTabs): #draw the tabs
      #self.tabList[i].draw()


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
    for i in range(self.numTabs):
      if i == tabNo: self.tabList[i].image = self.tab1Image
      else: self.tabList[i].image = self.tab0Image
