from __future__ import division
from math import cos,exp,atan2,sin
from marching import isosurface
from vectormath import *
from euclid import Vector3
  
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
def sclamp(x, c):
  return x*(abs(x) + c) / abs(x)
def gyroid(r):
  return sum(map(cos, r))
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
def orthocircle(r):
  r = r /8
  x,y,z = r.x,r.y,r.z
  ff = 0.075
  bb = 3.0
  return ((x**2 + y**2 - 1)**2 + z**2)*((y**2 + z**2 - 1)**2 + x**2)*((z**2 + x**2 - 1)**2 + y**2) - ff**2*(1 + bb*(x**2 + y**2 + z**2)) 

def func(x,y,z):
  r = Vector3(x,y,z)
  s = sphere(r, 5)
  g = gyroid(r)
  return orthocircle(r)

if __name__ == '__main__':
  from subprocess import call
  isosurface(func)
  call(["openscad", "-o", "out.png","-D",  'model="out.stl";',"veiw.scad"])
