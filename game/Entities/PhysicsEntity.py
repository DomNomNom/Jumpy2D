from Entity import Entity
import pymunk
import game.globals as game

#
# PLEASE NOTE: every PhysicsEntity should be listed in game.physics.py ==> physicsEntities
#

class PhysicsEntity(Entity):
  mass = 10.
  moment = 30. # pymunk.moment_for_poly(mass, verticies)

  # please call this when you create a instance of a subclass of this
  def __init__(self):
    #self.body = game.engine.space.static_body
    self.groups = self.groups | {'game', 'physics'} # append to set
