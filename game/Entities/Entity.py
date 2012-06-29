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

  # note: some PhysicsEntities can be "partial" physics entities. eg:
  #       the editor shoud be able to create a platform without a physicsSpace

  # PLEASE NOTE: every PhysicsEntity should be listed in
  #              game/physics.py ==> physicsEntities

  groups = {'all', 'updating', 'game', 'physics'}

  mass = 10.
  moment = 30. # pymunk.moment_for_poly(mass, verticies)
  level = None # The level that contains the physics Space
