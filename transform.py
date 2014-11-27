from __future__ import division
from collections import namedtuple
from euclid import Vector3

class Face(object):
	def __init__(self, vertices, normal=None):
		if normal == None and len(vertices) == 3:
			a = vertices[2] - vertices[1]
			b = vertices[0] - vertices[1]
			self.normal = a.cross(b)
		else:
			self.normal = normal
		self.vertices = vertices
	def __str__(self):
		format_string = """\tfacet normal {n.x} {n.y} {n.z}\n\t\touter loop\n{verts}\t\tendloop\n\t\tendfacet\n"""
		verts = "".join("\t\t\tvertex {v.x} {v.y} {v.z}\n".format(v=vertex) for vertex in self.vertices)
		return format_string.format(n = self.normal, verts = verts)
	def transformed(self, f, depth = 0):
		"return a list of the new faces that this face got transfo into"
		split_distance = 0.5
		new_verts = map(f, self.vertices)
		longest_edge = max(((0,1,2), (1,2,0), (2,0,1)), key = lambda x : abs(new_verts[x[0]] - new_verts[x[1]]))
		v0 = new_verts[longest_edge[0]]
		v1 = new_verts[longest_edge[1]]
		v2 = new_verts[longest_edge[2]]
		g0 = self.vertices[longest_edge[0]]
		g1 = self.vertices[longest_edge[1]]
		g2 = self.vertices[longest_edge[2]]
		midpoint = (v0 + v1) / 2
		old_midpoint = (g0 + g1) / 2
		new_midpoint = f(old_midpoint)
		if abs(midpoint - new_midpoint) > split_distance and depth < 50:
			faces1 = Face(vertices = (g2, g0, old_midpoint)).transformed(f, depth+1)
			faces2 = Face(vertices = (g2, old_midpoint, g1)).transformed(f,depth +1)
			faces1.extend(faces2)
			return faces1
		return [Face(new_verts)]

class STL(object):
	def __init__(self, faces, name):
		self.faces = faces
		self.name = name
	def __str__(self):
		faces = "".join(str(face) for face in self.faces)
		return "solid {name}\n{faces}\nensolid {name}".format(name = self.name, faces = faces)
	def transformed(self, f):
		new_faces = []
		for face in self.faces:
			new_faces.extend(face.transformed(f))
		name = "{oldname} under {transform}".format(oldname = self.name, transform = f.__name__)
		return STL(new_faces, name)

def tokens_to_vector(tokens):
	return Vector3(*map(float, tokens))

def parse(tokens):
	current_face = None
	facets = []
	name = tokens[1]
	while tokens:
		token = tokens.pop()
		if token == "vertex":
			vertex = tokens_to_vector((tokens.pop(), tokens.pop(), tokens.pop()))
			current_face.vertices.append(vertex)
		if token == "facet":
			current_face = Face(list())
		if token == "normal":
			normal = tokens_to_vector((tokens.pop(), tokens.pop(), tokens.pop()))
			current_face.normal = normal
		if token == "endfacet":
			assert(current_face != None)
			facets.append(current_face)
			current_face = None
	return STL(facets, name)


def spherical_projection(r, n, t = Vector3(0,0,0), blend = 1.0):
	"lines parrallel to n are mapped to radial lines through the origin"
	r -= t
	d = r.dot(n)
	mag = r.magnitude()
	mu = 0.0 if d == 0 else abs(d) / mag
	new_r = r * mu
	return (new_r * blend) + r * (1.0 - blend)
def inverse_spherical_projection(r, n, t = Vector3(0,0,0), blend = 1.0):
	"lines parrallel to n are mapped to radial lines through the origin"
	d = r.dot(n)
	mag = r.magnitude()
	mu = 0 if d == 0 else abs(d) / mag
	new_r = r / mu if mu != 0 else Vector3(float("inf")*3)
	new_r -= t
	return (new_r * blend) + r * (1.0 - blend)

def sphere_inverstion(r,radius,t= Vector3(0,0,0)):
	r -= t
	mag = r.magnitude()
	if mag - radius == 0: return 0 * r
	return r.normalized() / (mag - radius)

def sphere_reversion(r,radius,t= Vector3(0,0,0)):
	mag = r.magnitude()
	if mag - radius == 0: return 0 * r
	r = r.normalized() * (mag - radius)
	r -= t
	return r

def blend(f, t):
	def _f(x):
		return f(x) * t + x * (1.0-t)
	return _f

def read_stl(filename):
	with open(filename) as f:
		stl = f.read().split()[::-1]
		return parse(stl)

from math import sin, pi
def oscillate(t):
	"vary sinusoidally from 0 to 1 to 1 as t goes from 0 to 1"
	return (sin(2.0*pi*t) + 1.0) / 2.0

def identity(r): return r
if __name__ == '__main__':
	import time.time as time
	t = time()
	from subprocess import call
	stl_name = "torus"
	stl = read_stl("stls/{}.stl".format(stl_name))
	directory = "pics/" + stl_name
	call(["mkdir", directory])
	call(["cd", directory])
	files = []
	steps = 40
	time = 7.0
	for i in range(steps):
		j = oscillate(i/steps)
		n = Vector3(-1,1,0).normalized()
		def spherical(r): return spherical_projection(r, n, blend = j*2)
		def inversion(r): return sphere_inverstion(r, 0, Vector3(0,2,0))
		f_name = "{directory}/solid {i}.stl".format(**locals())
		files.append("{directory}/solid{i}.png".format(**locals()))
		f = open(f_name, "w")
		new_stl = stl.transformed(blend(inversion, j))
		f.write(str(new_stl))
		call(["openscad", "-o", "{directory}/solid{i}.png".format(**vars()),"-D",  'model="{directory}/solid {i}.stl";'.format(**vars()),"veiw.scad"])
	#call(["convert", "-delay", str(time/steps*100), "-loop", "0"] + files + ["{directory}/animation.gif".format(**vars())])		
	print time() - t
