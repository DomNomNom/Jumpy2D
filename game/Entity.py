class Entity:
  pos = Vector(0., 0.)
  vel = Vector(0., 0.)

  size = Vector(100, 100) # distance from center (pos)

  groups = set()

  def update(self, dt):
    pos += vel * dt

  def draw(self):
    pass

