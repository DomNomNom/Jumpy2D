#!/usr/bin/python
from pyglet import app
from pymunk import Vec2d
import argparse

# our engine
import game.globals
from game.Engine import Engine

# game state stuff (should be moved as well)
from game.LevelLoader import LevelLoader

# Things we are going to add to the engine
from game.KeyboardControl import KeyboardControl
from game.Controller import Controller

# Entities (TODO: move to level loader)
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
game.globals.engine = Engine()
engine = game.globals.engine # a shorthand

# Do stuff to the engine using the arguments (TODO)
if args.editor and args.level:
  print 'lets edit this level:', args.level.name
elif args.editor:
  game.engine.addEntity(Editor())
elif args.level:
  print 'lets play this level:', args.level.name
else:
  pass # go to menu

playerInput = KeyboardControl()
try:
  playerInput = Controller() # use game pad input if we have one
except: pass

player = Player(playerInput, pos=(320, 240))
engine.addEntity(player) #TODO: PlayerSpawn in level Loader
engine.addEntity(DebugCross(engine.windowCenter, (1,1,1) ))
engine.addEntity(DebugCross(engine.mousePos,     (1,0,0) ))

loader = LevelLoader('test')

# 3.2.1. GO!
app.run()
