'''
A file to hold together things about physics
Things about the interaction between 2 entities should not really be in engine, or one entitiy
Therefore it's in here
'''

from Entities.Rocket import Rocket
from Entities.Player import Player
from Entities.Trigger import Trigger
from Entities.Platform import Platform

import game.globals as game


physicsEntities = [Platform, Player, Rocket, Trigger]

# a dict from a unique power of 2 (the layer number) to the entities that are in the layer
collisionLayers = {
  2**0 : [Platform, Player],
  2**1 : [Platform, Rocket],
  2**2 : [Player,  Trigger],
}


# assign a unique collision type to each entity
for entity, collisionType in zip(physicsEntities, xrange(len(physicsEntities))):
  entity.collisionType = collisionType

# put collision layers into entities so they can initialize their shapes with them
for entity in physicsEntities:
  entity.collisionLayers = 0 # just to be sure
  for layerNumber, collisionGroup in collisionLayers.items():
    if entity in collisionGroup:
      entity.collisionLayers += layerNumber


## Collision handlers from here on

def rocketHandler(space, arbiter, *args, **kwargs):
  rocketShape = arbiter.shapes[0]
  for rocket in game.engine.groups['rockets']:
    if rocketShape in rocket.shapes:
      rocket.explode()
      game.engine.removeEntity(rocket)
      break
  return False

def triggerOn(space, arbiter, *args, **kwargs):
  print 'Trigger On'
  return False
def triggerOff(space, arbiter, *args, **kwargs):
  print "Trigger Off"
  return False
