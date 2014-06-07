from math import cos,exp,atan2,sin
from marching import isosurface
from vectormath import *
  
def lobes(x,y,z):  
 try:  
  theta = atan2(x,y)         # sin t = o   
 except:  
  theta = 0  
 try:  
  phi = atan2(z,y)  
 except:  
  phi = 0  
 r = x*x+y*y+z*z  
 ct=cos(theta)  
 cp=cos(phi)  
 return ct*ct*cp*cp*exp(-r/10)

from math import log, tan
def smax(x,y):
  return log(exp(x) + exp(y))

def smin(x,y):
  return log(exp(-x) + exp(-y))
def clamp(val, c):
  return 0 if abs(val) < c else val

def sphere(p,r):
  return mag(p) - r
def cubisphere(p,r):
  return mag(p, e = 6.0) - r
def oddsphere(p,r):
  d = p.x**3 + p.y**3 + p.z**3
  return d - 5.0
def plane(p):
  a = p
  b = Vector(1,2,3)
  return scalar_product(a,b)
def line(p):
  a = p
  b = Vector(1,2,3)
  return 0

def func(x,y,z):
  p = Vector(x,y,z)
  b = sphere(p, 10.0)
  try:
    a = 1.0/x + 1.0/y + 1.0/z
    return max(a,b)
  except:
    return 1000

if __name__ == '__main__':
  isosurface(func)