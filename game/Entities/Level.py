from pymunk import Vec2d, Space

# for saving loading
from os import path, mkdir, pardir
from ast import literal_eval

from Entity import Entity
from game.physics import rocketHandler

from Rocket import Rocket
from Player import Player
from Platform import Platform
from SpawnPoint import SpawnPoint

import game.globals as game


class Level(Entity):
  constructors = {
    'Platform' : Platform,
    'SpawnPoint' : SpawnPoint
  }

  chrashOnConstructorFail = True # TODO: move this to a config


  def __init__(self, playerInput, levelName):
    self.groups = {'all', 'level'}
    # create our physics space
    self.space = Space()
    self.space.gravity = Vec2d(0.0, -900.0)
    self.space.collision_bias = 0

    self.space.add_collision_handler(
      Rocket.collisionType,
      Platform.collisionType,
      begin=rocketHandler
    )

    self.ids = {} # a dict for IDs to entities

    self.player = Player(self, playerInput, pos=(320, 240))
    self.addEntity(0, self.player)
    self.loadEntities(levelName)

  def loadEntities(self, levelName):
    # TODO: uncompression

    levelPath = path.join(path.dirname(__file__), pardir, 'Resources', 'Levels', 'uncompressed', levelName, 'level.txt')
    with open(levelPath) as levelFile:
      lineCount = 0
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
        self.addEntity(entityID, newEntity) # TODO
        #newEntities.append(newEntity)

    #return newEntities


  def addEntity(self, entityID, entity):
    assert entityID not in self.ids
    self.ids[entityID] = entity
    game.engine.addEntity(entity)


  def saveEntities(self, levelName, entities):
    levelPath = path.join(path.dirname(__file__), pardir, 'Resources', 'Levels', 'uncompressed', levelName, 'level.txt')
    levelDir = path.dirname(levelPath)
    if not path.exists(levelDir):
      mkdir(levelDir)

    with open(levelPath, 'w') as levelFile:
      for entity in entities:
        levelFile.write(repr(entity) + '\n')
