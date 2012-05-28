from game.Vector import Vector

# TODO: sorting by drawLayer
class Entity:
  pos = Vector(0., 0.)
  vel = Vector(0., 0.)

  size = Vector(100, 100) # distance from center (pos)

  groups = {'all', 'updating'} # a set of groups we are in (see Enine.groups)

  def update(self, dt):
    pos += vel * dt

  def draw(self):
    pass
