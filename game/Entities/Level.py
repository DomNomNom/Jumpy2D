# for saving and loading
from os import path, mkdir, pardir
from ast import literal_eval
from pyglet.resource import file as resourceOpen

from game.physics import initSpace

from game.PlayerInput import PlayerInput

# Entities
from Gates import NotGate
from Entity import Entity
from Rocket import Rocket
from Player import Player
from Trigger import Trigger, LevelEnd
from Platform import Platform
from SpawnPoint import SpawnPoint

import game.globals as game


class Level(Entity):
  constructors = { # To construct the entities when we load a level from a file
    'NotGate' : NotGate,
    'Trigger' : Trigger,
    'LevelEnd' : LevelEnd,
    'Platform' : Platform,
    'SpawnPoint' : SpawnPoint,
  }
  
  groups = {'all', 'level'} # note: updating is not in this as we're special

  chrashOnConstructorFail = True # TODO: move this to a config


  def __init__(self, playerInput=None, levelName=None):

    self.space = initSpace()   # create our physics space
    self.levelTime = 0

    self.ids = {} # a dict for IDs to entities

    if not playerInput:
      playerInput = PlayerInput()
    playerInput.level = self
    self.player = Player(self, playerInput, pos=(320, 240))
    self.levelName = levelName
    if levelName:
      self.addEntity(0, self.player)
      self.loadEntities(levelName)
    else:
      self.ids[0] = self.player

  # note: This will NOT be called from the loop though the 'updating' groups,
  #       It'll be from the 'level' group.
  def update(self, dt):
    if self.isPaused: return
    self.levelTime += dt
    self.space.step(dt)
    

  def setPaused(self, isPaused):
    self.isPaused = isPaused
    self.player.input.currentlyRecording = not isPaused
  

  def loadEntities(self, levelName):
    # TODO: uncompression

    lineCount = 0
    with resourceOpen('Levels/uncompressed/'+levelName+'/level.txt') as levelFile:
      for line in levelFile:
        lineCount += 1
        lineErr = "(line " + str(lineCount) + ")"
        if len(line.strip()) == 0:       continue # skip blank lines
        if line.strip().startswith('#'): continue # skip comment lines

        try:
          data = literal_eval(line)
        except:
          print lineErr, "This line could not be parsed:", line
          continue

        entityID, entityType, args = data[0], data[1], data[2:]

        if entityType not in Level.constructors:
          print lineErr, "This is not a valid entity type:", entityType
          print lineErr, "Possible types:", Level.constructors.keys()
          continue
        constructor = self.constructors[entityType]

        if self.chrashOnConstructorFail:
          newEntity = constructor(self, *args)
        else:
          try:
            newEntity = constructor(self, *args)
          except:
            print lineErr, "Constructing", entityType, "failed. probably weird arguments:", args
            continue
        self.addEntity(entityID, newEntity)


  def addEntity(self, entityID, entity):
    assert entityID not in self.ids, "Every entity needs a unique ID (start of line)"
    self.ids[entityID] = entity
    game.engine.addEntity(entity)


  def save(self):
    assert self.levelName
    '''
    levelPath = path.join(path.dirname(__file__), pardir, 'Resources', 'Levels', 'uncompressed', levelName, 'level.txt')
    levelDir = path.dirname(levelPath)
    if not path.exists(levelDir):
      mkdir(levelDir)
    '''
    # TODO: test whether this will create folders
    with resourceOpen('Levels/uncompressed/'+self.levelName+'/level.txt', 'w') as f:
      for entityID, entity in self.ids.iteritems():
        if entityID == 0:
          f.write('# 0 reserved for player\n')
        else:
          f.write('{0}, {1}\n'.format(entityID, repr(entity)))
