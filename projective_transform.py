from __future__ import division
from euclid import Vector3
from math import sqrt, copysign

output = open("sphericalhexagons_2.stl", 'w')
stl = open("circlehexagon.stl").readlines()
n = Vector3(0,0,1.0)
n.normalize()
t = 1

def spherical_projection(r, n):
	"lines parrallel to n are mapped to radial lines through the origin"
	r -= Vector3(0,0,5)
	d = r.dot(n)
	mu = 0.0 if d == 0 else abs(d) / r.magnitude()
	return r * mu
def blend(a,b,t):
	"lerp between a and b based on the factor t between 1 and 0"
	return a*t + b*(1.0-t)


for line in stl:
	s_line = line.strip()
	if s_line.startswith("vertex"):
		r = Vector3(*map(float, s_line.split(' ')[1:4]))
		new_r = spherical_projection(r, n)
		new_r = blend(new_r, r, t)
		output.write("vertex {} {} {}\n".format(*new_r))

	elif s_line.startswith("facet"):
		output.write("facet normal 0 0 0\n")
	else:
		output.write(line)