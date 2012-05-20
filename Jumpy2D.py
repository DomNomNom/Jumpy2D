import pyglet
from pyglet.gl import *

from Controller import Controller
from Vector import Vector

window = pyglet.window.Window()
posX = posY = 0
c = Controller()
windowCenter = Vector(window.get_size()[0], window.get_size()[1]) / 2

# draw a cross at the position of a vector
def drawCross(v):
    r = 8
    glBegin(GL_LINES)
    glVertex2f(v.x  , v.y+r)
    glVertex2f(v.x  , v.y-r)
    glVertex2f(v.x+r, v.y  )
    glVertex2f(v.x-r, v.y  )
    glEnd()

@window.event
def on_draw():
    global posX, posY, c, windowCenter
    glClearColor(0,0,0, 50)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    glColor3f(1.0, 0.0, 0.0)
    drawCross(Vector(posX, posY))
    
    glColor3f(0.0, 1.0, 0.0)
    drawCross(windowCenter + 100 * c.stick_l_raw)
    glColor3f(1.0, 1.0, 0.0)
    drawCross(windowCenter + 100 * c.stick_r_raw)
    
    glColor3f(1.0, 1.0, 1.0)
    drawCross(windowCenter)

@window.event
def on_mouse_motion(x, y, dx, dy):
  global posX, posY
  posX = x
  posY = y



pyglet.app.run()
