import pyglet

from game.Engine import Engine
import game.globals


game.globals.engine = Engine() # FIXME? is this the global one?

pyglet.app.run()
