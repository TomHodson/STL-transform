from __future__ import division

class Vector: # struct XYZ  
  def __init__(self,x,y,z):  
    self.x=x  
    self.y=y  
    self.z=z
  def __add__(self, b):
    return Vector(self.x + b.x, self.y + b.y, self.z + b.z)
  def __mul__(self, a):
    return Vector(self.x*a, self.y*a, self.z*a)
  def __div__(self, a):
    return self * (1.0/a)
  def __sub__(self, a):
    return self + (a * -1.0)
  def __str__(self):  
    return str(self.x)+" "+str(self.y)+" "+str(self.z)  

def vector_product(a, b):
  x = a.y*b.z - a.z*b.y
  y = -1.0 * (a.x*b.z - a.z*b.x)
  z = a.x*b.y - a.y*b.x
  return Vector(x,y,z)
def mag(a, e = 2.0):
  return ( a.x**e + a.y**e + a.z**e ) ** (1.0/e)

def scalar_product(a,b):
  return a.x*b.x + a.y*b.y + a.z*b.z

def normal(a,b,c):
  n = vector_product(b-a, c-a)
  m = mag(n)
  return n

  from euclid import Vector3
  a = Vector3(1,2,3)
  b = Vector3(2,3,4)
  print vector_product(a,b)