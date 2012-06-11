#!/usr/bin/python
from pyglet import app
import argparse

# our engine
import game.globals as game
from game.Engine import Engine

# Things we are going to add to the engine
from game.KeyboardControl import KeyboardControl

# Entities
from game.Entities.Editor import Editor
from game.Entities.Player import Player
from game.Entities.Platform import Platform
from game.Entities.DebugCross import DebugCross


# set command line arguments
#TODO: arguments: nographics, windowed, resolution, nosound, demo (conflicts with editor)
parser = argparse.ArgumentParser(description='A 2D rocket jumping game. :D')
parser.add_argument('-e', '--editor', action="store_true", help='Starts the game in editor mode')
parser.add_argument('-l', '--level', type=file, help='Loads a level file at the start')


# parse command line arguments (note: this can fail and it will exit)
args = parser.parse_args()

# Create the engine
game.engine = Engine()

# Do stuff to the engine using the arguments (TODO)
if args.editor and args.level:
  print 'lets edit this level:', args.level.name
elif args.editor:
  game.engine.addEntity(Editor())
elif args.level:
  print 'lets play this level:', args.level.name
else:
  pass # go to menu

game.engine.addEntity(DebugCross())
game.engine.addEntity(Player(KeyboardControl()))
game.engine.addEntity(Platform())

# 3.2.1. GO!
app.run()
