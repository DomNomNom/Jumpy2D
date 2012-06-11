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

