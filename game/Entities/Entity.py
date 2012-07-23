from pymunk import Vec2d, Poly
import pyglet.gl as gl

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



class GameEntity(Entity):
  groups = {'all', 'updating', 'game'}
  
  def visible(self, state):
    # TODO: do something about sprites
    # TODO: set the draw-layer of the entity to None or type(self).drawLayer
    drawLayer = game.engine.drawLayers[self.drawLayer]
    if state:
      drawLayer.add(self)
    else:
      if self in drawLayer:
        drawLayer.remove(self)

  # This function should return a list like ('ClassName', constructorArguments...)
  # This is used by __repr__() and therefore for saving/re-creating a GameEntity
  # See Platform.py for an example
  def reconstructionArgs(self):
    return ["This should not happen"]

  # Returns a string of the following format: "'ClassName', constructorArg1, arg2"
  def __repr__(self, className='Trigger'):
    return ', '.join(map(repr, self.reconstructionArgs()))
      
  triggerables = {
    'visible' : visible,
  }



class PhysicsEntity(GameEntity):

  # PLEASE NOTE: every PhysicsEntity should be listed in
  #              game/physics.py ==> physicsEntities

  groups = {'all', 'updating', 'game', 'physics'}

  mass = 10.
  moment = 30. # pymunk.moment_for_poly(mass, verticies)
  level = None # The level that contains the physics Space
  
  # this is for the following funciton
  specialPolyTypes = {
    2 : gl.GL_LINES,
    3 : gl.GL_TRIANGLES,
    4 : gl.GL_QUADS,
  }

  # creates a shape for the Entities physics body with the given verticies
  def createShape(self, verticies):
    assert len(verticies) >= 2
    
    verticies = self.verticies = map(Vec2d, verticies)
    if len(verticies) in self.specialPolyTypes:
      self.polyType = self.specialPolyTypes[len(verticies)]
    else:
      self.polyType = pg.GL_POLYGON

    self.shape = Poly(self.body, verticies)

    # note: collisionLayers and collisionType get created by physics.py
    self.shape.layers = self.collisionLayers
    self.shape.collision_type = self.collisionType
    self.shapes = [self.shape]
