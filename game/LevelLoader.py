from os import path
from ast import literal_eval

import game.globals as game

from Entities.Platform import Platform
#TODO: more entities

class LevelLoader(object):

  constructors = {
    'Platform' : Platform,
    #'PlayerSpawn' : TODO
  }


  def __init__(self, levelName):
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

        if entityType not in self.constructors:
          print lineErr, "This is not a valid entity type:", entityType
          print lineErr, "Possible types:", self.constructors.keys()
          continue
        constructor = self.constructors[entityType]

        try:
          newEntity = constructor(*args)
        except:
          print lineErr, "Constructing", entityType, "failed. probably weird arguments:", args
          continue
        newEntities.append(newEntity)

    for entity in newEntities:
      game.engine.addEntity(entity)
