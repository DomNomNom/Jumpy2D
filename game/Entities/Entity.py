from pymunk import Vec2d

import game.globals as game

class Entity(object):
  pos = Vec2d(0., 0.)
  vel = Vec2d(0., 0.)
  size = Vec2d(100, 100) # distance from center (pos)

  groups = {'all', 'updating'} #a set of groups we are in (see Engine.groups)

  drawLayer = 'game' #None if it shouldn't be drawn; otherwise a string from engine.drawLayerNames

  def update(self, dt):
    pass

  def draw(self):
    pass

  def visible(self, state):
    # TODO: do something about sprites
    # TODO: set the draw-layer of the entity to None or type(self).drawLayer
    drawLayer = game.engine.drawLayers[self.drawLayer]
    if state:
      drawLayer.add(self)
    else:
      if self in drawLayer:
        drawLayer.remove(self)
      
  triggerables = {
    'visible' : visible,
  }


class PhysicsEntity(Entity):

  # PLEASE NOTE: every PhysicsEntity should be listed in
  #              game/physics.py ==> physicsEntities

  groups = {'all', 'updating', 'game', 'physics'}

  mass = 10.
  moment = 30. # pymunk.moment_for_poly(mass, verticies)
  level = None # The level that contains the physics Space
