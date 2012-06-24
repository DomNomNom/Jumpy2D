from pymunk import Vec2d

class Entity(object):
  pos = Vec2d(0., 0.)
  vel = Vec2d(0., 0.)
  size = Vec2d(100, 100) # distance from center (pos)

  groups = {'all', 'updating'} # a set of groups we are in (see Engine.groups)

  drawLayer = 'game' # None if it shouldn't be drawn; otherwise a string from engine.drawLayerNames

  def update(self, dt):
    pass

  def draw(self):
    pass



class PhysicsEntity(Entity):

  # PLEASE NOTE: every PhysicsEntity should be listed in
  #              game/physics.py ==> physicsEntities

  mass = 10.
  moment = 30. # pymunk.moment_for_poly(mass, verticies)

  # please call this when you create a instance of a subclass of this
  def __init__(self):
    #self.body = game.engine.space.static_body
    self.groups = self.groups | {'game', 'physics'} # append to set
