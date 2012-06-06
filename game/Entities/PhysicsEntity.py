from Entity import Entity
from pymunk import Body

class PhysicsEntity(Entity):
  mass = 10
  moment = 3000 # pymunk.moment_for_poly(mass, vs)

  # please call this when you create a instance of a subclass of this
  def __init__(self):
    self.body = Body(self.mass, self.moment)
    self.groups.update(['game', 'physics']) # append to set
