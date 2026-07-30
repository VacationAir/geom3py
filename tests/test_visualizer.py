from geom3py import Point, Box, Face, Line, Polygon
from geom3py.visualization import Scene

p1 = Point(5,4,3)
p2 = Point(8, 7, 6)
cube = Box(p1, p2)
pol3d = Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 1], [0, 1, 0]])
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

scene1.add(p1)
scene1.add(cube)
scene1.add(face2)
scene1.add(line_g, color="orange")
scene1.add(line_g1, color="yellow")
scene1.add(line_g2, color="lightyellow")
scene1.add(pol3d)

scene2.add(g)
scene2.add(g2)
scene2.add(g3)
scene2.add(g4)
scene2.add(g5)

scene1.show()
scene2.show()