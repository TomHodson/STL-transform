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
def cube(r, b, edgeround = 0.5):
  r = Vector3(abs(r.x), abs(r.y), abs(r.z))
  r -= b
  return abs(Vector3(max(r.x,0), max(r.y,0), max(r.z,0)))-edgeround


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

def torus(r):
  rad1 = 2
  rad2 = 0.5
  d = (r.x**2 + r.z**2)**0.5 - rad1
  return (d**2 + r.y**2)**0.5 - rad2

from transform import sphere_inverstion, sphere_reversion, spherical_projection, inverse_spherical_projection, oscillate
def inversion(r): return inverse_spherical_projection(r, Vector3(1,0,0), Vector3(0,4,0), blend = 0.5)


animate = True

if __name__ == '__main__':
  if animate == True:
    from subprocess import call
    call(["openscad", "-o", "out.png","-D",  'model="out.stl";',"veiw.scad"])
    stl_name = "torus"
    directory = "pics/" + stl_name
    call(["mkdir", directory])
    call(["cd", directory])
    files = []
    steps = 40
    time = 5.0
    for i in range(steps):
      j = oscillate(i/steps)
      def func(x,y,z):
        r = Vector3(x,y,z)
        s = sphere(r, j)
        g = gyroid(r)
        t = torus(r - Vector3(0,0,2))
        c = cube(r, Vector3(1,1,1))
        return smin(s, t)
      print i,"/",steps
      f_name = "{directory}/solid {i}.stl".format(**locals())
      files.append("{directory}/solid{i}.png".format(**locals()))
      isosurface(func, size = 5.0, filename = f_name)
      call(["openscad", "-o", "{directory}/solid{i}.png".format(**vars()),"-D",  'model="{directory}/solid {i}.stl";'.format(**vars()),"veiw.scad"])
    call(["convert", "-delay", str(time/steps*100), "-loop", "0"] + files + ["{directory}/animation.gif".format(**vars())])   


