from geom3py import Point, Box, Face, Line, Polygon, load_obj
from geom3py.visualization import Scene
import math
import time

polygons = load_obj(r"C:\Users\Alex\Documents\GitHub\geom3py\assets\test.obj")

###################################################


p1 = Point(5,4,3)
p2 = Point(8, 7, 6)
p3 = Point(-4, 4, 0)

cube = Box(p1, p2)
pol3d = Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 1], [0, 1, 0]])

star_points = []
for i in range(10):
    angle = 2 * math.pi * i / 10
    radius = 2.0 if i % 2 == 0 else 0.8
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    star_points.append(Point(x, y, 1))

poly = Polygon(star_points)
triangles = poly.triangles

line_g = Line.from_points([-9, -7, 0], [0, 0, 9])
line_g1 = Line.from_points([-9, 0, 0], [-9, -7, 0])
line_g2 = Line.from_points([0, -7, 0], [-9, -7, 0])
face2 =Face([0, 0, 0], line_g1.support_vector, line_g.support_vector, line_g2.support_vector)

####################################################

g = Line(Point(1, 2, 3), Point(1, 0, 0))
g2 = g.scale(2)
g3 = g.translate(Point(5, 0, 0))
g4 = g.rotate(90, "z")
g5 = g.reflect_on_point(Point(0, 0, 0))

####################################################

scene1 = Scene()
scene2 = Scene()
scene3 = Scene()

scene1.add(p1)
scene1.add(cube)
scene1.add(face2)
scene1.add(line_g, color="orange")
scene1.add(line_g1, color="yellow")
scene1.add(line_g2, color="lightyellow")
scene1.add(pol3d)
#scene1.add(poly)
for T in triangles:
    scene1.add(T)

scene2.add(g)
scene2.add(g2)
scene2.add(g3)
scene2.add(g4)
scene2.add(g5)

for poly in polygons:
    for i in range(len(poly.triangles)):
        line = Line(p3, poly.triangles[i].plane.foot_point(p3))
        scene3.add(line)

    scene3.add(poly)


print()

scene1.show()
scene2.show()
scene3.show()   