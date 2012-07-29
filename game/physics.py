'''
A file to hold together things about physics
Things about the interaction between 2 entities should not really be in engine, or one entitiy
Therefore it's in here
'''

from pymunk import Vec2d, Space

from Entities.Rocket import Rocket
from Entities.Player import Player
from Entities.Trigger import Trigger
from Entities.Platform import Platform
from Entities.Explosion import Explosion

import game.globals as game


physicsEntities = [Platform, Player, Rocket, Trigger, Explosion]

# a dict from a unique power of 2 (the layer number) to the entities that are in the layer
collisionLayers = {
  2**0 : [Platform, Player],
  2**1 : [Platform, Rocket],
  2**2 : [Player,  Trigger],
  2**3 : [Player,  Explosion],
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


# creates and initializes a physics space
def initSpace():
  space = Space()
  space.gravity = Vec2d(0.0, -900.0)
  space.collision_bias = 0

  space.add_collision_handler(
    Rocket.collisionType,
    Platform.collisionType,
    begin = rocketHandler
  )
  space.add_collision_handler(
    Player.collisionType,
    Explosion.collisionType,
    begin = explosionHandler
  )
  space.add_collision_handler(
    Player.collisionType,
    Trigger.collisionType,
    begin    = triggerOn,
    separate = triggerOff
  )
  space.add_collision_handler(
    Player.collisionType,
    Platform.collisionType,
    post_solve = notifyPlayer
  )

  return space



## Collision handlers from here on

def rocketHandler(space, arbiter, *args, **kwargs):
  rocket = game.engine.shapeToEntity[arbiter.shapes[0]]
  rocket.explode()
  game.engine.removeEntity(rocket)
  return False

def explosionHandler(space, arbiter, *args, **kwargs):
  player    = game.engine.shapeToEntity[arbiter.shapes[0]]
  explosion = game.engine.shapeToEntity[arbiter.shapes[1]]
  explosion.onPlayerCollide(player)
  return False

def triggerOn(space, arbiter, *args, **kwargs):
  trigger = game.engine.shapeToEntity[arbiter.shapes[1]]
  trigger.triggered(True)
  return False

def triggerOff(space, arbiter, *args, **kwargs):
  try:
    triggerShape = arbiter.shapes[1]
  except:
    #print "OMG, pyglet shat itself."
    return False
  trigger = game.engine.shapeToEntity[triggerShape]
  trigger.triggered(False)
  return False

def notifyPlayer(space, arbiter, *args, **kwargs):
  player = game.engine.shapeToEntity[arbiter.shapes[0]]
  player.platformCollision(arbiter)
  return True
