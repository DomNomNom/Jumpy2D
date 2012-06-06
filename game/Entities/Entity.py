from game.Vector import Vector

class Entity(object):
  pos = Vector(0., 0.)
  vel = Vector(0., 0.)

  size = Vector(100, 100) # distance from center (pos)

  groups = {'all', 'updating'} # a set of groups we are in (see Engine.groups)

  drawLayer = 'game' # None if it shouldn't be drawn; otherwise a string from engine.drawLayerNames

  def update(self, dt):
    self.move(dt)

  def move(self, dt):
    self.pos += self.vel * dt

  def draw(self):
    pass

