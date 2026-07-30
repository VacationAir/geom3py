from geom3py import Point, Cube, Face
from geom3py.visualization import Scene

p1 = Point(5,4,3)
p2 = Point(8, 7, 6)
cube = Cube(p1, p2)
F = Face([0,0,0], [0,0,2], [2,0,0], [0,2,0])
scene = Scene()

scene.add(p1)
scene.add(cube)
scene.add(F)
scene.show()