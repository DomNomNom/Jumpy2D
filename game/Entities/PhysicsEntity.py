from Entity import Entity
import pymunk
import game.globals as game

class PhysicsEntity(Entity):
  mass = 10.
  moment = 30. # pymunk.moment_for_poly(mass, verticies)

  # please call this when you create a instance of a subclass of this
  def __init__(self):
    #self.body = game.engine.space.static_body
    self.groups.update(['game', 'physics']) # append to set
