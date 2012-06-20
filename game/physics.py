'''
A file to hold together things about physics
Things about the interaction between 2 entities should not really be in engine, or one entitiy
Therefore it's in here
'''
from pymunk import Vec2d, Space

from Entities.Rocket import Rocket
from Entities.Player import Player
from Entities.Platform import Platform

import game.globals as game


physicsEntities = [Platform, Player, Rocket]

# a dict from a unique power of 2 (the layer number) to the entities that are in the layer
collisionLayers = {
  2**0 : [Platform, Player],
  2**1 : [Platform, Rocket],
}


def initPhysics(engine):
  # assign a unique collision type to each entity
  for entity, collisionType in zip(physicsEntities, range(len(physicsEntities))):
    entity.collisionType = collisionType

  # put collision layers into entities so they can initialize their shapes with them
  for entity in physicsEntities:
    entity.collisionLayers = 0 # just to be sure
    for layerNumber, collisionGroup in collisionLayers.items():
      if entity in collisionGroup:
        entity.collisionLayers += layerNumber

  # create our physics space
  engine.space = Space()
  engine.space.gravity = Vec2d(0.0, -900.0)
  engine.space.collision_bias = 0

  engine.space.add_collision_handler(
    Rocket.collisionType,
    Platform.collisionType,
    begin=rocketHandler
  )


# this class only groups collision handler functions together
def rocketHandler(space, arbiter, *args, **kwargs):
  print "KABLAAAM!"
  rocketShape = arbiter.shapes[0]
  for rocket in game.engine.groups['rockets']:
    if rocketShape in rocket.shapes:
      game.engine.removeEntity(rocket)
      break
  return False
