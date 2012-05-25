import pyglet

from game.Engine import Engine
from game.globals import engine

window = pyglet.window.Window()
engine = Engine(window)
posX = posY = 0


@window.event
def on_draw():
  engine.run()

@window.event
def on_mouse_motion(x, y, dx, dy):
  global posX, posY
  posX = x
  posY = y


pyglet.app.run()
