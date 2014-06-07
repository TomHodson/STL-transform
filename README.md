STL-transforms
=============

Isosurface.py and Marching.py
--------------
Generates an stl by solving some function for f(x,y,z) == 0
For instance
```python
def f(x,y,z): return x**2 + y**2 + z**2 - 5 
```
would give a solid sphere of radius 5.

More interesting things include:

Gyroid:
```
def f(x,y,z): return cos(x) + cos(y) + cos(z)
```
![A gyroid, the solution to the above equation](pics/5.png?raw=true "Gyroid")

This is heavily related to the idea of distance fields, so have a look at
	http://iquilezles.org/www/articles/distfunctions/distfunctions.htm

You can also do intersections, unions, etc and even 'smooth' unions:
min(cube, sphere)

![The union of a cube and a sphere](pics/6.png?raw=true "min(cube, sphere)")

smin(cube, sphere)

![The smooth union of a cube and a sphere](pics/7.png?raw=true "smooth_min(cube, sphere)")

Transform.py
-------------
A bit of hacked together code to read in ASCII STL files and then some routines to transform the faces based on an arbitrary function, it splits the facets if they're very distorted.
for instance under a stereographic projection that turns parallel lines into radial lines
a cube

![cube](pics/cube.png?raw=true "cube")

becomes a section of a sphere

![cube](pics/transformed_cube.png?raw=true "cube")