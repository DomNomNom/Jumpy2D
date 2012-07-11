import math
from pyglet import image, sprite, graphics, gl
from pymunk import Vec2d

from Entity import Entity
from Level import Level
from Platform import Platform
import game.globals

class Editor(Entity):

  #CONSTRUCTOR
  def __init__(self, levelName=None):

    self.focus = False

    #set groups
    self.groups = self.groups | {'UI_editor'}
    self.drawLayer = 'UI_editor'
    self.batch = game.globals.engine.drawLayersBatch[self.drawLayer]

    #create variables
    self.numTabs = 8 #the number of tabs the editor has
    self.leftMouseDown = False #reflects the left mouse button's state
    self.rightMouseDown = False #reflects the right mouse button's state
    self.mousePos = game.globals.engine.mousePos
    self.windowSize = Vec2d(game.globals.engine.window.get_size()) #gets the window size as a vector
    self.selected = "platform" #the current slected object
    self.brushShape = "rectangle" #the current brush shape
    self.gridOn = True #is the grid on
    self.snapToGrid = True #is snap to grid on?
    self.gridSize = Vec2d(16, 16) #the size of a grid unit
    self.gridOffset = Vec2d(0, 0) #the x and y offsets of the grid
    self.dragBoxStart = Vec2d(0, 0) #the start coords of the dragbox
    self.dragBoxOrigin = Vec2d(0, 0) #the original drag box start point
    self.dragBoxEnd = Vec2d(0, 0) #the end coords of the dragbox
    self.level = Level(levelName=levelName)  # The level that will store our entities

    #until resources is implement the editor currently loads its own images
    self.sideBarImage  = image.load("game/Resources/Graphics/EditorUI/editorUI.png")
    self.tab0Image     = image.load("game/Resources/Graphics/EditorUI/editorTab0.png") #deslected tab
    self.tab1Image     = image.load("game/Resources/Graphics/EditorUI/editorTab1.png") #selected tab

    #set sprites
    self.sideBarSprite = sprite.Sprite(self.sideBarImage, batch = self.batch)
    self.tabList = [] #list that contains all the sprites of the tabs
    for i in xrange(self.numTabs):
      self.tabList.append(sprite.Sprite(self.tab0Image, batch = self.batch)) #default load all the tabs to unselected

    #scaling
    self.scale = float(game.globals.engine.window.height)/1080.0 #find the scale
    self.sideBarSprite.scale  = self.scale
    for i in self.tabList:
      i.scale = self.scale

    #set positions
    self.sideBarSprite.position = (0, 0)
    j = 0
    for i in self.tabList:
      i.position = ((38.0*self.scale)+(i.width*j), 1004.0*self.scale)
      j += 1

    self.selectTab(0) #select the first tab

    #mouse event functions
    @game.globals.engine.window.event
    def on_mouse_press(x, y, button, modifiers):
      if button == 1:
        self.leftMouseDown = True
        if self.snapToGrid: self.dragBoxStart = Vec2d(x-(x%self.gridSize.x), y-(y%self.gridSize.x)+self.gridSize.x)
        else: self.dragBoxStart = Vec2d(x, y)
        self.dragBoxOrigin = self.dragBoxStart
      elif button == 4: self.rightMouseDown = True
      self.dragBoxEnd = self.dragBoxStart

    @game.globals.engine.window.event
    def on_mouse_release(x, y, button, modifiers):
      if button == 1:
        self.leftMouseDown = False
        self.place()
      elif button == 4: self.rightMouseDown = False


  #FUNCTIONS
  #Updates the editor
  def update(self, dt):
    #checks to see if the mouse is at the edge of the screen and moves camera accordingly
    if self.mousePos.x >= self.windowSize.x*0.95: #move the camera to the right
        game.globals.engine.camera.gameFocus = game.globals.engine.camera.gameFocus-Vec2d(2, 0)
    elif self.mousePos.x <= self.windowSize.x*0.05: #move the camera to the left
        game.globals.engine.camera.gameFocus = game.globals.engine.camera.gameFocus+Vec2d(2, 0)
    if self.mousePos.y >= self.windowSize.y*0.95: #move the camera up
        game.globals.engine.camera.gameFocus = game.globals.engine.camera.gameFocus-Vec2d(0, 2)
    elif self.mousePos.y <= self.windowSize.y*0.05: #move the camera down
        game.globals.engine.camera.gameFocus = game.globals.engine.camera.gameFocus+Vec2d(0, 2)
        
    
    
    #when the drag box is snapping to grid make sure a dragged over squares are in the box
    if self.leftMouseDown and self.snapToGrid:
      if self.mousePos.x < self.dragBoxStart.x and self.dragBoxStart.x == self.dragBoxOrigin.x:
        self.dragBoxStart = self.dragBoxStart+Vec2d(self.gridSize.x, 0)
      elif self.mousePos.x >= self.dragBoxStart.x and self.dragBoxStart.x > self.dragBoxOrigin.x:
        self.dragBoxStart = self.dragBoxStart-Vec2d(self.gridSize.x, 0)
      if self.mousePos.y > self.dragBoxStart.y and self.dragBoxStart.y == self.dragBoxOrigin.y:
        self.dragBoxStart = self.dragBoxStart-Vec2d(0, self.gridSize.x)
      elif self.mousePos.y <= self.dragBoxStart.y and self.dragBoxStart.y < self.dragBoxOrigin.y:
        self.dragBoxStart = self.dragBoxStart+Vec2d(0, self.gridSize.x)

    #get the mouse position if a drag box is being created
    if self.leftMouseDown:
      if self.snapToGrid:
        self.dragBoxEnd = self.mousePos-(self.mousePos%self.gridSize)
        if self.mousePos.x >= self.dragBoxStart.x: self.dragBoxEnd = self.dragBoxEnd+Vec2d(self.gridSize.x, 0)
        if self.mousePos.y >= self.dragBoxStart.y: self.dragBoxEnd = self.dragBoxEnd+Vec2d(0, self.gridSize.x)
      else: self.dragBoxEnd = Vec2d(self.mousePos.x, self.mousePos.y)


  #Draw the editor
  def draw(self):
    #draw grid
    if self.gridOn:
      gl.glColor4d(0.5, 0.5, 0.5, 0.5)
      winWidth = game.globals.engine.window.width
      winHeight = game.globals.engine.window.height
      gl.glBegin(gl.GL_LINES)
      for i in xrange(int(self.gridOffset.x), winWidth, int(self.gridSize.x)): #draw the vertical lines
        gl.glVertex2f(i, 0)
        gl.glVertex2f(i, winHeight)
      for i in xrange(int(self.gridOffset.y), winHeight, int(self.gridSize.x)):
        gl.glVertex2f(0, i)
        gl.glVertex2f(winWidth, i)
      gl.glEnd()

    #draw the left mouse drag box
    if self.leftMouseDown:
      gl.glColor4f(0.0, 0.0, 1.0, 0.35)

      if self.brushShape == "circle": #draw a circle
        #Find the dimensions of the circle
        centreCircle = Vec2d(((self.dragBoxEnd.x-self.dragBoxStart.x)/2.0+self.dragBoxStart.x), ((self.dragBoxEnd.y-self.dragBoxStart.y)/2.0+self.dragBoxStart.y))
        circleWidth = (self.dragBoxEnd.x-self.dragBoxStart.x)/2.0
        circleHeight = (self.dragBoxEnd.y-self.dragBoxStart.y)/2.0
        #draw the inner circle
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glVertex2f(centreCircle.x, centreCircle.y)
        for i in xrange(0, 365, 5):
          rad = (i*math.pi)/180.0 #converts to raidians
          gl.glVertex2f(centreCircle.x+math.sin(rad)*circleWidth, centreCircle.y+math.cos(rad)*circleHeight)
        gl.glEnd()
        #draw the circle outline
        gl.glColor4f(0.0, 0.0, 1.0, 1.0)
        gl.glBegin(gl.GL_LINE_LOOP)
        for i in xrange(0, 360, 5):
          rad = (i*math.pi)/180.0 #converts to raidians
          gl.glVertex2f(centreCircle.x+math.sin(rad)*circleWidth, centreCircle.y+math.cos(rad)*circleHeight)
        gl.glEnd()

      else: #draw a rectangle or a triangle
        if self.brushShape == "rectangle": gl.glBegin(gl.GL_QUADS) #draw a rectangle
        elif self.brushShape == "triangle": gl.glBegin(gl.GL_TRIANGLES) #draw a triangle
        #draw the inner box
        gl.glVertex2f(self.dragBoxStart.x, self.dragBoxStart.y)
        if self.brushShape == "rectangle": gl.glVertex2f(self.dragBoxEnd.x, self.dragBoxStart.y)
        gl.glVertex2f(self.dragBoxEnd.x, self.dragBoxEnd.y)
        gl.glVertex2f(self.dragBoxStart.x, self.dragBoxEnd.y)
        gl.glEnd()
        #draw the outline
        gl.glColor4f(0.0, 0.0, 1.0, 1.0)
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glVertex2f(self.dragBoxStart.x, self.dragBoxStart.y)
        if self.brushShape == "rectangle": gl.glVertex2f(self.dragBoxEnd.x, self.dragBoxStart.y)
        gl.glVertex2f(self.dragBoxEnd.x, self.dragBoxEnd.y)
        gl.glVertex2f(self.dragBoxStart.x, self.dragBoxEnd.y)
        gl.glEnd()

  #set the given tab as the selected tab
  def selectTab(self, tabNo):
    for i in range(self.numTabs):
      if i == tabNo: self.tabList[i].image = self.tab1Image
      else: self.tabList[i].image = self.tab0Image

  #place an object into the level
  def place(self):
    cam = game.globals.engine.camera
    with cam.shiftView():
      s = cam.toModelSpace(self.dragBoxStart)
      e = cam.toModelSpace(self.dragBoxEnd)
    size = (e-s) / 2
    game.globals.engine.addEntity(Platform(self.level, s+size, size))
