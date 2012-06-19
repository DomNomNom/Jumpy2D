#!/usr/bin/python
from pyglet import app
from pymunk import Vec2d
import argparse

# our globals
import game.globals
from game.Engine import Engine
from game.GameState import GameState

# game state stuff (should be moved as well)
from game.LevelLoader import loadLevel, saveLevel #TODO: move load/save to gamestate

# Entities (TODO: move to level loader)
from game.Entities.Editor import Editor
from game.Entities.Platform import Platform
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
engine = game.globals.engine # a shorthand

# load a level when specified
if args.level:
  for entity in loadLevel(args.level):
    engine.addEntity(entity)

if args.editor:
  engine.addEntity(Editor())
else: # play a level
  if not args.level: # if no level is specified, load a default level
    for entity in loadLevel('test2'):
      engine.addEntity(entity)
  game.globals.gameState.pushState(GameState.PlayCurrentLevel())

engine.addEntity(DebugCross(engine.windowCenter, (1,1,1) ))
engine.addEntity(DebugCross(engine.mousePos,     (1,0,0) ))


# 3.2.1. GO!
app.run()
