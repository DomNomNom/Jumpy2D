#!/usr/bin/python
from pyglet import app
from pymunk import Vec2d
import argparse

# our globals
import game.globals
from game.Engine import Engine
from game.GameState import GameState
from game.Resources import Resources

from game.PlayerInput import KeyboardControl, Controller


from game.Entities.Editor import Editor # TODO: move to gameState
from game.Entities.DebugCross import DebugCross


# set command line arguments
#TODO: arguments: nographics, windowed, resolution, nosound, demo (conflicts with editor)
parser = argparse.ArgumentParser(description='A 2D rocket jumping game. :D')
parser.add_argument('-e', '--editor', action="store_true", help='Starts the game in editor mode')
parser.add_argument('-l', '--level', help='Loads a level at the start')

# parse command line arguments (note: this can fail and it will exit)
args = parser.parse_args()


# Create global variables
game.globals.engine = Engine()
game.globals.gameState = GameState()
game.globals.resources = Resources()
game.globals.resources.load()

engine = game.globals.engine # a shorthand


if args.editor:
  game.globals.gameState.pushState(GameState.editLevel())
else: # play a level
  # load a level when specified
  levelName = args.level
  if not levelName:
    levelName = 'test2'
  try:
    playerInput = Controller() # use a game pad input if we have one
  except:
    playerInput = KeyboardControl()
  game.globals.gameState.pushState(GameState.Play([playerInput], levelName))

engine.addEntity(DebugCross(engine.windowCenter, (1,1,1) ))
engine.addEntity(DebugCross(engine.mousePos,     (1,0,0) ))


# 3.2.1. GO!
app.run()
