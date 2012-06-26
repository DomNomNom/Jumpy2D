from os import path, mkdir
from ast import literal_eval

import game.globals as game

from Entities.Platform import Platform
from Entities.SpawnPoint import SpawnPoint
#TODO: more entities


constructors = {
  'Platform' : Platform,
  'SpawnPoint' : SpawnPoint
}


def loadLevel(levelName):
  # TODO: uncompression
  newEntities = []

  levelPath = path.join(path.dirname(__file__), 'Resources', 'Levels', 'uncompressed', levelName, 'level.txt')
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

      entityType, args = data[0], data[1:]

      if entityType not in constructors:
        print lineErr, "This is not a valid entity type:", entityType
        print lineErr, "Possible types:", constructors.keys()
        continue
      constructor = constructors[entityType]

      try:
        newEntity = constructor(*args)
      except:
        print lineErr, "Constructing", entityType, "failed. probably weird arguments:", args
        continue
      newEntities.append(newEntity)

  return newEntities



def saveLevel(levelName, entities):
  levelPath = path.join(path.dirname(__file__), 'Resources', 'Levels', 'uncompressed', levelName, 'level.txt')
  levelDir = path.dirname(levelPath)
  if not path.exists(levelDir):
    mkdir(levelDir)

  with open(levelPath, 'w') as levelFile:
    for entity in entities:
      levelFile.write(repr(entity) + '\n')
