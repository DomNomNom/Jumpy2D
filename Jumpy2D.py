from pyglet import app

from game.Engine import Engine
import game.globals
#from game.globals import *

global engine
game.globals.engine = Engine()

#e2 = Engine()

app.run()