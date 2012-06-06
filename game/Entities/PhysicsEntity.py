from Entity import Entity

class PhysicsEntity(Entity):

  # please call this when you create a instance of a subclass of this
  def __init__(self):
    self.groups.update(['game', 'physics']) # append to set
