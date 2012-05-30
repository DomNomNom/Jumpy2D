from pyglet import app
import argparse

import game.globals
from game.Engine import Engine
from game.Entities.DebugCross import DebugCross


# set command line arguments
#TODO: arguments: nographics, windowed, resolution, nosound, demo (conflicts with editor)
parser = argparse.ArgumentParser(description='A 2D rocket jumping game. :D')
parser.add_argument('-e', '--editor', action="store_true", help='Starts the game in editor mode')
parser.add_argument('-l', '--level', type=file, help='Loads a level file at the start')


# parse command line arguments
args = parser.parse_args()

# Create the engine
game.globals.engine = Engine()

# Do stuff to the engine using the arguments (TODO)
if args.editor and args.level:
  print 'lets edit this level:', args.level.name
elif args.editor:
  print 'lets make a new level'
elif args.level:
  print 'lets play this level:', args.level.name
else:
  pass # go to menu

game.globals.engine.addEntity(DebugCross())

# 3.2.1. GO!
app.run()
