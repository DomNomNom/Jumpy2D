from game.Vector import Vector

# TODO: sorting by drawLayer
class Entity:
  pos = Vector(0., 0.)
  vel = Vector(0., 0.)

  size = Vector(100, 100) # distance from center (pos)

  groups = {'all', 'updating'} # a set of groups we are in (see Engine.groups)

  def update(self, dt):
    self.move(dt)

  def move(self, dt):
    self.pos += self.vel * dt

  def draw(self):
    pass

