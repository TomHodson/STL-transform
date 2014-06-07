import pyglet
from pyglet.window import Window, key
from transform import read_stl, STL
import itertools as it
from pyglet.gl import *


scale = 1.0
window = Window(800,640, caption = 'Stl veiwer', vsync = True)
@window.event
def on_draw():
	global scale
	glViewport(0, 0, window.width, window.height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(65 * scale, window.width / float(window.height), .1, 1000)
	glMatrixMode(GL_MODELVIEW)
	return pyglet.event.EVENT_HANDLED

@window.event
def on_mouse_scroll(x, y, dx, dy):
	inc = 1.1
	global scale
	print inc**dy
	scale *= (inc**dy)

if __name__ == '__main__':
	stl = read_stl("sphere.stl")
	n_stl = stl.transformed(lambda x: x / 45.0 * scale)
	vertices = list(it.chain(*list(it.chain(*face.vertices) for face in n_stl.faces)))
	colour = (255,0,0)

	def draw(context):
		pyglet.graphics.draw(len(vertices)/3, pyglet.gl.GL_TRIANGLES,('v3f', vertices),('c3B',[x for _ in range(len(vertices)/3) for x in colour]) )
	
	pyglet.clock.schedule_interval(draw, 1.0/20.0)
	pyglet.app.run()