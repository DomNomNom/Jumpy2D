from math import hypot, sin, cos, acos, pi

"""
  A simple 2D vector.
  
  note: does no type checking.
"""
class Vector:
  x = 0 
  y = 0
  
  # Constructor
  def __init__(self, x=0, y=0):
    self.x = x
    self.y = y
    
  def __neg__(self):
    return Vector(
      -self.x,
      -self.y,
    )
  
  def __add__(self, other):
    return Vector(
      self.x + other.x,
      self.y + other.y,
    )
    
  def __sub__(self, other):
    return Vector(
      self.x - other.x,
      self.y - other.y,
    )
  
  def __mul__(self, factor):
    return Vector(
      self.x * factor,
      self.y * factor,
    )
  
  def __rmul__(self, factor):
    return self * factor # calling the above
    
  def __div__(self, denominator):
    return Vector(
      self.x / denominator,
      self.y / denominator,
    )
  
  def __iadd__(self, other):
    self.x += other.x
    self.y += other.y
    return self
  
  def __isub__(self, other):
    self.x -= other.x
    self.y -= other.y
    return self
  
  # multiply this vector by a scalar factor
  def __imul__(self, factor):
    self.x *= factor
    self.y *= factor
    return self 

  def __idiv__(self, denominator):
    self.x /= denominator
    self.y /= denominator
    return self

  def __repr__(self):
    return str(self.tuple())
  
  def tuple(self):
    return (self.x, self.y)

  # magnitude of this vector
  def mag(self):
    return hypot(self.x, self.y)
  
  # distance between vectors
  def dist(self, other):
    return hypot(
      self.x - other.x,
      self.y - other.y,
    )
  
  # Dot product
  def dot(self, other):
    return (
      self.x*other.x +
      self.y*other.y
    )
    
  # normalize the vector
  def norm(self):
    self /= self.mag()
    return self

  # angle between this and (1, 0)
  def angle(self):
    return acos(self.x / self.mag())

  # angle between two vectors
  def angleBetween(self, other):
    return acos(
      self.dot(other) / (self.mag() * other.mag())
    )
    
  # value copy from another vector
  def copyFrom(self, other):
    self.x = other.x
    self.y = other.y
    return self
    
  def constrainLength(self, length):
    if self.mag() > length:
      self *= (length / self.mag())
    return self
    
  def rotate(self, theta):
    (self.x, self.y) = (
      self.x*cos(theta) - self.y*sin(theta),
      self.x*sin(theta) + self.y*cos(theta)
    )
    return self
    

# if this is the main file
if __name__ == "__main__":
  a = Vector("abc", "hello ")
  print a*2
  
  #print b.rotate(pi/2)
  #print b.rotate(-pi*0.5)
  #print a + Vector(2, 1), a
